"""Accès aux API gratuites de la SEC (EDGAR).

- https://www.sec.gov/files/company_tickers.json : correspondance ticker -> CIK
- https://data.sec.gov/submissions/CIK##########.json : liste des dépôts (10-K, 10-Q...)
- https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json : toutes les données XBRL

Règles de la SEC : User-Agent identifiant le client, et au plus 10 requêtes par seconde.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path

import requests

URL_TICKERS = "https://www.sec.gov/files/company_tickers.json"
URL_SUBMISSIONS = "https://data.sec.gov/submissions/CIK{cik:010d}.json"
URL_FACTS = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
URL_DEPOT = "https://www.sec.gov/Archives/edgar/data/{cik}/{accn_sans_tirets}/{document}"

FORMULAIRES_SUIVIS = ("10-K", "10-Q", "10-K/A", "10-Q/A")
DELAI_ENTRE_REQUETES = 0.15  # secondes, reste bien sous la limite de 10 requêtes/s
DUREE_CACHE_TICKERS = 7 * 24 * 3600  # la liste des tickers change peu


@dataclass
class Depot:
    """Un dépôt 10-K ou 10-Q."""

    formulaire: str
    accession: str
    date_depot: str
    date_periode: str
    document: str
    cik: int

    @property
    def url(self) -> str:
        return URL_DEPOT.format(
            cik=self.cik, accn_sans_tirets=self.accession.replace("-", ""), document=self.document
        )


class ClientSEC:
    def __init__(self, user_agent: str, dossier_cache: Path):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent, "Accept-Encoding": "gzip, deflate"})
        self.dossier_cache = Path(dossier_cache)
        self.dossier_cache.mkdir(parents=True, exist_ok=True)
        self._derniere_requete = 0.0

    # --- bas niveau -------------------------------------------------------
    def _get_json(self, url: str) -> dict:
        attente = DELAI_ENTRE_REQUETES - (time.monotonic() - self._derniere_requete)
        if attente > 0:
            time.sleep(attente)
        for essai in range(3):
            self._derniere_requete = time.monotonic()
            r = self.session.get(url, timeout=60)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (429, 503) or (r.status_code == 403 and essai < 2):
                time.sleep(2 * (essai + 1))  # la SEC limite le débit : on patiente
                continue
            break
        raise RuntimeError(
            f"La SEC a répondu {r.status_code} pour {url}. "
            "Vérifie le user_agent dans config.yaml (format 'Nom contact@domaine.com')."
        )

    # --- ticker -> CIK ---------------------------------------------------
    def table_tickers(self) -> dict[str, dict]:
        chemin = self.dossier_cache / "company_tickers.json"
        if chemin.exists() and time.time() - chemin.stat().st_mtime < DUREE_CACHE_TICKERS:
            brut = json.loads(chemin.read_text(encoding="utf-8"))
        else:
            brut = self._get_json(URL_TICKERS)
            chemin.write_text(json.dumps(brut), encoding="utf-8")
        return {v["ticker"].upper(): v for v in brut.values()}

    def cik_pour(self, ticker: str) -> int:
        table = self.table_tickers()
        t = ticker.upper()
        for variante in (t, t.replace(".", "-"), t.replace("-", ".")):
            if variante in table:
                return int(table[variante]["cik_str"])
        raise KeyError(f"Ticker inconnu à la SEC : {ticker}. Ajoute son 'cik' dans config.yaml.")

    # --- dépôts ------------------------------------------------------------
    def soumissions(self, cik: int) -> dict:
        return self._get_json(URL_SUBMISSIONS.format(cik=cik))

    def derniers_depots(self, cik: int, soumissions: dict | None = None) -> list[Depot]:
        """Dépôts 10-K / 10-Q récents, du plus récent au plus ancien."""
        s = soumissions or self.soumissions(cik)
        r = s["filings"]["recent"]
        depots = []
        for i, form in enumerate(r["form"]):
            if form in FORMULAIRES_SUIVIS:
                depots.append(
                    Depot(
                        formulaire=form,
                        accession=r["accessionNumber"][i],
                        date_depot=r["filingDate"][i],
                        date_periode=r["reportDate"][i],
                        document=r["primaryDocument"][i],
                        cik=cik,
                    )
                )
        return depots

    # --- données XBRL --------------------------------------------------------
    def company_facts(self, cik: int, rafraichir: bool = True) -> dict:
        """Télécharge (ou relit du cache) toutes les données XBRL de l'entreprise."""
        chemin = self.dossier_cache / f"facts_CIK{cik:010d}.json"
        if chemin.exists() and not rafraichir:
            return json.loads(chemin.read_text(encoding="utf-8"))
        facts = self._get_json(URL_FACTS.format(cik=cik))
        chemin.write_text(json.dumps(facts), encoding="utf-8")
        return facts
