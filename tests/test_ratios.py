from datetime import date

import pytest

from suivi.extraction import extraire
from suivi.ratios import RATIOS_PAR_CLE, Contexte, calculer_ratios, formule_excel

D = date.fromisoformat
FIN = D("2025-12-31")


@pytest.fixture
def annuels(facts):
    return calculer_ratios(extraire(facts).annuel, "annuel")


@pytest.fixture
def trimestriels(facts):
    return calculer_ratios(extraire(facts).trimestriel, "trimestriel")


def test_marges(annuels):
    assert annuels.at["marge_brute", FIN] == pytest.approx(200 / 500)
    assert annuels.at["marge_exploitation", FIN] == pytest.approx(90 / 500)
    assert annuels.at["marge_nette", FIN] == pytest.approx(60 / 500)


def test_fcf_et_qualite(annuels):
    assert annuels.at["fcf", FIN] == 80 - 25
    assert annuels.at["marge_fcf", FIN] == pytest.approx(55 / 500)
    assert annuels.at["qualite_benefices", FIN] == pytest.approx(80 / 60)


def test_dette_nette_sur_baiia(annuels):
    assert annuels.at["dette_nette", FIN] == 85 - 50  # pas de placements CT : comptés 0
    assert annuels.at["dette_nette_baiia", FIN] == pytest.approx(35 / (90 + 10))


def test_roe_sur_capitaux_propres_moyens(annuels):
    assert annuels.at["roe", FIN] == pytest.approx(60 / ((220 + 200) / 2))
    # 1re colonne : pas de colonne « un an plus tôt » pour les capitaux propres d'ouverture
    assert annuels.isna().at["roe", D("2024-12-31")]


def test_croissance(annuels):
    assert annuels.at["croissance_revenus", FIN] == pytest.approx(500 / 400 - 1)
    assert annuels.at["croissance_bpa", FIN] == pytest.approx(5 / 4 - 1)


def test_valeur_manquante_et_division_par_zero(annuels):
    assert annuels.isna().at["croissance_revenus", D("2024-12-31")]  # pas d'année précédente
    assert annuels.isna().at["liquidite", FIN]  # passif courant = 0


def test_roe_trimestriel_sur_12_mois(trimestriels):
    # bénéfice des 4 trimestres = 60 ; capitaux propres moyens (220 et 200 un an plus tôt)
    assert trimestriels.at["roe", FIN] == pytest.approx(60 / 210)
    assert trimestriels.isna().at["roe", D("2025-09-30")]  # moins de 4 trimestres disponibles


def test_formule_excel(facts):
    table = extraire(facts).annuel
    ctx = Contexte(table, "annuel")
    adresse = lambda cle, p: f"{cle}@{p.year}"  # noqa: E731
    assert formule_excel(RATIOS_PAR_CLE["marge_nette"], ctx, FIN, adresse) == "=(benefice_net@2025/revenus@2025)"
    assert formule_excel(RATIOS_PAR_CLE["croissance_revenus"], ctx, FIN, adresse) == "=((revenus@2025/revenus@2024)-1)"
    # placements CT absents -> remplacés par 0 dans la formule
    assert "0)" in formule_excel(RATIOS_PAR_CLE["dette_nette"], ctx, FIN, adresse)
    # donnée manquante -> pas de formule
    assert formule_excel(RATIOS_PAR_CLE["croissance_revenus"], ctx, D("2024-12-31"), adresse) is None
