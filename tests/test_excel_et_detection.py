"""Tests de bout en bout sans réseau : la SEC est remplacée par un faux client."""

import json
import re
from datetime import date

import pytest
from openpyxl import load_workbook

from suivi import __main__ as principal
from suivi.config import charger_config
from suivi.sec import Depot

from .conftest import facts_fictifs

REF = re.compile(r"'([^']+)'!([A-Z]+[0-9]+)")


def evaluer(wb, formule: str) -> float:
    """Évalue une formule simple (+ - * / et références) comme le ferait Excel."""
    expr = REF.sub(lambda m: repr(float(wb[m.group(1)][m.group(2)].value or 0)), formule.lstrip("="))
    assert re.fullmatch(r"[0-9eE.+\-*/() ]+", expr), expr
    return eval(expr)  # noqa: S307 (expression purement numérique, vérifiée ci-dessus)


class FauxClient:
    depots = {}

    def __init__(self, user_agent, dossier_cache):
        self.dossier_cache = dossier_cache
        dossier_cache.mkdir(parents=True, exist_ok=True)

    def cik_pour(self, ticker):
        return 1

    def derniers_depots(self, cik):
        return FauxClient.depots

    def company_facts(self, cik, rafraichir=True):
        (self.dossier_cache / f"facts_CIK{cik:010d}.json").write_text("{}")
        return facts_fictifs()


@pytest.fixture
def projet(tmp_path, monkeypatch):
    (tmp_path / "config.yaml").write_text(
        "entreprises:\n  - ticker: FICT\nuser_agent: \"Test test@example.com\"\nunite: 1\n", encoding="utf-8")
    monkeypatch.setattr(principal, "ClientSEC", FauxClient)
    return tmp_path


def depot(accn, form="10-K"):
    return [Depot(form, accn, "2026-02-01", "2025-12-31", "doc.htm", 1)]


def test_classeur_et_formules(projet):
    FauxClient.depots = depot("0000000001-26-000001")
    assert principal.executer(["--config", str(projet / "config.yaml")]) == 0

    wb = load_workbook(projet / "sortie" / "etats_financiers.xlsx")
    assert wb.sheetnames == ["Sommaire", "Journal", "FICT - Résultats", "FICT - Bilan", "FICT - Flux", "FICT - Ratios"]

    ws = wb["FICT - Ratios"]
    lignes = {}
    for r in range(1, ws.max_row + 1):
        lignes.setdefault(ws.cell(r, 1).value, r)  # 1re occurrence = bloc annuel
    r = lignes["Marge nette"]
    formule = ws.cell(r, 3).value  # colonne C = exercice 2025
    assert formule == "=('FICT - Résultats'!C10/'FICT - Résultats'!C6)"
    assert evaluer(wb, formule) == pytest.approx(60 / 500)
    assert evaluer(wb, ws.cell(lignes["Rendement des capitaux propres (ROE)"], 3).value) == pytest.approx(60 / 210)
    assert ws.cell(lignes["Croissance des revenus (sur 1 an)"], 2).value is None  # pas d'année précédente

    som = wb["Sommaire"]
    assert som["A5"].value == "FICT"
    assert som["I5"].value == pytest.approx(60 / 500)  # marge nette
    assert (projet / "donnees" / "FICT_etats.csv").exists()


def test_detection_nouveau_depot(projet):
    cfg = ["--config", str(projet / "config.yaml")]
    FauxClient.depots = depot("0000000001-26-000001")
    principal.executer(cfg)  # premier passage : rien dans le journal
    etat = json.loads((projet / "donnees" / "etat.json").read_text(encoding="utf-8"))
    assert etat["journal"] == []
    assert etat["entreprises"]["FICT"]["derniere_accession"] == "0000000001-26-000001"

    principal.executer(cfg)  # même dépôt : toujours rien
    assert json.loads((projet / "donnees" / "etat.json").read_text(encoding="utf-8"))["journal"] == []

    # Nouveau dépôt pas encore intégré à l'API XBRL : pas marqué comme traité
    FauxClient.depots = depot("0000000001-26-000099", "10-Q")
    principal.executer(cfg)
    etat = json.loads((projet / "donnees" / "etat.json").read_text(encoding="utf-8"))
    assert etat["entreprises"]["FICT"]["derniere_accession"] == "0000000001-26-000001"
    assert etat["journal"] == []


def test_detection_nouveau_depot_integre(projet, monkeypatch):
    cfg = ["--config", str(projet / "config.yaml")]
    FauxClient.depots = depot("ancien")
    monkeypatch.setattr(principal, "_depot_dans_facts", lambda facts, accn: True)
    principal.executer(cfg)
    FauxClient.depots = depot("nouveau", "10-Q")
    principal.executer(cfg)
    etat = json.loads((projet / "donnees" / "etat.json").read_text(encoding="utf-8"))
    assert [j["formulaire"] for j in etat["journal"]] == ["10-Q"]
    wb = load_workbook(projet / "sortie" / "etats_financiers.xlsx")
    assert wb["Journal"]["C4"].value == "10-Q"


def test_classeur_ouvert_dans_excel(projet, monkeypatch):
    FauxClient.depots = depot("x")

    def verrouille(*a, **k):
        raise PermissionError

    monkeypatch.setattr(principal, "ecrire_classeur", verrouille)
    assert principal.executer(["--config", str(projet / "config.yaml")]) == 1
    assert not (projet / "donnees" / "etat.json").exists()  # sera retenté


def test_config_user_agent_obligatoire(tmp_path):
    (tmp_path / "config.yaml").write_text("entreprises: [AAPL]\nuser_agent: sans-courriel\n", encoding="utf-8")
    with pytest.raises(ValueError):
        charger_config(tmp_path / "config.yaml")


def test_config_liste_simple(tmp_path):
    (tmp_path / "config.yaml").write_text("entreprises: [aapl, MSFT]\nuser_agent: a b@c.d\n", encoding="utf-8")
    cfg = charger_config(tmp_path / "config.yaml")
    assert [e.ticker for e in cfg.entreprises] == ["AAPL", "MSFT"]
