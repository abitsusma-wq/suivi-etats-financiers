"""Transforme les données XBRL brutes de la SEC en tableaux par période.

Points délicats gérés ici :
- Une même valeur est déclarée dans plusieurs dépôts (le 10-K de 2026 reprend 2025) :
  on garde la valeur du dépôt le plus récent, donc les chiffres retraités.
- Les 10-Q donnent les flux de trésorerie en cumul depuis le début de l'exercice (6 mois,
  9 mois). Le trimestre se déduit par différence : (9 mois) - (6 mois).
- Il n'y a pas de 10-Q pour le 4e trimestre : T4 = exercice complet - 9 mois.
- Le BPA et le nombre d'actions ne s'additionnent pas : jamais déduits par différence.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

import pandas as pd

from .concepts import ETATS, TOUTES_LES_LIGNES, Ligne

FORMULAIRES_ACCEPTES = ("10-K", "10-Q")  # 10-K/A et 10-Q/A inclus (startswith)
DUREE_TRIMESTRE = (80, 115)  # jours : 12 à 16 semaines (Costco a un T4 de 16 semaines)
DUREE_ANNEE = (350, 380)  # exercices de 52 ou 53 semaines


def _d(texte: str) -> date:
    return date.fromisoformat(texte)


def _faits(facts: dict, balise: str, unite: str) -> list[dict]:
    brut = facts.get("facts", {}).get("us-gaap", {}).get(balise, {}).get("units", {}).get(unite, [])
    return [f for f in brut if str(f.get("form", "")).startswith(FORMULAIRES_ACCEPTES)]


def _par_periode(faits: list[dict]) -> dict:
    """{(debut, fin)} ou {fin} -> valeur, en gardant le dépôt le plus récent."""
    meilleurs: dict = {}
    for f in faits:
        cle = (_d(f["start"]), _d(f["end"])) if "start" in f else _d(f["end"])
        if cle not in meilleurs or f["filed"] > meilleurs[cle][1]:
            meilleurs[cle] = (f["val"], f["filed"])
    return {k: v[0] for k, v in meilleurs.items()}


def _dans(jours: int, bornes: tuple[int, int]) -> bool:
    return bornes[0] <= jours <= bornes[1]


# --------------------------------------------------------------------------
# Valeur d'une balise pour une période
# --------------------------------------------------------------------------
def valeur_annuelle(donnees: dict, fin: date, ligne: Ligne):
    if ligne.nature == "stock":
        return donnees.get(fin)
    for (debut, f), v in donnees.items():
        if isinstance(f, date) and f == fin and _dans((f - debut).days, DUREE_ANNEE):
            return v
    return None


def valeur_trimestrielle(donnees: dict, fin: date, ligne: Ligne):
    """Renvoie (valeur, deduite) ; deduite=True si calculée par différence de cumuls."""
    if ligne.nature == "stock":
        return donnees.get(fin), False
    cumuls = {}
    for cle, v in donnees.items():
        if not isinstance(cle, tuple) or cle[1] != fin:
            continue
        debut = cle[0]
        duree = (fin - debut).days
        if _dans(duree, DUREE_TRIMESTRE):
            return v, False
        if duree > DUREE_TRIMESTRE[1]:
            cumuls[debut] = v
    if not ligne.additif:
        return None, False
    # Cumul jusqu'à `fin` moins cumul jusqu'à la fin du trimestre précédent, même début.
    for debut, v_cumul in sorted(cumuls.items(), key=lambda kv: kv[0], reverse=True):
        for cle, v_prec in donnees.items():
            if isinstance(cle, tuple) and cle[0] == debut and _dans((fin - cle[1]).days, DUREE_TRIMESTRE):
                return v_cumul - v_prec, True
    return None, False


# --------------------------------------------------------------------------
# Choix des périodes
# --------------------------------------------------------------------------
LIGNES_REPERES = ("revenus", "benefice_net", "flux_exploitation")


def _toutes_durees(facts: dict, formulaires: tuple[str, ...] = FORMULAIRES_ACCEPTES) -> list[tuple[date, date]]:
    durees = []
    for cle in LIGNES_REPERES:
        ligne = TOUTES_LES_LIGNES[cle]
        for balise in ligne.balises:
            for f in _faits(facts, balise, ligne.unite):
                if "start" in f and str(f.get("form", "")).startswith(formulaires):
                    durees.append((_d(f["start"]), _d(f["end"])))
    return durees


def fins_exercices(facts: dict) -> list[date]:
    # Seuls les 10-K définissent les exercices : certains 10-Q (ex. Amazon) déclarent aussi
    # des cumuls sur 12 mois glissants, qui passeraient sinon pour des fins d'exercice.
    return sorted({fin for debut, fin in _toutes_durees(facts, ("10-K",)) if _dans((fin - debut).days, DUREE_ANNEE)})


def fins_trimestres(facts: dict) -> list[date]:
    fins = set()
    for debut, fin in _toutes_durees(facts):
        duree = (fin - debut).days
        # trimestre, cumul 6 ou 9 mois, ou exercice complet : tous finissent sur une fin de trimestre
        if duree >= DUREE_TRIMESTRE[0]:
            fins.add(fin)
    return sorted(fins)


# --------------------------------------------------------------------------
# Libellés de période (exercice fiscal)
# --------------------------------------------------------------------------
def libelle_exercice(fin: date) -> str:
    # Un exercice qui finit début janvier (ex. 52 semaines) est rattaché à l'année précédente.
    annee = fin.year - 1 if fin.month == 1 and fin.day <= 7 else fin.year
    return f"Ex. {annee}"


def libelle_trimestre(fin: date, fins_annuelles: list[date]) -> str:
    """Ex. 'T3 2026' en exercice fiscal de l'entreprise."""
    if not fins_annuelles:
        return fin.isoformat()
    candidates = [f for f in fins_annuelles if f >= fin - timedelta(days=3)]
    if candidates:
        fin_ex = min(candidates)
    else:  # exercice en cours : on prolonge par pas d'un an
        fin_ex = fins_annuelles[-1]
        while fin_ex < fin - timedelta(days=3):
            fin_ex += timedelta(days=365)
    ecart = (fin_ex - fin).days
    numero = 4 - round(ecart / 91.3)
    numero = min(4, max(1, numero))
    return f"T{numero} {libelle_exercice(fin_ex)[4:]}"


# --------------------------------------------------------------------------
# Extraction complète
# --------------------------------------------------------------------------
@dataclass
class Donnees:
    """Résultat de l'extraction pour une entreprise."""

    nom: str
    annuel: pd.DataFrame  # index = clé de poste, colonnes = date de fin d'exercice
    trimestriel: pd.DataFrame  # colonnes = date de fin de trimestre
    sources: pd.DataFrame  # format long : poste, type, fin, valeur, balise, déduite
    fins_annuelles_toutes: list[date]


def _calculer(expression: tuple[str, ...], valeurs: dict):
    """Évalue une expression de repli du type ('a', '-', 'b').

    '+' : les postes manquants comptent pour 0 (au moins un doit exister).
    '-' : les deux postes doivent exister.
    """
    termes = [expression[0]] + list(expression[2::2])
    ops = ["+"] + list(expression[1::2])
    if "-" in ops and any(valeurs.get(t) is None for t in termes):
        return None
    presents = [valeurs.get(t) for t in termes]
    if all(v is None for v in presents):
        return None
    total = 0
    for op, v in zip(ops, presents):
        total += (v or 0) if op == "+" else -(v or 0)
    return total


def extraire(facts: dict, annees: int = 10, trimestres: int = 12) -> Donnees:
    fins_a = fins_exercices(facts)
    fins_t = fins_trimestres(facts)
    sources = []
    tables = {}

    for mode, fins in (("annuel", fins_a), ("trimestriel", fins_t)):
        valeurs: dict[str, dict[date, float]] = {}
        for lignes in ETATS.values():
            for ligne in lignes:
                valeurs[ligne.cle] = {}
                donnees_par_balise = [(b, _par_periode(_faits(facts, b, ligne.unite))) for b in ligne.balises]
                for fin in fins:
                    for balise, donnees in donnees_par_balise:
                        if mode == "annuel":
                            v, deduite = valeur_annuelle(donnees, fin, ligne), False
                        else:
                            v, deduite = valeur_trimestrielle(donnees, fin, ligne)
                        if v is not None:
                            valeurs[ligne.cle][fin] = v
                            sources.append((ligne.cle, mode, fin, v, balise, deduite))
                            break
        # Postes calculés en repli (ex. bénéfice brut = revenus - coût des ventes)
        for ligne in TOUTES_LES_LIGNES.values():
            if not ligne.calcul:
                continue
            for fin in fins:
                if fin in valeurs[ligne.cle]:
                    continue
                v = _calculer(ligne.calcul, {c: valeurs[c].get(fin) for c in ligne.calcul[::2]})
                if v is not None:
                    valeurs[ligne.cle][fin] = v
                    sources.append((ligne.cle, mode, fin, v, "calcul: " + " ".join(ligne.calcul), False))

        df = pd.DataFrame(valeurs).T.reindex(list(TOUTES_LES_LIGNES))
        df = df.reindex(columns=sorted(df.columns))
        # On ne garde que les périodes où le bénéfice net est connu (filtre les dates parasites)
        if "benefice_net" in df.index:
            df = df.loc[:, df.loc["benefice_net"].notna()]
        n = annees if mode == "annuel" else trimestres
        tables[mode] = df.iloc[:, -n:] if n > 0 else df.iloc[:, :0]

    sources_df = pd.DataFrame(sources, columns=["poste", "type", "fin", "valeur", "balise", "deduite"])
    return Donnees(
        nom=facts.get("entityName", ""),
        annuel=tables["annuel"],
        trimestriel=tables["trimestriel"],
        sources=sources_df,
        fins_annuelles_toutes=fins_a,
    )
