"""Mémoire entre deux exécutions : dernier dépôt traité par entreprise et journal des nouveautés."""

from __future__ import annotations

import json
from pathlib import Path


def charger_etat(chemin: Path) -> dict:
    chemin = Path(chemin)
    if chemin.exists():
        etat = json.loads(chemin.read_text(encoding="utf-8"))
    else:
        etat = {}
    etat.setdefault("entreprises", {})
    etat.setdefault("journal", [])
    return etat


def sauver_etat(chemin: Path, etat: dict) -> None:
    chemin = Path(chemin)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    tmp = chemin.with_suffix(".tmp")
    tmp.write_text(json.dumps(etat, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(chemin)
