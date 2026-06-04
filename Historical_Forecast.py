import requests
import json
import os
import time
# ── Constants ────────────────────────────────────────────────────────────────

BASE_URL = "https://previous-runs-api.open-meteo.com/v1/forecast"

MODELS = [
    "icon_seamless", "icon_global", "icon_eu", "icon_d2",
    "metno_seamless", "metno_nordic",
    "geosphere_seamless", "geosphere_arome_austria",
    "dmi_harmonie_arome_europe", "dmi_seamless",
    "knmi_harmonie_arome_netherlands", "knmi_harmonie_arome_europe", "knmi_seamless",
    "ukmo_seamless", "ukmo_global_deterministic_10km", "ukmo_uk_deterministic_2km",
    "meteoswiss_icon_ch2", "italia_meteo_arpae_icon_2i",
    "meteoswiss_icon_ch1", "meteoswiss_icon_seamless",
    "meteofrance_arome_france_hd", "meteofrance_arome_france",
    "meteofrance_arpege_europe", "meteofrance_arpege_world", "meteofrance_seamless",
    "gem_seamless", "gem_global", "gem_hrdps_continental",
    "gem_regional", "gem_hrdps_west",
    "bom_access_global", "cma_grapes_global",
    "ecmwf_aifs025_single", "ecmwf_ifs025", "ecmwf_ifs",
    "best_match",
    "gfs_seamless", "gfs_global", "gfs_hrrr",
    "ncep_nbm_conus", "ncep_nam_conus", "ncep_aigfs025",
    "gfs_graphcast025", "ncep_hgefs025_ensemble_mean",
    "jma_gsm", "jma_msm", "jma_seamless",
    "kma_seamless", "kma_ldps", "kma_gdps",
]

HOURLY_VARS = ["temperature_2m", "temperature_2m_previous_day1"]


# ── Functions ─────────────────────────────────────────────────────────────────
def historical_forecast(icao, latitude, longitude, start_date, end_date, unit):
    """Orchestrate the download and saving of historical forecast data for a city."""
    print(f"\n[{icao}] Fetching forecast ({start_date} to {end_date})")
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ",".join(HOURLY_VARS),
        "models": ",".join(MODELS),
        "start_date": start_date,
        "end_date": end_date,
        "temperature_unit": unit,
    }
    
    data = fetch_forecast(params)

    save_json(data, icao)
    print(f"[{icao}] Done.")


def fetch_forecast(params):
    """Make the API request and return the JSON response."""
    print(f"  -> Request params:")
    for key, value in params.items():
        display = value if len(str(value)) < 80 else f"{str(value)[:77]}..."
        print(f"       {key}: {display}")

    response = requests.get(BASE_URL, params=params)
    print(f"  -> Status: {response.status_code} {'OK' if response.ok else 'ERROR'}")
    response.raise_for_status()
    data = response.json()

    if "error" in data:
        raise ValueError(f"API error: {data.get('reason', data)}")

    return data


def save_json(data, icao, output_dir="data"):
    """Save the JSON response to disk."""
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{icao}_Previous_Forecasts.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved: {path}")





# ── Do NOT MODIFY ─────────────────────────────────────────────────────────────

if __name__ == "__main__":

    with open("Data/Cities-Pending.json", "r", encoding="utf-8") as f:
        cities = json.load(f)

    start_date = "2021-04-01"
    end_date = "2026-04-20"

    for city in cities:
        historical_forecast(
            icao=city["icao"],
            latitude=city["lat"],
            longitude=city["lon"],
            start_date=start_date,
            end_date=end_date,
            unit=city["unit"],
        )
        time.sleep(30)
