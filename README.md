# AlmaLaurea Analysis

Statistical analysis of Italian university graduates using data from [AlmaLaurea](https://www.almalaurea.it), Italy's national graduate database. Covers the period **2008–2024** across all 15 MUR 2020 discipline groups.

## Structure

```
├── almalaurea/
│   ├── constants.py   — area/group mappings and shared config
│   ├── scraper.py     — fetch_profile() and fetch_employment()
│   └── plots.py       — one function per chart
├── data/
│   ├── almalaurea.csv — pre-scraped dataset (~816 rows)
│   └── id_uni.csv     — lookup table: university names → AlmaLaurea IDs
├── plots/             — output PNG charts
└── main.py            — entry point
```

## Charts produced (`plots/`)

| File | Function | Content |
|---|---|---|
| `M_VS_F.png` | `plot_gender_split` | Male/female graduate percentages by discipline group *(requires HTTP)* |
| `retribuzione_gruppi_{1,3,5}.png` | `plot_salary_by_group` | Monthly net salary by gender at 1, 3, and 5 years post-graduation |
| `divario_retributivo.png` | `plot_pay_gap` | Gender pay gap (%) over time by discipline group |
| `disoccupazione_gruppi.png` | `plot_unemployment` | Unemployment rate over time by discipline group |
| `numero_laureati_percentuale.png` | `plot_graduate_share` | Share of graduates per discipline group over time |

## Tech stack

- **Python 3**
- `requests` + `re` — HTML scraping and regex parsing of AlmaLaurea pages
- `pandas` / `numpy` — data wrangling
- `matplotlib` — plotting
- `tqdm` — progress bars during scraping

## Installation

```bash
pip install numpy matplotlib requests pandas tqdm
```

## Usage

The dataset has already been collected and saved to `data/almalaurea.csv`. To regenerate all charts, run:

```bash
python main.py
```

Output PNGs are written to the `plots/` directory.

To add or remove a specific chart, edit the `main()` function in `main.py` and call (or remove) the corresponding plot function.

To re-scrape data from AlmaLaurea, uncomment the `collect_data()` function in `main.py` and call it from `main()`. Be aware this makes many HTTP requests and may take a while.

## Data structure

`data/almalaurea.csv` columns:

| Column | Description |
|---|---|
| `anno` | Graduation year |
| `anni_da_conseguimento_titolo` | Years since graduation (1, 3, or 5) |
| `gruppo` | Discipline group ID (1–15 or `tutti`) |
| `ateneo` | University ID (`tutti` = national aggregate) |
| `numero_laureati` | Total graduate count |
| `percentuale_maschi` | % male graduates |
| `percentuale_femmine` | % female graduates |
| `tasso_occupazione_totale` | Employment rate (%) |
| `tasso_disoccupazione_totale` | Unemployment rate (%) |
| `retribuzione_mensile_maschi` | Monthly net salary — men (€) |
| `retribuzione_mensile_femmine` | Monthly net salary — women (€) |
| `retribuzione_mensile` | Monthly net salary — total (€) |

## Discipline groups (MUR 2020)

| ID | Group | Area |
|---|---|---|
| 1 | Educazione e formazione | ALE |
| 2 | Arte e design | ALE |
| 3 | Letterario umanistico | ALE |
| 4 | Linguistico | ALE |
| 5 | Politico-sociale e comunicazione | EGS |
| 6 | Psicologico | EGS |
| 7 | Economico | EGS |
| 8 | Giuridico | EGS |
| 9 | Scientifico | STEM |
| 10 | Informatica e tecnologie ICT | STEM |
| 11 | Architettura e Ing civile | STEM |
| 12 | Ing industriale e dell'informazione | STEM |
| 13 | Agrario-forestale e veterinario | SAV |
| 14 | Medico-sanitario e farmaceutico | SAV |
| 15 | Scienze motorie e sportive | SAV |

## Source & author

Data source: [AlmaLaurea](https://www.almalaurea.it)
Elaboration: Biasissi Riccardo
