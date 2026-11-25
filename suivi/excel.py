"""Écriture du classeur Excel de référence.

Structure :
- « Sommaire » : une ligne par entreprise (dernier dépôt, ratios du dernier exercice) ;
- « Journal » : les nouveaux dépôts détectés, avec lien vers le document sur EDGAR ;
- pour chaque entreprise : « TICKER - Résultats », « TICKER - Bilan », « TICKER - Flux »
  (valeurs) et « TICKER - Ratios » (formules qui pointent vers les trois autres onglets).

Chaque onglet a un bloc annuel en haut et un bloc trimestriel en dessous.
Le classeur est entièrement régénéré à chaque mise à jour : ne pas y saisir tes propres notes.
"""

from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

import pandas as pd
from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from .concepts import ETATS, TITRES_ETATS, TOUTES_LES_LIGNES
from .extraction import Donnees, libelle_exercice, libelle_trimestre
from .ratios import RATIOS, Contexte, formule_excel
from .sec import Depot

BLEU = "1F3864"
GRIS_CLAIR = "F2F2F2"
POLICE_TITRE = Font(bold=True, size=14, color=BLEU)
POLICE_ENTETE = Font(bold=True, color="FFFFFF")
FOND_ENTETE = PatternFill("solid", fgColor=BLEU)
FOND_BLOC = PatternFill("solid", fgColor="D9E1F2")
POLICE_DEDUITE = Font(italic=True, color="7F7F7F")
BORDURE_BAS = Border(bottom=Side(style="thin", color="BFBFBF"))

FMT_MONTANT = '#,##0;(#,##0);"–"'
FMT_MONTANT_DEC = '#,##0.0;(#,##0.0);"–"'
FMT_BPA = '0.00;(0.00)'
FMT_PCT = '0.0%;-0.0%'
FMT_X = '0.00"x";-0.00"x"'

LIGNE_ENTETE_ANNUEL = 4  # libellés de périodes ; ligne 5 = dates ; postes à partir de la ligne 6


@dataclass
class Entreprise:
    """Tout ce qu'il faut pour écrire les onglets d'une entreprise."""

    ticker: str
    cik: int
    donnees: Donnees
    dernier_depot: Depot | None
    ratios_annuels: pd.DataFrame
    ratios_trimestriels: pd.DataFrame


def _nom_onglet(ticker: str, etat: str) -> str:
    return f"{ticker} - {etat}"[:31]


def _ref(onglet: str, ligne: int, colonne: int) -> str:
    return f"'{onglet}'!{get_column_letter(colonne)}{ligne}"


def _lignes_affichees(donnees: Donnees, lignes) -> list:
    """Postes qui ont au moins une valeur (annuelle ou trimestrielle)."""
    garder = []
    for l in lignes:
        a = donnees.annuel.loc[l.cle] if l.cle in donnees.annuel.index else pd.Series(dtype=float)
        t = donnees.trimestriel.loc[l.cle] if l.cle in donnees.trimestriel.index else pd.Series(dtype=float)
        if a.notna().any() or t.notna().any():
            garder.append(l)
    return garder


def _format_poste(ligne) -> str:
    if ligne.unite == "USD/shares":
        return FMT_BPA
    if ligne.unite == "shares":
        return FMT_MONTANT_DEC
    return FMT_MONTANT


def _echelle(ligne, unite: int) -> float:
    if ligne.unite == "USD/shares":
        return 1
    if ligne.unite == "shares":
        return 1_000_000
    return unite


def _libelle_unite(unite: int) -> str:
    return {1: "en dollars US", 1000: "en milliers de $ US", 1_000_000: "en millions de $ US"}.get(
        unite, f"en unités de {unite:,} $ US"
    )


def _entete_bloc(ws, ligne: int, titre: str, periodes: list[date], libelles: list[str]):
    ws.cell(ligne, 1, titre).font = POLICE_ENTETE
    ws.cell(ligne, 1).fill = FOND_ENTETE
    ws.cell(ligne + 1, 1, "Fin de période").font = Font(italic=True, color="595959")
    for j, (p, lib) in enumerate(zip(periodes, libelles), start=2):
        c = ws.cell(ligne, j, lib)
        c.font, c.fill, c.alignment = POLICE_ENTETE, FOND_ENTETE, Alignment(horizontal="center")
        d = ws.cell(ligne + 1, j, p)
        d.number_format = "yyyy-mm-dd"
        d.font = Font(italic=True, color="595959")
        d.alignment = Alignment(horizontal="center")


def _libelles(periodes: list[date], mode: str, fins_annuelles: list[date]) -> list[str]:
    if mode == "annuel":
        return [libelle_exercice(p) for p in periodes]
    return [libelle_trimestre(p, fins_annuelles) for p in periodes]


def _mise_en_page(ws, nb_colonnes: int, largeur_a: int = 46):
    ws.column_dimensions["A"].width = largeur_a
    for j in range(2, nb_colonnes + 2):
        ws.column_dimensions[get_column_letter(j)].width = 13
    ws.freeze_panes = ws.cell(LIGNE_ENTETE_ANNUEL + 2, 2)
    ws.sheet_view.showGridLines = False


# --------------------------------------------------------------------------
# Onglets d'états financiers
# --------------------------------------------------------------------------
def _ecrire_etat(wb, ent: Entreprise, etat: str, unite: int, positions: dict):
    """Écrit un état et note dans `positions[(mode, cle)] = (onglet, ligne)` où trouver chaque poste."""
    d = ent.donnees
    onglet = _nom_onglet(ent.ticker, etat)
    ws = wb.create_sheet(onglet)
    ws.cell(1, 1, f"{d.nom} ({ent.ticker}) — {TITRES_ETATS[etat]}").font = POLICE_TITRE
    ws.cell(2, 1, f"Montants {_libelle_unite(unite)}, sauf BPA ($ par action) et actions (millions). "
                  "Source : SEC EDGAR, données XBRL. En gris italique : valeur déduite par calcul.").font = Font(
        italic=True, color="595959")

    lignes = _lignes_affichees(d, ETATS[etat])
    deduites = set(
        (r.type, r.poste, r.fin) for r in d.sources.itertuples() if r.deduite or str(r.balise).startswith("calcul")
    )
    ligne_courante = LIGNE_ENTETE_ANNUEL
    for mode, table, titre in (("annuel", d.annuel, "Annuel"), ("trimestriel", d.trimestriel, "Trimestriel")):
        periodes = list(table.columns)
        _entete_bloc(ws, ligne_courante, titre, periodes, _libelles(periodes, mode, d.fins_annuelles_toutes))
        for i, l in enumerate(lignes):
            r = ligne_courante + 2 + i
            ws.cell(r, 1, l.libelle).border = BORDURE_BAS
            positions[(mode, l.cle)] = (onglet, r)
            for j, p in enumerate(periodes, start=2):
                v = table.at[l.cle, p] if l.cle in table.index else None
                c = ws.cell(r, j)
                c.border = BORDURE_BAS
                if v is None or pd.isna(v):
                    continue
                c.value = float(v) / _echelle(l, unite)
                c.number_format = _format_poste(l)
                if (mode, l.cle, p) in deduites:
                    c.font = POLICE_DEDUITE
        ligne_courante += 2 + len(lignes) + 2
    _mise_en_page(ws, max(len(d.annuel.columns), len(d.trimestriel.columns)))


# --------------------------------------------------------------------------
# Onglet de ratios (formules)
# --------------------------------------------------------------------------
FORMATS_RATIOS = {"pct": FMT_PCT, "x": FMT_X, "montant": FMT_MONTANT}


def _ecrire_ratios(wb, ent: Entreprise, unite: int, positions: dict):
    d = ent.donnees
    onglet = _nom_onglet(ent.ticker, "Ratios")
    ws = wb.create_sheet(onglet)
    ws.cell(1, 1, f"{d.nom} ({ent.ticker}) — Ratios clés").font = POLICE_TITRE
    ws.cell(2, 1, f"Formules Excel calculées à partir des onglets Résultats, Bilan et Flux. "
                  f"Montants {_libelle_unite(unite)}. Clique sur une cellule pour voir le calcul.").font = Font(
        italic=True, color="595959")

    ligne_courante = LIGNE_ENTETE_ANNUEL
    for mode, table, titre in (("annuel", d.annuel, "Annuel"), ("trimestriel", d.trimestriel, "Trimestriel")):
        periodes = list(table.columns)
        _entete_bloc(ws, ligne_courante, titre, periodes, _libelles(periodes, mode, d.fins_annuelles_toutes))
        ctx = Contexte(table, mode)
        colonne = {p: j for j, p in enumerate(periodes, start=2)}

        def adresse(cle: str, p: date, _mode=mode) -> str:
            nom, r = positions[(_mode, cle)]
            return _ref(nom, r, colonne[p])

        for i, ratio in enumerate(RATIOS):
            r = ligne_courante + 2 + i
            c = ws.cell(r, 1, ratio.libelle)
            c.border = BORDURE_BAS
            c.comment = Comment(ratio.explication, "suivi")
            for p, j in colonne.items():
                cell = ws.cell(r, j)
                cell.border = BORDURE_BAS
                f = formule_excel(ratio, ctx, p, adresse)
                if f:
                    cell.value = f
                    cell.number_format = FORMATS_RATIOS[ratio.format]
        ligne_courante += 2 + len(RATIOS) + 2

    # Définitions
    ws.cell(ligne_courante, 1, "Définitions").font = Font(bold=True, color=BLEU)
    for i, ratio in enumerate(RATIOS, start=1):
        ws.cell(ligne_courante + i, 1, ratio.libelle).font = Font(bold=True)
        ws.cell(ligne_courante + i, 2, ratio.explication)
    _mise_en_page(ws, max(len(d.annuel.columns), len(d.trimestriel.columns)), largeur_a=40)


# --------------------------------------------------------------------------
# Sommaire et journal
# --------------------------------------------------------------------------
COLONNES_SOMMAIRE = [
    ("Ticker", 9, None), ("Entreprise", 28, None), ("Dernier dépôt", 12, None), ("Période", 12, "yyyy-mm-dd"),
    ("Déposé le", 12, "yyyy-mm-dd"), ("Document", 11, None), ("Dernier exercice", 14, None),
    ("Revenus", 13, FMT_MONTANT), ("Marge nette", 12, FMT_PCT), ("Marge FCF", 12, FMT_PCT),
    ("ROE", 10, FMT_PCT), ("Dette nette / BAIIA", 12, FMT_X), ("Croissance revenus", 12, FMT_PCT),
    ("Croissance BPA", 12, FMT_PCT),
]


def _ecrire_sommaire(ws, entreprises: list[Entreprise], unite: int):
    ws.title = "Sommaire"
    ws.cell(1, 1, "Suivi des états financiers").font = POLICE_TITRE
    ws.cell(2, 1, f"Mis à jour le {datetime.now():%Y-%m-%d %H:%M}. Source : SEC EDGAR (XBRL). "
                  f"Montants {_libelle_unite(unite)}. Ratios du dernier exercice complet. "
                  "Vérifie toujours dans le rapport officiel ; ceci n'est pas un conseil financier.").font = Font(
        italic=True, color="595959")
    for j, (titre, largeur, _) in enumerate(COLONNES_SOMMAIRE, start=1):
        c = ws.cell(4, j, titre)
        c.font, c.fill = POLICE_ENTETE, FOND_ENTETE
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(j)].width = largeur
    ws.row_dimensions[4].height = 32

    for i, e in enumerate(entreprises, start=5):
        ra = e.ratios_annuels
        der = ra.columns[-1] if len(ra.columns) else None
        val = (lambda cle: None if der is None or pd.isna(ra.at[cle, der]) else float(ra.at[cle, der]))
        revenus = e.donnees.annuel.at["revenus", der] if der is not None else None
        dep = e.dernier_depot
        valeurs = [
            e.ticker, e.donnees.nom, dep.formulaire if dep else None,
            date.fromisoformat(dep.date_periode) if dep and dep.date_periode else None,
            date.fromisoformat(dep.date_depot) if dep else None, "Ouvrir" if dep else None,
            libelle_exercice(der) if der is not None else None,
            None if revenus is None or pd.isna(revenus) else float(revenus) / unite,
            val("marge_nette"), val("marge_fcf"), val("roe"), val("dette_nette_baiia"),
            val("croissance_revenus"), val("croissance_bpa"),
        ]
        for j, (v, (_, _, fmt)) in enumerate(zip(valeurs, COLONNES_SOMMAIRE), start=1):
            c = ws.cell(i, j, v)
            c.border = BORDURE_BAS
            if fmt:
                c.number_format = fmt
        if dep:
            lien = ws.cell(i, 6)
            lien.hyperlink = dep.url
            lien.font = Font(color="0563C1", underline="single")
        ws.cell(i, 1).hyperlink = f"#'{_nom_onglet(e.ticker, 'Ratios')}'!A1"
        ws.cell(i, 1).font = Font(bold=True, color="0563C1", underline="single")
    ws.freeze_panes = "C5"
    ws.sheet_view.showGridLines = False


def _ecrire_journal(wb, journal: list[dict]):
    ws = wb.create_sheet("Journal")
    ws.cell(1, 1, "Nouveaux dépôts détectés").font = POLICE_TITRE
    entetes = [("Détecté le", 18), ("Ticker", 9), ("Formulaire", 11), ("Période", 12), ("Déposé le", 12), ("Lien", 60)]
    for j, (t, w) in enumerate(entetes, start=1):
        c = ws.cell(3, j, t)
        c.font, c.fill = POLICE_ENTETE, FOND_ENTETE
        ws.column_dimensions[get_column_letter(j)].width = w
    for i, e in enumerate(reversed(journal), start=4):
        for j, cle in enumerate(("detecte_le", "ticker", "formulaire", "periode", "date_depot", "url"), start=1):
            ws.cell(i, j, e.get(cle))
        if e.get("url"):
            ws.cell(i, 6).hyperlink = e["url"]
            ws.cell(i, 6).font = Font(color="0563C1", underline="single")
    ws.freeze_panes = "A4"


# --------------------------------------------------------------------------
# Point d'entrée
# --------------------------------------------------------------------------
def ecrire_classeur(chemin: Path, entreprises: list[Entreprise], journal: list[dict], unite: int) -> Path:
    """Écrit le classeur. Lève PermissionError si le fichier est ouvert dans Excel."""
    wb = Workbook()
    _ecrire_sommaire(wb.active, entreprises, unite)
    _ecrire_journal(wb, journal)
    for e in entreprises:
        positions: dict = {}
        for etat in ETATS:
            _ecrire_etat(wb, e, etat, unite, positions)
        _ecrire_ratios(wb, e, unite, positions)
    wb.calculation.fullCalcOnLoad = True  # Excel recalcule les formules à l'ouverture

    chemin = Path(chemin)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    # On écrit dans un fichier temporaire puis on remplace : si Excel a le fichier ouvert,
    # le remplacement échoue proprement et l'ancien classeur reste intact.
    fd, tmp = tempfile.mkstemp(suffix=".xlsx", dir=chemin.parent)
    os.close(fd)
    try:
        wb.save(tmp)
        os.replace(tmp, chemin)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    return chemin
