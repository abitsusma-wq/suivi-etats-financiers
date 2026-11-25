"""Ratios clés, définis une seule fois et calculés de deux façons :

- en Python (valeurs pour le sommaire, le CSV et les tests) ;
- en formules Excel (onglet Ratios), pour que tu puisses cliquer sur une cellule et voir
  le calcul, par ex. ='AAPL - Résultats'!K9/'AAPL - Résultats'!K6.

Une formule n'est écrite que si toutes ses données existent ; sinon la cellule reste vide.

En mode trimestriel, les ratios qui comparent un flux à un stock (ROE, dette nette/BAIIA)
utilisent la somme des 4 derniers trimestres (« 12 mois glissants »).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Callable

import pandas as pd

ECART_TRIMESTRE = (80, 115)  # 12 à 16 semaines entre deux fins de trimestre
ECART_ANNEE = (350, 380)


# --------------------------------------------------------------------------
# Contexte : où trouver les valeurs
# --------------------------------------------------------------------------
class Contexte:
    def __init__(self, table: pd.DataFrame, mode: str):
        """table : index = clés de postes, colonnes = dates de fin (triées)."""
        self.table = table
        self.mode = mode
        self.periodes: list[date] = list(table.columns)

    def valeur(self, cle: str, p: date):
        if cle not in self.table.index or p not in self.table.columns:
            return None
        v = self.table.at[cle, p]
        return None if pd.isna(v) else float(v)

    def _decalage(self, p: date, bornes: tuple[int, int]):
        for q in reversed(self.periodes):
            if q < p and bornes[0] <= (p - q).days <= bornes[1]:
                return q
        return None

    def an_precedent(self, p: date):
        return self._decalage(p, ECART_ANNEE)

    def quatre_trimestres(self, p: date):
        """[p, p-1T, p-2T, p-3T] si les 4 trimestres consécutifs sont présents."""
        chaine = [p]
        while len(chaine) < 4:
            q = self._decalage(chaine[-1], ECART_TRIMESTRE)
            if q is None:
                return None
            chaine.append(q)
        return chaine


Adresse = Callable[[str, date], str]  # (clé du poste, période) -> "'AAPL - Bilan'!C7"


# --------------------------------------------------------------------------
# Mini-langage d'expressions
# --------------------------------------------------------------------------
class Expr:
    def valeur(self, ctx: Contexte, p: date):
        raise NotImplementedError

    def excel(self, ctx: Contexte, p: date, adr: Adresse) -> str:
        raise NotImplementedError

    def __add__(self, o): return Op("+", self, _e(o))
    def __sub__(self, o): return Op("-", self, _e(o))
    def __truediv__(self, o): return Op("/", self, _e(o))


def _e(x) -> Expr:
    return x if isinstance(x, Expr) else Const(x)


@dataclass
class Const(Expr):
    v: float

    def valeur(self, ctx, p): return self.v
    def excel(self, ctx, p, adr): return repr(self.v).rstrip("0").rstrip(".") if isinstance(self.v, float) else str(self.v)


@dataclass
class Poste(Expr):
    """Valeur d'un poste à la période. optionnel=True : absent = 0."""

    cle: str
    optionnel: bool = False

    def valeur(self, ctx, p):
        v = ctx.valeur(self.cle, p)
        return 0.0 if v is None and self.optionnel else v

    def excel(self, ctx, p, adr):
        if ctx.valeur(self.cle, p) is None and self.optionnel:
            return "0"
        return adr(self.cle, p)


@dataclass
class Flux12m(Expr):
    """Flux sur un an : valeur annuelle, ou somme des 4 derniers trimestres."""

    cle: str

    def _periodes(self, ctx, p):
        return [p] if ctx.mode == "annuel" else ctx.quatre_trimestres(p)

    def valeur(self, ctx, p):
        ps = self._periodes(ctx, p)
        if not ps:
            return None
        vals = [ctx.valeur(self.cle, q) for q in ps]
        return None if any(v is None for v in vals) else sum(vals)

    def excel(self, ctx, p, adr):
        ps = self._periodes(ctx, p)
        if len(ps) == 1:
            return adr(self.cle, p)
        return "(" + "+".join(adr(self.cle, q) for q in reversed(ps)) + ")"


@dataclass
class AnPrecedent(Expr):
    """La même expression évaluée un an plus tôt (même trimestre l'an dernier)."""

    e: Expr

    def valeur(self, ctx, p):
        q = ctx.an_precedent(p)
        return None if q is None else self.e.valeur(ctx, q)

    def excel(self, ctx, p, adr):
        return self.e.excel(ctx, ctx.an_precedent(p), adr)


@dataclass
class Op(Expr):
    op: str
    a: Expr
    b: Expr

    def valeur(self, ctx, p):
        x, y = self.a.valeur(ctx, p), self.b.valeur(ctx, p)
        if x is None or y is None:
            return None
        if self.op == "+": return x + y
        if self.op == "-": return x - y
        if self.op == "/": return None if y == 0 else x / y
        raise ValueError(self.op)

    def excel(self, ctx, p, adr):
        return f"({self.a.excel(ctx, p, adr)}{self.op}{self.b.excel(ctx, p, adr)})"


def moyenne(a: Expr, b: Expr) -> Expr:
    return (a + b) / 2


# --------------------------------------------------------------------------
# Les ratios
# --------------------------------------------------------------------------
@dataclass
class Ratio:
    cle: str
    libelle: str
    expr: Expr
    format: str  # "pct", "x" (multiple) ou "montant"
    explication: str


R, F = Poste, Flux12m
FCF = R("flux_exploitation") - R("capex")
BAIIA = R("resultat_exploitation") + R("amortissements")
DETTE_NETTE = R("dette_totale", optionnel=True) - R("tresorerie") - R("placements_ct", optionnel=True)

RATIOS = [
    Ratio("marge_brute", "Marge brute", R("benefice_brut") / R("revenus"), "pct",
          "Bénéfice brut / revenus. Ce qui reste après le coût direct des produits vendus."),
    Ratio("marge_exploitation", "Marge d'exploitation", R("resultat_exploitation") / R("revenus"), "pct",
          "Résultat d'exploitation / revenus. Rentabilité du cœur de métier."),
    Ratio("marge_nette", "Marge nette", R("benefice_net") / R("revenus"), "pct",
          "Bénéfice net / revenus."),
    Ratio("qualite_benefices", "Flux d'exploitation / bénéfice net", R("flux_exploitation") / R("benefice_net"), "x",
          "Qualité des bénéfices : au-dessus de 1, le bénéfice est bien converti en trésorerie."),
    Ratio("fcf", "Flux de trésorerie disponible (FCF)", FCF, "montant",
          "Flux d'exploitation - capex. L'argent disponible pour dividendes, rachats ou dette."),
    Ratio("marge_fcf", "Marge FCF", FCF / R("revenus"), "pct",
          "FCF / revenus."),
    Ratio("baiia", "BAIIA (EBITDA)", BAIIA, "montant",
          "Résultat d'exploitation + amortissements."),
    Ratio("dette_nette", "Dette nette", DETTE_NETTE, "montant",
          "Dette financière - trésorerie - placements CT (hors obligations locatives). Négatif = trésorerie nette."),
    Ratio("dette_nette_baiia", "Dette nette / BAIIA",
          DETTE_NETTE / (F("resultat_exploitation") + F("amortissements")), "x",
          "Années de BAIIA pour rembourser la dette nette. En trimestriel : BAIIA des 12 derniers mois."),
    Ratio("roe", "Rendement des capitaux propres (ROE)",
          F("benefice_net") / moyenne(R("capitaux_propres"), AnPrecedent(R("capitaux_propres"))), "pct",
          "Bénéfice net (12 mois) / capitaux propres moyens (début et fin). Peu parlant si les capitaux propres sont faibles ou négatifs."),
    Ratio("liquidite", "Ratio de liquidité générale", R("actif_courant") / R("passif_courant"), "x",
          "Actif courant / passif courant."),
    Ratio("croissance_revenus", "Croissance des revenus (sur 1 an)", R("revenus") / AnPrecedent(R("revenus")) - 1, "pct",
          "Par rapport à l'exercice précédent, ou au même trimestre l'an dernier."),
    Ratio("croissance_benefice_net", "Croissance du bénéfice net (sur 1 an)",
          R("benefice_net") / AnPrecedent(R("benefice_net")) - 1, "pct",
          "Même principe. Peu parlant si le bénéfice précédent était faible ou négatif."),
    Ratio("croissance_bpa", "Croissance du BPA dilué (sur 1 an)", R("bpa_dilue") / AnPrecedent(R("bpa_dilue")) - 1, "pct",
          "La croissance du BPA intègre l'effet des rachats d'actions."),
]

RATIOS_PAR_CLE = {r.cle: r for r in RATIOS}


def calculer_ratios(table: pd.DataFrame, mode: str) -> pd.DataFrame:
    ctx = Contexte(table, mode)
    lignes = {r.cle: {p: r.expr.valeur(ctx, p) for p in ctx.periodes} for r in RATIOS}
    return pd.DataFrame(lignes).T.reindex(columns=ctx.periodes)


def formule_excel(ratio: Ratio, ctx: Contexte, p: date, adr: Adresse) -> str | None:
    """Formule Excel du ratio, ou None si une donnée manque."""
    if ratio.expr.valeur(ctx, p) is None:
        return None
    return "=" + ratio.expr.excel(ctx, p, adr)
