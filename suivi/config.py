"""Lecture du fichier config.yaml."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

RACINE = Path(__file__).resolve().parent.parent


@dataclass
class Entreprise:
    ticker: str
    cik: int | None = None


@dataclass
class Config:
    entreprises: list[Entreprise]
    user_agent: str
    annees: int = 10
    trimestres: int = 12
    unite: int = 1_000_000
    fichier_excel: Path = field(default_factory=lambda: RACINE / "sortie" / "etats_financiers.xlsx")
    dossier_cache: Path = field(default_factory=lambda: RACINE / "cache")
    dossier_donnees: Path = field(default_factory=lambda: RACINE / "donnees")
    fichier_etat: Path = field(default_factory=lambda: RACINE / "donnees" / "etat.json")


def charger_config(chemin: Path | str = RACINE / "config.yaml") -> Config:
    chemin = Path(chemin)
    with open(chemin, encoding="utf-8") as f:
        brut = yaml.safe_load(f) or {}

    entreprises = []
    for e in brut.get("entreprises", []):
        if isinstance(e, str):  # on accepte aussi une simple liste de tickers
            e = {"ticker": e}
        entreprises.append(Entreprise(ticker=str(e["ticker"]).upper(), cik=e.get("cik")))
    if not entreprises:
        raise ValueError("Aucune entreprise dans config.yaml (clé 'entreprises').")

    user_agent = brut.get("user_agent", "").strip()
    if "@" not in user_agent:
        raise ValueError(
            "La SEC exige un user_agent au format 'NomDuClient contact@domaine.com' dans config.yaml."
        )

    base = chemin.parent
    return Config(
        entreprises=entreprises,
        user_agent=user_agent,
        annees=int(brut.get("annees", 10)),
        trimestres=int(brut.get("trimestres", 12)),
        unite=int(brut.get("unite", 1_000_000)),
        fichier_excel=base / brut.get("fichier_excel", "sortie/etats_financiers.xlsx"),
        dossier_cache=base / "cache",
        dossier_donnees=base / "donnees",
        fichier_etat=base / "donnees" / "etat.json",
    )
