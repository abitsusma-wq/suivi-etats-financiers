"""Données XBRL fictives, au même format que l'API companyfacts de la SEC.

Entreprise imaginaire, exercice terminé fin décembre, deux exercices (2024 et 2025).
Les trimestres de 2025 sont déclarés comme dans les vrais 10-Q :
- revenus et bénéfice : valeur du trimestre ET cumul depuis le début de l'exercice ;
- flux d'exploitation : uniquement en cumul (3, 6, 9 mois), comme dans la réalité.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def fait(val, end, start=None, form="10-K", filed="2026-02-01", accn="0000000001-26-000001"):
    f = {"end": end, "val": val, "accn": accn, "form": form, "filed": filed}
    if start:
        f["start"] = start
    return f


def facts_fictifs():
    Q = [("2025-01-01", "2025-03-31"), ("2025-04-01", "2025-06-30"), ("2025-07-01", "2025-09-30")]
    rev_t = [100, 110, 120]  # T4 = 500 - 330 = 170
    ni_t = [10, 12, 14]  # T4 = 60 - 36 = 24
    cfo_cumul = [15, 35, 50]  # T1=15, T2=20, T3=15, T4 = 80 - 50 = 30

    revenus = [
        # 2024 : déclaré sous l'ancienne balise « Revenues » (test de la priorité des balises)
        fait(400, "2024-12-31", "2024-01-01", filed="2025-02-01", accn="a-2024"),
    ]
    rfc = [fait(500, "2025-12-31", "2025-01-01")]
    ni = [
        fait(50, "2024-12-31", "2024-01-01", filed="2025-02-01"),
        fait(48, "2024-12-31", "2024-01-01", filed="2026-02-01"),  # retraité : doit l'emporter
        fait(60, "2025-12-31", "2025-01-01"),
        fait(13, "2024-12-31", "2024-10-01"),  # T4 2024 : sert au ROE trimestriel (un an plus tôt)
    ]
    cfo = [fait(70, "2024-12-31", "2024-01-01", filed="2025-02-01"), fait(80, "2025-12-31", "2025-01-01")]
    eps = [fait(4.0, "2024-12-31", "2024-01-01"), fait(5.0, "2025-12-31", "2025-01-01")]
    cumul_debut = "2025-01-01"
    for i, (s, e) in enumerate(Q):
        filed = f"2025-{(i + 1) * 3 + 1:02d}-30"
        rfc.append(fait(rev_t[i], e, s, form="10-Q", filed=filed))
        rfc.append(fait(sum(rev_t[: i + 1]), e, cumul_debut, form="10-Q", filed=filed))
        ni.append(fait(ni_t[i], e, s, form="10-Q", filed=filed))
        ni.append(fait(sum(ni_t[: i + 1]), e, cumul_debut, form="10-Q", filed=filed))
        cfo.append(fait(cfo_cumul[i], e, cumul_debut, form="10-Q", filed=filed))
        eps.append(fait(1.0 + i / 10, e, s, form="10-Q", filed=filed))

    def stock(valeurs):
        return [fait(v, e, form="10-K" if e.endswith("12-31") else "10-Q") for e, v in valeurs.items()]

    fins = ["2023-12-31", "2024-12-31", "2025-03-31", "2025-06-30", "2025-09-30", "2025-12-31"]
    us_gaap = {
        "Revenues": {"units": {"USD": revenus}},
        "RevenueFromContractWithCustomerExcludingAssessedTax": {"units": {"USD": rfc}},
        "CostOfRevenue": {"units": {"USD": [fait(240, "2024-12-31", "2024-01-01"), fait(300, "2025-12-31", "2025-01-01")]}},
        "OperatingIncomeLoss": {"units": {"USD": [fait(70, "2024-12-31", "2024-01-01"), fait(90, "2025-12-31", "2025-01-01")]}},
        "NetIncomeLoss": {"units": {"USD": ni}},
        "EarningsPerShareDiluted": {"units": {"USD/shares": eps}},
        "NetCashProvidedByUsedInOperatingActivities": {"units": {"USD": cfo}},
        "PaymentsToAcquirePropertyPlantAndEquipment": {"units": {"USD": [fait(20, "2024-12-31", "2024-01-01"), fait(25, "2025-12-31", "2025-01-01")]}},
        "DepreciationDepletionAndAmortization": {"units": {"USD": [fait(10, "2024-12-31", "2024-01-01"), fait(10, "2025-12-31", "2025-01-01")]}},
        "CashAndCashEquivalentsAtCarryingValue": {"units": {"USD": stock(dict(zip(fins, [30, 40, 41, 42, 43, 50])))}},
        "LongTermDebtNoncurrent": {"units": {"USD": stock(dict(zip(fins, [100, 90, 90, 90, 90, 80])))}},
        "CommercialPaper": {"units": {"USD": stock({"2025-12-31": 5})}},
        "StockholdersEquity": {"units": {"USD": stock(dict(zip(fins, [180, 200, 205, 210, 215, 220])))}},
        "AssetsCurrent": {"units": {"USD": stock({"2024-12-31": 150, "2025-12-31": 160})}},
        "LiabilitiesCurrent": {"units": {"USD": stock({"2024-12-31": 100, "2025-12-31": 0})}},
        "Assets": {"units": {"USD": stock({"2024-12-31": 500, "2025-12-31": 560})}},
        "LiabilitiesAndStockholdersEquity": {"units": {"USD": stock({"2024-12-31": 500, "2025-12-31": 560})}},
    }
    return {"cik": 1, "entityName": "Entreprise Fictive Inc.", "facts": {"us-gaap": us_gaap}}


@pytest.fixture
def facts():
    return facts_fictifs()
