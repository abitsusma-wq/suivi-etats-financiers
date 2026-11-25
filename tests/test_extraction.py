from datetime import date

from suivi.extraction import extraire, libelle_exercice, libelle_trimestre

D = date.fromisoformat


def test_periodes(facts):
    d = extraire(facts)
    assert list(d.annuel.columns) == [D("2024-12-31"), D("2025-12-31")]
    assert list(d.trimestriel.columns) == [D("2024-12-31"), D("2025-03-31"), D("2025-06-30"), D("2025-09-30"), D("2025-12-31")]


def test_priorite_des_balises_par_periode(facts):
    a = extraire(facts).annuel
    assert a.at["revenus", D("2024-12-31")] == 400  # ancienne balise « Revenues »
    assert a.at["revenus", D("2025-12-31")] == 500  # nouvelle balise


def test_valeur_retraitee_la_plus_recente(facts):
    assert extraire(facts).annuel.at["benefice_net", D("2024-12-31")] == 48


def test_trimestres_directs_et_t4_deduit(facts):
    t = extraire(facts).trimestriel.iloc[:, -4:]  # les 4 trimestres de 2025
    assert list(t.loc["revenus"]) == [100, 110, 120, 170]
    assert list(t.loc["benefice_net"]) == [10, 12, 14, 24]


def test_flux_cumules_convertis_en_trimestres(facts):
    t = extraire(facts).trimestriel.iloc[:, -4:]  # les 4 trimestres de 2025
    assert list(t.loc["flux_exploitation"]) == [15, 20, 15, 30]
    assert t.loc["flux_exploitation"].sum() == 80  # = total annuel


def test_bpa_jamais_deduit_par_difference(facts):
    t = extraire(facts).trimestriel.iloc[:, -4:]  # les 4 trimestres de 2025
    assert t.at["bpa_dilue", D("2025-03-31")] == 1.0
    assert t.loc["bpa_dilue"].isna()[D("2025-12-31")]  # pas de T4 inventé


def test_postes_calcules_en_repli(facts):
    a = extraire(facts).annuel
    assert a.at["benefice_brut", D("2025-12-31")] == 200  # 500 - 300
    assert a.at["dette_totale", D("2025-12-31")] == 85  # 80 + 5 (dette CT présente)
    assert a.at["dette_totale", D("2024-12-31")] == 90  # papier commercial absent = 0
    assert a.at["total_passif", D("2025-12-31")] == 340  # 560 - 220


def test_sources_tracees(facts):
    s = extraire(facts).sources
    t4 = s[(s.poste == "flux_exploitation") & (s.type == "trimestriel") & (s.fin == D("2025-12-31"))]
    assert bool(t4.deduite.iloc[0]) is True


def test_nombre_de_periodes_limite(facts):
    d = extraire(facts, annees=1, trimestres=2)
    assert list(d.annuel.columns) == [D("2025-12-31")]
    assert len(d.trimestriel.columns) == 2


def test_libelles():
    fins = [D("2025-09-27"), D("2026-09-26")]  # exercice d'Apple
    assert libelle_exercice(D("2026-09-26")) == "Ex. 2026"
    assert libelle_exercice(D("2026-01-03")) == "Ex. 2025"  # exercice de 52 semaines fini début janvier
    assert libelle_trimestre(D("2025-12-27"), fins) == "T1 2026"
    assert libelle_trimestre(D("2026-06-27"), fins) == "T3 2026"
    assert libelle_trimestre(D("2026-09-26"), fins) == "T4 2026"
    assert libelle_trimestre(D("2026-12-26"), fins) == "T1 2027"  # exercice en cours
    # Costco : 3 trimestres de 12 semaines puis un T4 de 16 semaines
    costco = [D("2025-08-31"), D("2026-08-30")]
    assert [libelle_trimestre(D(x), costco) for x in ("2025-11-23", "2026-02-15", "2026-05-10")] == [
        "T1 2026", "T2 2026", "T3 2026"]


def test_douze_mois_glissants_des_10q_ignores(facts):
    """Amazon déclare dans ses 10-Q des cumuls sur 12 mois glissants : ce ne sont pas des exercices."""
    ni = facts["facts"]["us-gaap"]["NetIncomeLoss"]["units"]["USD"]
    ni.append({"start": "2024-10-01", "end": "2025-09-30", "val": 55, "accn": "q3", "form": "10-Q", "filed": "2025-10-30"})
    d = extraire(facts)
    assert list(d.annuel.columns) == [D("2024-12-31"), D("2025-12-31")]
    assert libelle_trimestre(D("2025-09-30"), d.fins_annuelles_toutes) == "T3 2025"
