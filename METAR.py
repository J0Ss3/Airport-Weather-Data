"""
An example script to sequentially download data from a bunch of long term
ASOS sites, for only a few specific variables, and save the result to
individual CSV files.

More help on CGI parameters is available at:

    https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?help

You are free to use this however you want.

Author: daryl herzmann akrherz@iastate.edu
"""

import os
from datetime import date, datetime, timedelta
import json
import httpx


#station_id = "ICAO"  # Change this to the station you want to download, e.g. "KLGA"
#start_date = "YYYY-MM-DD"  # Change this to the date you want to start from, e.g. "2021-04-01"
#end_date = "YYYY-MM-DD"    # Change this to the date you want to end at, e.g. "2024-06-30"


def fetch(station_id, starting_date="2021-04-01", end_date="2026-05-20"):
    
    os.makedirs("Data", exist_ok=True)
    localfn = os.path.join("Data", f"{station_id}.csv")
    
    if os.path.isfile(localfn):
        print(f"- Cowardly refusing to over-write existing file: {localfn}")
        return
    
    print(f"+ Downloading for {station_id}")
    
    starting_year, starting_month, starting_day = map(int, starting_date.split("-"))
    end_year, end_month, end_day = map(int, end_date.split("-"))
    
    uri = (
        "http://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?"
        f"station={station_id}&data=all&year1={starting_year}&month1={starting_month}&day1={starting_day}&"
        f"year2={end_year}&month2={end_month}&day2={end_day}&"
        "tz=Etc%2FUTC&format=onlycomma&latlon=no&elev=no&missing=M&trace=T&"
        "direct=no&report_type=3&report_type=4"
    )
    
    resp = httpx.get(uri, timeout=300)
    
    with open(localfn, "w", encoding="utf-8") as fh:
        fh.write(resp.text)

def main():
    """Main loop."""
    # Step 1: Fetch global METAR geojson metadata
    # https://mesonet.agron.iastate.edu/sites/networks.php
    resp = httpx.get(
        "http://mesonet.agron.iastate.edu/geojson/network/AZOS.geojson",
        timeout=60,
    )
    geojson = resp.json()
    for feature in geojson["features"]:
        station_id = feature["id"]
        props = feature["properties"]
        # We want stations with data to today (archive_end is null)
        if props["archive_end"] is not None:
            continue
        # We want stations with data to at least 1943
        if props["archive_begin"] is None:
            continue
        archive_begin = datetime.strptime(props["archive_begin"], "%Y-%m-%d")
        if archive_begin.year > 1943:
            continue
        # Horray, fetch data
        fetch(station_id)


if __name__ == "__main__":
    starting_date = "2021-04-01"
    end_date = "2026-05-20"

    with open("Data/cities.json", "r", encoding="utf-8") as f:
        cities = json.load(f)

    for city in cities:
        fetch(city["icao"], starting_date, end_date)