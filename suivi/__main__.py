"""Point d'entrée : python -m suivi [--force] [--tickers AAPL MSFT] [--config chemin]

1. Pour chaque entreprise, demande à la SEC la liste de ses dépôts récents.
2. Si un nouveau 10-K ou 10-Q est apparu depuis la dernière exécution (ou avec --force),
   télécharge les données XBRL à jour. Sinon, réutilise celles du cache.
3. Régénère le classeur Excel et les CSV dans donnees/.

Code de sortie : 0 = OK, 1 = erreur (ex. classeur ouvert dans Excel), 2 = configuration invalide.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime

import pandas as pd

from .config import RACINE, charger_config
from .etat import charger_etat, sauver_etat
from .excel import Entreprise, ecrire_classeur
from .extraction import extraire
from .ratios import calculer_ratios
from .sec import ClientSEC


def _log(msg: str) -> None:
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}", flush=True)


def executer(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m suivi", description=__doc__.splitlines()[0])
    parser.add_argument("--force", action="store_true", help="retélécharge les données même sans nouveau dépôt")
    parser.add_argument("--tickers", nargs="+", help="limite la mise à jour à ces tickers")
    parser.add_argument("--config", default=str(RACINE / "config.yaml"))
    args = parser.parse_args(argv)

    try:
        cfg = charger_config(args.config)
    except (ValueError, FileNotFoundError) as e:
        _log(f"Configuration invalide : {e}")
        return 2

    client = ClientSEC(cfg.user_agent, cfg.dossier_cache)
    etat = charger_etat(cfg.fichier_etat)
    cibles = {t.upper() for t in args.tickers} if args.tickers else None
    entreprises: list[Entreprise] = []
    nouveautes: list[dict] = []
    traites: dict[str, dict] = {}
    erreurs = 0

    for e in cfg.entreprises:
        t = e.ticker
        memo = etat["entreprises"].get(t, {})
        try:
            cik = e.cik or memo.get("cik") or client.cik_pour(t)
            depots = client.derniers_depots(cik)
            dernier = depots[0] if depots else None
            cache_present = (cfg.dossier_cache / f"facts_CIK{cik:010d}.json").exists()
            nouveau = dernier is not None and dernier.accession != memo.get("derniere_accession")
            a_jour = (cibles is None or t in cibles) and (args.force or nouveau or not cache_present)

            facts = client.company_facts(cik, rafraichir=a_jour)
            if a_jour:
                _log(f"{t} : données XBRL téléchargées" + (f" (nouveau {dernier.formulaire} du {dernier.date_depot})" if nouveau else ""))
            else:
                _log(f"{t} : aucun nouveau dépôt (dernier : {dernier.formulaire if dernier else '?'} du {dernier.date_depot if dernier else '?'})")

            # La SEC met parfois quelques heures à intégrer un dépôt dans l'API XBRL.
            # Si le dernier dépôt n'y est pas encore, on ne le marque pas comme traité :
            # il sera retenté à la prochaine exécution.
            integre = dernier is None or _depot_dans_facts(facts, dernier.accession)
            if nouveau and not integre:
                _log(f"{t} : le {dernier.formulaire} du {dernier.date_depot} n'est pas encore dans l'API XBRL, nouvel essai au prochain passage.")

            donnees = extraire(facts, cfg.annees, cfg.trimestres)
            ent = Entreprise(
                ticker=t, cik=cik, donnees=donnees, dernier_depot=dernier,
                ratios_annuels=calculer_ratios(donnees.annuel, "annuel"),
                ratios_trimestriels=calculer_ratios(donnees.trimestriel, "trimestriel"),
            )
            entreprises.append(ent)
            _sauver_csv(cfg, ent)

            if integre and dernier is not None:
                traites[t] = {"cik": cik, "derniere_accession": dernier.accession, "date_depot": dernier.date_depot}
                if nouveau and memo:  # pas de « nouveauté » au tout premier passage
                    nouveautes.append({
                        "detecte_le": f"{datetime.now():%Y-%m-%d %H:%M}", "ticker": t,
                        "formulaire": dernier.formulaire, "periode": dernier.date_periode,
                        "date_depot": dernier.date_depot, "url": dernier.url,
                    })
            else:
                traites[t] = {**memo, "cik": cik}
        except Exception as exc:  # une entreprise en erreur ne bloque pas les autres
            erreurs += 1
            _log(f"{t} : ERREUR {type(exc).__name__}: {exc}")

    if not entreprises:
        _log("Aucune entreprise traitée.")
        return 1

    journal = etat["journal"] + nouveautes
    try:
        chemin = ecrire_classeur(cfg.fichier_excel, entreprises, journal, cfg.unite)
    except PermissionError:
        _log(f"Impossible d'écrire {cfg.fichier_excel} : ferme le fichier dans Excel puis relance. "
             "Les nouveaux dépôts seront retraités au prochain passage.")
        return 1

    etat["entreprises"].update(traites)
    etat["journal"] = journal
    sauver_etat(cfg.fichier_etat, etat)

    for n in nouveautes:
        _log(f"NOUVEAU : {n['ticker']} {n['formulaire']} (période {n['periode']}) {n['url']}")
    _log(f"Classeur mis à jour : {chemin}")
    return 1 if erreurs else 0


def _depot_dans_facts(facts: dict, accession: str) -> bool:
    for balise in ("NetIncomeLoss", "ProfitLoss", "Assets"):
        for faits in facts.get("facts", {}).get("us-gaap", {}).get(balise, {}).get("units", {}).values():
            if any(f.get("accn") == accession for f in faits):
                return True
    return False


def _sauver_csv(cfg, ent: Entreprise) -> None:
    """Données en format long, pratiques pour pandas : une ligne par (poste, période)."""
    cfg.dossier_donnees.mkdir(parents=True, exist_ok=True)
    sources = ent.donnees.sources.copy()
    sources.insert(0, "ticker", ent.ticker)
    sources.to_csv(cfg.dossier_donnees / f"{ent.ticker}_etats.csv", index=False, encoding="utf-8-sig")
    lignes = []
    for mode, table in (("annuel", ent.ratios_annuels), ("trimestriel", ent.ratios_trimestriels)):
        long = table.rename_axis("ratio").reset_index().melt(id_vars="ratio", var_name="fin", value_name="valeur")
        long.insert(1, "type", mode)
        lignes.append(long.dropna(subset=["valeur"]))


    ratios = pd.concat(lignes, ignore_index=True)
    ratios.insert(0, "ticker", ent.ticker)
    ratios.to_csv(cfg.dossier_donnees / f"{ent.ticker}_ratios.csv", index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    sys.exit(executer())
