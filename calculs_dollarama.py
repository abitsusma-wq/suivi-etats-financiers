"""Ratios Dollarama, exercice 2026 (clos le 1er fevrier 2026) vs exercice 2025.
Source : etats financiers consolides audites et rapport de gestion du 24 mars 2026.
Montants en milliers de $ CA (convertis en M$ a l'affichage).
"""

# ---------- Etat des resultats ----------
I = {
    2026: dict(ventes=7_255_754, cout_ventes=3_987_089, marge_brute=3_268_665, frais_vga=1_093_289,
               amort=429_053, amort_dans_cout=30_966, quote_part_mev=191_536, res_exploit=1_937_859,
               gain_non_realise=10_348, frais_fin=184_020, bai=1_764_187, impots=454_749,
               benef_net=1_309_438, bpa_dilue=4.73, actions_moy=275_611, actions_moy_dil=276_684,
               baiia_societe=2_408_226),
    2025: dict(ventes=6_413_145, cout_ventes=3_519_399, marge_brute=2_893_746, frais_vga=930_168,
               amort=382_805, amort_dans_cout=28_346, quote_part_mev=129_905, res_exploit=1_710_678,
               gain_non_realise=0, frais_fin=163_782, bai=1_546_896, impots=378_351,
               benef_net=1_168_545, bpa_dilue=4.16, actions_moy=279_825, actions_moy_dil=280_819,
               baiia_societe=2_121_829),
    2024: dict(ventes=5_867_348, benef_net=1_010_460, bpa_dilue=3.56, res_exploit=1_495_721),
}
# Charges d'interets brutes (note 20)
interets = {2026: dict(dette=92_531, baux=99_087, court_terme=12_500, autres=5_572, revenus=-25_670),
            2025: dict(dette=87_489, baux=86_730, court_terme=13_235, autres=4_801, revenus=-28_473)}

# ---------- Bilan ----------
B = {
    2026: dict(encaisse=331_569, clients=38_500, impots_recev=559, distrib_recev=0, frais_payes=38_452,
               stocks=1_103_175, deriv=9_734, actif_court=1_521_989, droits_utilisation=2_397_209,
               immo=1_258_499, incorporels=178_281, goodwill=801_709, mev=1_285_105, actif=7_558_352,
               fournisseurs=461_766, passif_court=1_348_179, dette_ct=398_275, baux_ct=377_743,
               dette_lt=2_226_846, baux_lt=2_392_730, passif=6_102_464, bnr=128_858,
               capitaux_propres=1_455_888, actions_fin=272_929_382),
    2025: dict(encaisse=122_685, clients=46_638, stocks=921_095, actif_court=1_201_280,
               droits_utilisation=2_109_445, immo=1_046_390, incorporels=180_689, goodwill=727_782,
               actif=6_482_592, fournisseurs=354_900, passif_court=1_014_306, dette_ct=273_771,
               baux_ct=278_705, dette_lt=2_008_908, baux_lt=2_148_272, passif=5_294_334,
               bnr=-225_301, capitaux_propres=1_188_258, actions_fin=277_177_329),
    2024: dict(encaisse=313_915, stocks=916_812, actif=5_263_607, capitaux_propres=380_848),
}

# ---------- Flux de tresorerie ----------
F = {
    2026: dict(benef_net=1_309_438, amort_total=460_019, remu_actions=16_023, frais_fin=184_020,
               impots_diff=-8_834, gain_non_realise=-10_348, quote_part_mev=-191_536,
               interets_recus=25_562, autres=32_686, var_bfr=-55_874, fte=1_761_156,
               acquisition=-181_831, invest_mev=-49_960, distrib_mev=106_554, capex_immo=-248_747,
               capex_incorp=-24_034, couts_baux=-6_554, cessions=1_077, invest=-403_495,
               emission_dette=600_000, rembours_dette=-250_000, interets_payes=-114_516,
               frais_emission=-3_584, paiements_baux=-390_333, emission_actions=8_840,
               dividendes=-113_196, rachats=-854_414, actions_tresor=-9_970, uad=-21_604,
               financement=-1_148_777, var_encaisse=208_884, interets_baux_payes=99_087,
               impots_payes=468_891),
    2025: dict(benef_net=1_168_545, amort_total=411_151, var_bfr=-6_752, fte=1_644_139,
               capex_immo=-212_828, capex_incorp=-30_622, invest=-220_719, interets_payes=-108_490,
               paiements_baux=-317_829, dividendes=-97_244, rachats=-1_070_712, actions_tresor=-20_000,
               financement=-1_614_650, var_encaisse=-191_230, interets_baux_payes=86_730),
}
# Detail de la variation du BFR (note 22a), exercice 2026
bfr_detail = dict(clients=-255, frais_payes=-21_931, stocks=-54_278, fournisseurs=37_855, impots=-17_265)
stocks_acquis_TRS = 127_801   # note 6 : stocks recus avec The Reject Shop (21 juillet 2025)
cout_ventes_australie = 288_321  # 22 juillet 2025 au 1er fevrier 2026 seulement
cours_approx = 195.0   # $/action fin janvier 2026, approximatif (196 a mi-janvier, 192 debut fevrier)

M = lambda x: x / 1000  # milliers -> millions
pct = lambda x: f"{100 * x:.1f} %"
moy = lambda a, b: (a + b) / 2
out = []
def p(label, val):
    out.append(f"{label:<62} {val}")

out.append("=== 1. ETAT DES RESULTATS ===")
for y in (2026, 2025):
    i = I[y]
    p(f"[{y}] Croissance des ventes", pct(i['ventes'] / I[y - 1]['ventes'] - 1))
    p(f"[{y}] Marge brute", pct(i['marge_brute'] / i['ventes']))
    p(f"[{y}] Frais VGA / ventes", pct(i['frais_vga'] / i['ventes']))
    baiia = i['res_exploit'] + i['amort'] + i['amort_dans_cout']
    p(f"[{y}] BAIIA recalcule (res. exploit. + tous amort.) M$", f"{M(baiia):,.1f}")
    p(f"[{y}] BAIIA publie par la societe M$", f"{M(i['baiia_societe']):,.1f}")
    p(f"[{y}] Marge BAIIA (publiee)", pct(i['baiia_societe'] / i['ventes']))
    p(f"[{y}] Marge d'exploitation", pct(i['res_exploit'] / i['ventes']))
    p(f"[{y}] Marge nette", pct(i['benef_net'] / i['ventes']))
    p(f"[{y}] Taux d'impot effectif", pct(i['impots'] / i['bai']))
    p(f"[{y}] Quote-part Dollarcity / resultat d'exploitation", pct(i['quote_part_mev'] / i['res_exploit']))
    p(f"[{y}] Croissance benefice net", pct(i['benef_net'] / I[y - 1]['benef_net'] - 1))
    p(f"[{y}] Croissance BPA dilue", pct(i['bpa_dilue'] / I[y - 1]['bpa_dilue'] - 1))
    p(f"[{y}] Variation du nb moyen d'actions diluees",
      pct(i['actions_moy_dil'] / I[y - 1].get('actions_moy_dil', 284_168) - 1))
    out.append("")

out.append("=== 2. FLUX DE TRESORERIE ===")
f, i = F[2026], I[2026]
out.append("Pont benefice net -> flux d'exploitation 2026 (M$) :")
for k in ('benef_net', 'amort_total', 'remu_actions', 'frais_fin', 'impots_diff', 'gain_non_realise',
          'quote_part_mev', 'interets_recus', 'autres', 'var_bfr'):
    out.append(f"   {k:<20} {M(f[k]):>9,.1f}")
somme = sum(f[k] for k in ('benef_net', 'amort_total', 'remu_actions', 'frais_fin', 'impots_diff',
                           'gain_non_realise', 'quote_part_mev', 'interets_recus', 'autres', 'var_bfr'))
out.append(f"   {'= FTE (verif.)':<20} {M(somme):>9,.1f}  (publie : {M(f['fte']):,.1f})")
out.append("Detail variation BFR 2026 (M$) : " + ", ".join(f"{k} {M(v):,.1f}" for k, v in bfr_detail.items()))
for y in (2026, 2025):
    f = F[y]
    capex = -(f['capex_immo'] + f['capex_incorp'])
    fcf_simple = f['fte'] - capex
    fcf_ajuste = f['fte'] - capex + f['paiements_baux'] + f['interets_payes']
    p(f"[{y}] Flux d'exploitation (FTE) M$", f"{M(f['fte']):,.1f}")
    p(f"[{y}] Conversion FTE / benefice net", f"{f['fte'] / f['benef_net']:.2f}x")
    fte_apres_int = f['fte'] + f['interets_payes'] - f['interets_baux_payes']
    p(f"[{y}] FTE apres TOUS les interets payes M$", f"{M(fte_apres_int):,.1f}")
    p(f"[{y}] Conversion (FTE apres interets) / benefice net", f"{fte_apres_int / f['benef_net']:.2f}x")
    p(f"[{y}] Capex (immo + incorporels) M$", f"{M(capex):,.1f}")
    p(f"[{y}] Capex / ventes", pct(capex / I[y]['ventes']))
    p(f"[{y}] Capex / amortissement total", f"{capex / f['amort_total']:.2f}x")
    p(f"[{y}] FCF simple (FTE - capex) M$", f"{M(fcf_simple):,.1f}")
    p(f"[{y}] Paiements de baux (capital + interets) M$", f"{M(-f['paiements_baux']):,.1f}")
    p(f"[{y}]   dont interets sur baux M$", f"{M(f['interets_baux_payes']):,.1f}")
    p(f"[{y}] Interets payes sur la dette M$", f"{M(-f['interets_payes']):,.1f}")
    p(f"[{y}] FCF ajuste (- baux - interets dette) M$", f"{M(fcf_ajuste):,.1f}")
    p(f"[{y}] FCF ajuste / benefice net", f"{fcf_ajuste / f['benef_net']:.2f}x")
    p(f"[{y}] FCF ajuste / ventes", pct(fcf_ajuste / I[y]['ventes']))
    retour = -(f['dividendes'] + f['rachats'] + f['actions_tresor'])
    p(f"[{y}] Dividendes + rachats M$", f"{M(retour):,.1f}")
    p(f"[{y}] (Dividendes + rachats) / FCF ajuste", pct(retour / fcf_ajuste))
    p(f"[{y}] Ratio de distribution des dividendes (div / BN)", pct(-f['dividendes'] / f['benef_net']))
    out.append("")
f = F[2026]
ar = (I[2026]['benef_net'] - f['fte']) / moy(B[2026]['actif'], B[2025]['actif'])
p("[2026] Ratio d'accruals de Sloan (BN - FTE) / actif moyen", pct(ar))
p("[2026] Quote-part Dollarcity (comptable) M$", f"{M(I[2026]['quote_part_mev']):,.1f}")
p("[2026] Distributions recues de Dollarcity (cash) M$", f"{M(f['distrib_mev']):,.1f}")
p("[2026] Pont encaisse : 122,7 + variation = fin", f"{M(B[2025]['encaisse'] + f['var_encaisse']):,.1f}")
out.append("")

out.append("=== 3. BILAN : FONDS DE ROULEMENT ===")
for y in (2026, 2025):
    b, i = B[y], I[y]
    stocks_moy = moy(b['stocks'], B[y - 1]['stocks'])
    p(f"[{y}] Jours de stocks DIO (stock moyen / cout des ventes x 365)",
      f"{stocks_moy / i['cout_ventes'] * 365:.0f} j")
    p(f"[{y}] Jours de stocks DIO (stock de fin)", f"{b['stocks'] / i['cout_ventes'] * 365:.0f} j")
    p(f"[{y}] Rotation des stocks (cout des ventes / stock moyen)", f"{i['cout_ventes'] / stocks_moy:.1f}x")
    if y == 2026:
        dso = moy(b['clients'], B[2025]['clients']) / i['ventes'] * 365
        dpo = moy(b['fournisseurs'], B[2025]['fournisseurs']) / i['cout_ventes'] * 365
        dio = stocks_moy / i['cout_ventes'] * 365
        p("[2026] Jours de comptes clients DSO", f"{dso:.1f} j")
        p("[2026] Jours fournisseurs DPO (inclut charges a payer)", f"{dpo:.0f} j")
        p("[2026] Cycle de conversion de tresorerie (DIO + DSO - DPO)", f"{dio + dso - dpo:.0f} j")
        p("[2026] Hausse des stocks au bilan", pct(b['stocks'] / B[2025]['stocks'] - 1))
        organique = b['stocks'] - stocks_acquis_TRS - B[2025]['stocks']
        p("[2026] Hausse des stocks hors The Reject Shop M$", f"{M(organique):,.1f}")
        p("[2026] Hausse des stocks hors The Reject Shop (%)", pct(organique / B[2025]['stocks']))
        p("[2026] Croissance des ventes (rappel)", pct(i['ventes'] / I[2025]['ventes'] - 1))
        cout_pf = i['cout_ventes'] + cout_ventes_australie / (196 / 364) * (1 - 196 / 364)
        p("[2026] DIO fin d'annee, cout des ventes Australie annualise (approx.)",
          f"{b['stocks'] / cout_pf * 365:.0f} j")
out.append("")

out.append("=== 4. BILAN : LIQUIDITE, DETTE, BAUX ===")
for y in (2026, 2025):
    b, i, f = B[y], I[y], F[y]
    p(f"[{y}] Ratio de liquidite generale (actif CT / passif CT)", f"{b['actif_court'] / b['passif_court']:.2f}")
    p(f"[{y}] Ratio de liquidite immediate ((encaisse+clients)/passif CT)",
      f"{(b['encaisse'] + b['clients']) / b['passif_court']:.2f}")
    dette = b['dette_ct'] + b['dette_lt']
    baux = b['baux_ct'] + b['baux_lt']
    dette_nette = dette - b['encaisse']
    baiia = i['baiia_societe']
    p(f"[{y}] Dette totale M$", f"{M(dette):,.1f}")
    p(f"[{y}] Dette nette M$", f"{M(dette_nette):,.1f}")
    p(f"[{y}] Obligations locatives M$", f"{M(baux):,.1f}")
    p(f"[{y}] Dette nette / BAIIA (sans baux, BAIIA IFRS 16 : a eviter)", f"{dette_nette / baiia:.2f}x")
    baiia_pre16 = baiia + f['paiements_baux']   # BAIIA apres loyers payes
    p(f"[{y}] BAIIA apres loyers (BAIIA - paiements de baux) M$", f"{M(baiia_pre16):,.1f}")
    p(f"[{y}] Dette nette / BAIIA apres loyers (coherent)", f"{dette_nette / baiia_pre16:.2f}x")
    p(f"[{y}] (Dette nette + baux) / BAIIA IFRS 16 (coherent)", f"{(dette_nette + baux) / baiia:.2f}x")
    int_brut = sum(v for k, v in interets[y].items() if k != 'revenus')
    p(f"[{y}] Couverture des interets : res. exploit. / frais fin. nets",
      f"{i['res_exploit'] / i['frais_fin']:.1f}x")
    p(f"[{y}] Couverture : (res. exploit. - quote-part Dollarcity) / frais fin. bruts",
      f"{(i['res_exploit'] - i['quote_part_mev']) / int_brut:.1f}x")
    p(f"[{y}] Dette totale / capitaux propres", f"{dette / b['capitaux_propres']:.2f}x")
    p(f"[{y}] (Dette + baux) / capitaux propres", f"{(dette + baux) / b['capitaux_propres']:.2f}x")
    p(f"[{y}] Goodwill / capitaux propres", pct(b['goodwill'] / b['capitaux_propres']))
    p(f"[{y}] Goodwill / actif total", pct(b['goodwill'] / b['actif']))
    p(f"[{y}] Capitaux propres tangibles (CP - goodwill - incorporels) M$",
      f"{M(b['capitaux_propres'] - b['goodwill'] - b['incorporels']):,.1f}")
    p(f"[{y}] Droits d'utilisation / actif total", pct(b['droits_utilisation'] / b['actif']))
    out.append("")

out.append("=== 5. RENTABILITE, ROE ET RACHATS ===")
b, b0, i = B[2026], B[2025], I[2026]
cp_moy = moy(b['capitaux_propres'], b0['capitaux_propres'])
actif_moy = moy(b['actif'], b0['actif'])
p("[2026] ROE (BN / CP moyens)", pct(i['benef_net'] / cp_moy))
p("[2026] ROA (BN / actif moyen)", pct(i['benef_net'] / actif_moy))
p("[2026] DuPont : marge nette", pct(i['benef_net'] / i['ventes']))
p("[2026] DuPont : rotation de l'actif (ventes / actif moyen)", f"{i['ventes'] / actif_moy:.2f}x")
p("[2026] DuPont : levier (actif moyen / CP moyens)", f"{actif_moy / cp_moy:.2f}x")
t = i['impots'] / i['bai']
cap_investi = b['capitaux_propres'] + b['dette_ct'] + b['dette_lt'] + b['baux_ct'] + b['baux_lt'] - b['encaisse']
p("[2026] ROIC approx. (res. exploit. x (1-t) / capital investi fin)", pct(i['res_exploit'] * (1 - t) / cap_investi))
cp_sans_rachats = b['capitaux_propres'] + 8_027_091   # prime payee sur rachats depuis 2012 (rapport de gestion)
p("[2026] ROE illustratif si on rajoutait la prime des rachats depuis 2012",
  pct(i['benef_net'] / cp_sans_rachats))
p("[2026] Actions en circulation fin d'annee : variation", pct(b['actions_fin'] / b0['actions_fin'] - 1))
p("[2026] Prix moyen paye par action rachetee", f"{850_237 / 4_426.267:.2f} $")
cap_boursiere = b['actions_fin'] * cours_approx / 1000
p("[2026] Capitalisation boursiere approx. (cours ~195 $) M$", f"{M(cap_boursiere):,.0f}")
p("[2026] Ratio cours / valeur comptable approx.", f"{cap_boursiere / b['capitaux_propres']:.0f}x")
p("[2026] Remuneration en actions / ventes", pct(F[2026]['remu_actions'] / i['ventes']))
p("[2026] Ecart actions diluees vs de base", pct(i['actions_moy_dil'] / i['actions_moy'] - 1))
out.append("")

out.append("=== 6. PIOTROSKI F-SCORE 2026 (vs 2025) ===")
roa26 = I[2026]['benef_net'] / B[2025]['actif']
roa25 = I[2025]['benef_net'] / B[2024]['actif']
lev26 = B[2026]['dette_lt'] / moy(B[2026]['actif'], B[2025]['actif'])
lev25 = B[2025]['dette_lt'] / moy(B[2025]['actif'], B[2024]['actif'])
cr26 = B[2026]['actif_court'] / B[2026]['passif_court']
cr25 = B[2025]['actif_court'] / B[2025]['passif_court']
gm26 = I[2026]['marge_brute'] / I[2026]['ventes']
gm25 = I[2025]['marge_brute'] / I[2025]['ventes']
at26 = I[2026]['ventes'] / B[2025]['actif']
at25 = I[2025]['ventes'] / B[2024]['actif']
crit = [
    ("1. Benefice net > 0", I[2026]['benef_net'] > 0, f"{M(I[2026]['benef_net']):,.0f} M$"),
    ("2. FTE > 0", F[2026]['fte'] > 0, f"{M(F[2026]['fte']):,.0f} M$"),
    ("3. ROA en hausse", roa26 > roa25, f"{pct(roa26)} vs {pct(roa25)}"),
    ("4. FTE > benefice net (accruals)", F[2026]['fte'] > I[2026]['benef_net'], "1 761 vs 1 309"),
    ("5. Dette LT / actif en baisse", lev26 < lev25, f"{pct(lev26)} vs {pct(lev25)}"),
    ("6. Ratio de liquidite en hausse", cr26 > cr25, f"{cr26:.2f} vs {cr25:.2f}"),
    ("7. Pas d'emission nette d'actions", B[2026]['actions_fin'] <= B[2025]['actions_fin'], "-1,5 % d'actions"),
    ("8. Marge brute en hausse", gm26 > gm25, f"{pct(gm26)} vs {pct(gm25)}"),
    ("9. Rotation de l'actif en hausse", at26 > at25, f"{at26:.3f} vs {at25:.3f}"),
]
for nom, ok, detail in crit:
    p(f"   {nom}", f"{'1' if ok else '0'}  ({detail})")
p("   F-Score", f"{sum(ok for _, ok, _ in crit)} / 9")
out.append("")

out.append("=== 7. ALTMAN Z-SCORE 2026 ===")
b, i = B[2026], I[2026]
x1 = (b['actif_court'] - b['passif_court']) / b['actif']
x2 = b['bnr'] / b['actif']
x3 = i['res_exploit'] / b['actif']
x4_marche = cap_boursiere / b['passif']
x4_compta = b['capitaux_propres'] / b['passif']
x5 = i['ventes'] / b['actif']
p("   X1 fonds de roulement / actif", f"{x1:.3f}")
p("   X2 benefices non repartis / actif", f"{x2:.3f}")
p("   X3 BAII / actif", f"{x3:.3f}")
p("   X4 cap. boursiere / passif total", f"{x4_marche:.2f}")
p("   X4'' valeur comptable CP / passif total", f"{x4_compta:.3f}")
p("   X5 ventes / actif", f"{x5:.3f}")
z = 1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4_marche + 1.0 * x5
z2 = 6.56 * x1 + 3.26 * x2 + 6.72 * x3 + 1.05 * x4_compta
p("   Z original (1968, manufacturieres cotees)", f"{z:.2f}  (>2,99 sur ; <1,81 detresse)")
p("   Z'' (non manufacturieres, valeur comptable)", f"{z2:.2f}  (>2,60 sur ; <1,10 detresse)")
p("   Part de X4 (cap. boursiere) dans le Z original", pct(0.6 * x4_marche / z))

print("\n".join(out))
