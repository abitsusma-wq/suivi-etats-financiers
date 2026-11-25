# Financial Statement Tracker

This project retrieves the financial statements of selected U.S. companies directly from the SEC and maintains a reference Excel workbook.

> Learning tool: always verify important figures in the official filing. This project does not provide financial advice.

## What You Get

The main output is [`sortie/etats_financiers.xlsx`](sortie/etats_financiers.xlsx). It contains:

| Worksheet | Content |
|---|---|
| **Sommaire** (summary) | One row per company: latest filing with a link, latest annual revenue, and key ratios. Click a ticker to open its ratios. |
| **Journal** (log) | Filings detected since the first run, with a link to each document. |
| **TICKER - Résultats** | Income statement: revenue, cost of sales, margins, operating income, net income, EPS, and more. |
| **TICKER - Bilan** | Balance sheet: cash, inventory, assets, debt, equity, and more. |
| **TICKER - Flux** | Cash flow statement: operating cash flow, capital expenditures, dividends, buybacks, and more. |
| **TICKER - Ratios** | Key ratios in Excel formula format so you can inspect every calculation. |

Worksheet and row labels in the workbook are in French. Each worksheet has an **Annuel** (annual) block with 10 fiscal years at the top and a **Trimestriel** (quarterly) block with 12 quarters below. Periods run from oldest to newest, left to right. Values in *italic gray* are derived by calculation (see [How It Works](#how-it-works)).

The same data is also exported to CSV files in [`donnees/`](donnees/), for example [`AAPL_etats.csv`](donnees/AAPL_etats.csv) and [`AAPL_ratios.csv`](donnees/AAPL_ratios.csv).

## Ratios

| Ratio | Calculation |
|---|---|
| Gross, operating, and net margin | Gross profit, operating income, or net income divided by revenue |
| Operating cash flow / net income | Earnings quality; above 1 means earnings are converting well into cash |
| FCF and FCF margin | Operating cash flow minus capital expenditures; then FCF divided by revenue |
| EBITDA | Operating income plus depreciation and amortization |
| Net debt | Interest-bearing debt minus cash and short-term investments (negative means net cash) |
| Net debt / EBITDA | Number of years of EBITDA needed to repay net debt |
| ROE | Net income divided by average shareholders' equity (beginning plus ending period) |
| Current ratio | Current assets divided by current liabilities |
| 1-year growth | Revenue, net income, or EPS compared with the prior year or the prior-year quarter |

For quarterly periods, ROE and net debt / EBITDA use trailing twelve-month values (the sum of the latest four quarters). Otherwise, a single quarter's earnings would be compared with a full-period balance sheet.

## Installation

From the project directory in PowerShell:

```powershell
pip install -r requirements.txt
```

## Usage

```powershell
python -m suivi
```

The script checks every configured company for a new filing. If nothing changed, it rebuilds the workbook from the cache instead of downloading the data again.

Useful options:

```powershell
python -m suivi --force
```

Redownload all company data. Use this after changing [`suivi/concepts.py`](suivi/concepts.py).

```powershell
python -m suivi --tickers AAPL
```

Update only one or more listed companies.

**Close the Excel workbook before running the script.** If it is open, Windows locks the file. The script stops safely without losing existing data, and new filings are processed on the next run.

## Configure Companies

Open [`config.yaml`](config.yaml) and edit the `entreprises` list, then run `python -m suivi`.

```yaml
entreprises:
  - ticker: AAPL
  - ticker: MSFT
  - ticker: COST
```

Only companies that submit 10-K and 10-Q filings to the SEC are supported.

If a ticker is not recognized, such as `BRK-B`, specify its CIK:

```yaml
  - ticker: BRK-B
    cik: 1067983
```

You can find a company's CIK through [SEC EDGAR](https://www.sec.gov/edgar/search/). The configuration file also controls the number of annual periods, quarterly periods, and display units.

## SEC User-Agent

The SEC requires every request to identify the sender in `Name contact@domain.com` format. Requests without this information receive `403 Forbidden`.

The default value in `config.yaml` is generic. The SEC expects a real contact, so replace it with your email address if you want. The email is sent only to the SEC.

## Automatic Daily Check

The [`planifier_tache.ps1`](planifier_tache.ps1) script creates a Windows Task Scheduler task that runs [`lancer_suivi.bat`](lancer_suivi.bat) every day at 19:00:

```powershell
powershell -ExecutionPolicy Bypass -File .\planifier_tache.ps1
```

- Change the time: `-Heure 07:30`
- Remove the task: `-Supprimer`

Each run appends output to [`journal/execution.log`](journal/execution.log), and detected filings appear in the **Journal** worksheet.

The task runs under your Windows account and only while your session is open. If the computer is off at the scheduled time, it starts as soon as possible after restart. 10-K and 10-Q filings are often submitted after market close and can take one or more hours to appear in the SEC API.

## How It Works

```text
config.yaml ──► SEC submissions ──► new filing? ──yes──► SEC company facts (XBRL)
                                  │ no                         │
                                  ▼                             ▼
                         cache/facts_*.json ◄────────────────────┘
                                  │
             extraction.py: XBRL tags ──► annual and quarterly tables
                                  │
             ratios.py: Python ratios + Excel formulas
                                  │
             excel.py ──► Excel workbook and CSV files
```

## Data Sources

The project uses three key SEC APIs. They are free and do not require an API key:

- `www.sec.gov/files/company_tickers.json`: maps tickers to SEC CIK identifiers.
- `data.sec.gov/submissions/CIK##########.json`: lists filings and detects new 10-K/10-Q submissions.
- `data.sec.gov/api/xbrl/companyfacts/CIK##########.json`: contains the company's XBRL data, generally from 2009 onward.

The script stays within the SEC request limit and redownloads company facts only when a new filing is detected or an existing cache is missing.

## Edge Cases Handled

- **Multiple tags for the same item.** Apple used `Revenues` until 2018 and later used `RevenueFromContractWithCustomerExcludingAssessedTax`. [`suivi/concepts.py`](suivi/concepts.py) defines prioritized lists of XBRL tags for this reason.
- **Restated figures.** The same fiscal year can appear in multiple filings. The script keeps the value from the newest filing.
- **Cumulative cash flows.** 10-Q filings report year-to-date flows. Quarterly flows are calculated by subtraction: 9-month value minus 6-month value.
- **No fourth-quarter 10-Q.** Fourth-quarter values are derived from the annual filing minus nine-month values.
- **Irregular quarters.** Costco has three 12-week quarters and a 16-week fourth quarter. Its fourth quarter should be compared with the prior year's fourth quarter, not with its third quarter.

For AAPL, MSFT, and COST, the sum of four quarters exactly matches the annual total for revenue, income, operating cash flow, and capital expenditures.

## Known Limitations

- **U.S. companies only.** Canadian SEDAR+ filings do not offer a comparable public API, and automated extraction from that site is not reliable.
- **Fourth-quarter EPS is unavailable.** EPS is not additive because the share count can change, so it is not derived by quarterly subtraction.
- **No growth or ROE in the first period.** These ratios need the corresponding prior-year period.
- **Lease liabilities are excluded from net debt.** Net debt does not include lease obligations under IFRS 16 or ASC 842.
- **Unusual company-specific tags.** A company may use a custom extension tag. In that case, the corresponding item can remain blank until the tag is added to [`suivi/concepts.py`](suivi/concepts.py), followed by `python -m suivi --force`.
- **Banks and insurers.** Their statements use different structures, so items such as cost of sales may remain empty.
- **The workbook is regenerated.** Do not store notes in it. Do analysis in a separate workbook or copy the generated worksheets.

## Project Structure

```text
config.yaml            Companies and display settings
suivi/
  __main__.py          Entry point: python -m suivi
  sec.py               SEC API access
  concepts.py          Financial statement items and XBRL tags
  extraction.py        XBRL data to annual and quarterly tables
  ratios.py            Ratio definitions and Excel formulas
  excel.py             Excel workbook generation
  etat.py              Processed-filings state (donnees/etat.json)
tests/                 Automatic tests; no network access
lancer_suivi.bat       Scheduled-task launcher
planifier_tache.ps1    Create or remove the Windows scheduled task
```

## Tests

```powershell
python -m pytest
```
