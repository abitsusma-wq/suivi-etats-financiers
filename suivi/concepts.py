"""Correspondance entre les postes des états financiers et les balises XBRL (taxonomie us-gaap).

Chaque entreprise choisit ses balises : Apple utilise « Revenues » jusqu'en 2018, puis
« RevenueFromContractWithCustomerExcludingAssessedTax ». On donne donc pour chaque poste une
liste de balises par ordre de priorité : pour chaque période, la première balise qui a une
valeur l'emporte.

Pour ajouter un poste : ajoute une `Ligne` dans la bonne liste. Pour trouver le nom d'une
balise, cherche le poste dans le rapport sur https://www.sec.gov/edgar/search/ et ouvre
l'onglet « Financial Report » (R2.htm, R4.htm...), ou explore le fichier cache/facts_*.json.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Ligne:
    cle: str
    libelle: str
    balises: tuple[str, ...] = ()
    nature: str = "flux"  # "flux" = sur une période (résultats, flux) ; "stock" = à une date (bilan)
    unite: str = "USD"  # "USD", "USD/shares" (par action) ou "shares" (nombre d'actions)
    additif: bool = True  # peut-on additionner/soustraire des périodes ? (faux pour le BPA)
    calcul: tuple[str, ...] = field(default=())  # postes servant au calcul de repli (voir extraction)


RESULTATS = [
    Ligne("revenus", "Revenus (chiffre d'affaires)", (
        "Revenues",
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "RevenueFromContractWithCustomerIncludingAssessedTax",
        "SalesRevenueNet",
        "SalesRevenueGoodsNet",
    )),
    Ligne("cout_ventes", "Coût des ventes", (
        "CostOfGoodsAndServicesSold",
        "CostOfRevenue",
        "CostOfGoodsSold",
        "CostOfGoodsAndServiceExcludingDepreciationDepletionAndAmortization",
    )),
    Ligne("benefice_brut", "Bénéfice brut", ("GrossProfit",), calcul=("revenus", "-", "cout_ventes")),
    Ligne("rd", "Recherche et développement", ("ResearchAndDevelopmentExpense",)),
    Ligne("sga", "Frais de vente et d'administration", ("SellingGeneralAndAdministrativeExpense",)),
    Ligne("resultat_exploitation", "Résultat d'exploitation (BAII)", ("OperatingIncomeLoss",)),
    Ligne("charges_interets", "Charges d'intérêts", (
        "InterestExpense",
        "InterestExpenseNonoperating",
        "InterestExpenseDebt",
    )),
    Ligne("benefice_avant_impots", "Bénéfice avant impôts", (
        "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
        "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments",
    )),
    Ligne("impots", "Impôts sur le résultat", ("IncomeTaxExpenseBenefit",)),
    Ligne("benefice_net", "Bénéfice net", (
        "NetIncomeLoss",
        "ProfitLoss",
        "NetIncomeLossAvailableToCommonStockholdersBasic",
    )),
    Ligne("bpa_dilue", "BPA dilué ($ par action)", (
        "EarningsPerShareDiluted",
        "EarningsPerShareBasicAndDiluted",
    ), unite="USD/shares", additif=False),
    Ligne("actions_diluees", "Actions diluées (moyenne, millions)", (
        "WeightedAverageNumberOfDilutedSharesOutstanding",
    ), unite="shares", additif=False),
]

BILAN = [
    Ligne("tresorerie", "Trésorerie et équivalents", (
        "CashAndCashEquivalentsAtCarryingValue",
        "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents",
        "Cash",
    ), nature="stock"),
    Ligne("placements_ct", "Placements à court terme", (
        "MarketableSecuritiesCurrent",
        "ShortTermInvestments",
        "AvailableForSaleSecuritiesDebtSecuritiesCurrent",
    ), nature="stock"),
    Ligne("comptes_clients", "Comptes clients", ("AccountsReceivableNetCurrent",), nature="stock"),
    Ligne("stocks", "Stocks (inventaires)", ("InventoryNet",), nature="stock"),
    Ligne("actif_courant", "Total de l'actif courant", ("AssetsCurrent",), nature="stock"),
    Ligne("immobilisations", "Immobilisations corporelles nettes", ("PropertyPlantAndEquipmentNet",), nature="stock"),
    Ligne("goodwill", "Écart d'acquisition (goodwill)", ("Goodwill",), nature="stock"),
    Ligne("total_actif", "Total de l'actif", ("Assets",), nature="stock"),
    Ligne("fournisseurs", "Comptes fournisseurs", ("AccountsPayableCurrent",), nature="stock"),
    Ligne("passif_courant", "Total du passif courant", ("LiabilitiesCurrent",), nature="stock"),
    Ligne("dette_ct", "Emprunts à court terme (papier commercial)", (
        "CommercialPaper",
        "ShortTermBorrowings",
    ), nature="stock"),
    Ligne("dette_lt_courante", "Dette à long terme échéant dans l'année", (
        "LongTermDebtCurrent",
        "LongTermDebtAndCapitalLeaseObligationsCurrent",
    ), nature="stock"),
    Ligne("dette_lt", "Dette à long terme", (
        "LongTermDebtNoncurrent",
        "LongTermDebtAndCapitalLeaseObligations",
    ), nature="stock"),
    Ligne("dette_totale", "Dette financière totale (hors loyers)", (),
          nature="stock", calcul=("dette_ct", "+", "dette_lt_courante", "+", "dette_lt")),
    Ligne("total_passif", "Total du passif", ("Liabilities",),
          nature="stock", calcul=("passif_et_cp", "-", "capitaux_propres_totaux")),
    Ligne("capitaux_propres", "Capitaux propres (actionnaires)", ("StockholdersEquity",), nature="stock"),
    Ligne("capitaux_propres_totaux", "Capitaux propres (y c. participations ne donnant pas le contrôle)", (
        "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
        "StockholdersEquity",
    ), nature="stock"),
    Ligne("passif_et_cp", "Total du passif et des capitaux propres", ("LiabilitiesAndStockholdersEquity",), nature="stock"),
]

FLUX = [
    Ligne("amortissements", "Amortissements", (
        "DepreciationDepletionAndAmortization",
        "DepreciationAmortizationAndAccretionNet",
        "DepreciationAndAmortization",
        "Depreciation",
    )),
    Ligne("remuneration_actions", "Rémunération à base d'actions", (
        "ShareBasedCompensation",
        "AllocatedShareBasedCompensationExpense",
    )),
    Ligne("flux_exploitation", "Flux de trésorerie liés à l'exploitation", (
        "NetCashProvidedByUsedInOperatingActivities",
        "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations",
    )),
    Ligne("capex", "Acquisitions d'immobilisations (capex, sortie)", (
        "PaymentsToAcquirePropertyPlantAndEquipment",
        "PaymentsToAcquireProductiveAssets",
    )),
    Ligne("flux_investissement", "Flux de trésorerie liés à l'investissement", (
        "NetCashProvidedByUsedInInvestingActivities",
        "NetCashProvidedByUsedInInvestingActivitiesContinuingOperations",
    )),
    Ligne("dividendes", "Dividendes versés (sortie)", (
        "PaymentsOfDividends",
        "PaymentsOfDividendsCommonStock",
    )),
    Ligne("rachats", "Rachats d'actions (sortie)", ("PaymentsForRepurchaseOfCommonStock",)),
    Ligne("flux_financement", "Flux de trésorerie liés au financement", (
        "NetCashProvidedByUsedInFinancingActivities",
        "NetCashProvidedByUsedInFinancingActivitiesContinuingOperations",
    )),
]

ETATS = {
    "Résultats": RESULTATS,
    "Bilan": BILAN,
    "Flux": FLUX,
}

TITRES_ETATS = {
    "Résultats": "État des résultats",
    "Bilan": "Bilan",
    "Flux": "Tableau des flux de trésorerie",
}

TOUTES_LES_LIGNES = {l.cle: l for lignes in ETATS.values() for l in lignes}
