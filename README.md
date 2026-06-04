# ✈️ Airport Weather Data

A collection of Python scripts to bulk-download historical weather observations and multi-model forecast data for airport stations, using publicly available meteorological APIs.

---

## 📁 Repository Structure

```
Airport-Weather-Data/
├── METAR.py                  # Downloads historical METAR observations via Iowa State Mesonet
├── Historical_Forecast.py    # Downloads historical NWP model forecasts via Open-Meteo
└── Data/
    ├── cities.json           # City/airport list for METAR downloads
    └── Cities-Pending.json   # City/airport list for forecast downloads
```

---

## 🛠️ Scripts

### `METAR.py` — ASOS/METAR Observations

Downloads historical Automated Surface Observing System (ASOS) data for a list of airport stations from the [Iowa State University Mesonet API](https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py).

- Reads a list of airport ICAO codes from `Data/cities.json`
- Fetches all available weather variables for each station over a configurable date range
- Saves output as individual CSV files in the `Data/` directory
- Skips stations that already have a local file (safe to re-run)

**Data source:** [mesonet.agron.iastate.edu](https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?help)

---

### `Historical_Forecast.py` — NWP Model Forecasts

Downloads historical forecast data from the [Open-Meteo Previous Runs API](https://previous-runs-api.open-meteo.com), covering a wide range of numerical weather prediction (NWP) models.

- Reads station metadata (ICAO, lat/lon, temperature unit) from `Data/Cities-Pending.json`
- Fetches `temperature_2m` and `temperature_2m_previous_day1` across **40+ NWP models**, including ECMWF, GFS, ICON, MetNo, UKMO, Météo-France, and others
- Saves output as per-station JSON files in a `data/` directory
- Includes a 30-second delay between requests to respect API rate limits

**Data source:** [open-meteo.com](https://open-meteo.com)

---

## ⚙️ Setup

### Prerequisites

- Python 3.8+
- [`httpx`](https://www.python-httpx.org/) (used in `METAR.py`)
- [`requests`](https://requests.readthedocs.io/) (used in `Historical_Forecast.py`)

### Installation

```bash
git clone https://github.com/J0Ss3/Airport-Weather-Data.git
cd Airport-Weather-Data
pip install httpx requests
```

---

## 🚀 Usage

### 1. Configure your station list

Edit `Data/cities.json` for METAR downloads:

```json
[
  { "icao": "KLGA" },
  { "icao": "EGLL" }
]
```

Edit `Data/Cities-Pending.json` for forecast downloads:

```json
[
  { "icao": "KLGA", "lat": 40.7769, "lon": -73.8740, "unit": "fahrenheit" },
  { "icao": "EGLL", "lat": 51.4775, "lon": -0.4614,  "unit": "celsius"    }
]
```

### 2. Run METAR observations download

```bash
python METAR.py
```

Output: `Data/<ICAO>.csv` for each station.

### 3. Run historical forecast download

```bash
python Historical_Forecast.py
```

Output: `data/<ICAO>_Previous_Forecasts.json` for each station.

> **Note:** The forecast script applies a 30-second pause between stations. For large station lists this will take some time.

---

## 📅 Default Date Range

Both scripts are pre-configured with the following range:

| Parameter    | Value        |
|-------------|-------------|
| Start date  | 2021-04-01  |
| End date    | 2026-04-20  |

Modify the `start_date` / `end_date` variables in each script's `__main__` block to change the range.

---

## 📦 Data Sources

| Source | Description | Docs |
|--------|-------------|------|
| Iowa State Mesonet | ASOS/METAR observations | [Link](https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?help) |
| Open-Meteo Previous Runs | Multi-model NWP forecasts | [Link](https://open-meteo.com/en/docs/historical-forecast-api) |

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

Original METAR script adapted from work by Daryl Herzmann ([@akrherz](https://github.com/akrherz)), Iowa State University.
