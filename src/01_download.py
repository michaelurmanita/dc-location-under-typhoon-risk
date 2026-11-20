"""Step 0: fetch the three sources into data/raw/: PSA's 2024 census table, GeoNames' Philippines extract and the IBTrACS Western
North Pacific track file.

The pinned copies the checkpoints were computed on are already in data/raw/ (downloaded November 6, 2026) and committed. Complete this
script so the project can be refreshed:

- PSA (PxWeb API, as in Project 40): GET the table's metadata (the PSA URL returns JSON with a title and a list of variables) and print
  the title and each variable's code and number of values. Then POST a query that selects every Geographic Location
  ({"filter": "all", "values": ["*"]}) and the Parameter "0", Total Population ({"filter": "item", "values": ["0"]}), once with
  {"format": "csv"} and once with {"format": "px"}, and save each response's bytes as received: data/raw/population_0191A6DTHP8.csv
  and data/raw/population_0191A6DTHP8.px. PSA sends Latin-1 text, so write the bytes with open(path, "wb"); do not decode and
  re-encode them. Sleep PAUSE seconds after every request to PSA. PSA answers a request that is too large or too fast with a 403 page:
  on a 403, wait 60 seconds and try once more with the BROWSER headers ("Mozilla/5.0"); other people's requests share the server.
- GeoNames: GET GEONAMES and save the bytes as data/raw/PH.zip.
- IBTrACS (as in Project 41): GET IBTRACS (115 MB, a few minutes) and write it gzipped as data/raw/ibtracs.WP.list.v04r01.csv.gz with
  gzip.compress(data, compresslevel=9, mtime=0); the file as served is over GitHub's 100 MB limit, and pandas reads the .gz directly.

Print each file's name and size in bytes (for IBTrACS, the size as served, its Last-Modified header, its line count and the gzipped size).

Functions to look up: urllib.request.Request(url, data=..., headers=...), urllib.request.urlopen(..., timeout=...), r.headers.get,
urllib.error.HTTPError (err.code), json.loads, json.dumps, bytes.decode("utf-8-sig"), time.sleep, gzip.compress, bytes.count,
open(path, "wb").
"""
import gzip
import json
import os
import sys
import time
import urllib.error
import urllib.request

RAW = sys.argv[1] if len(sys.argv) > 1 else "data/raw"   # optional first argument: a scratch folder, so a test run leaves the pinned files alone
PSA = "https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/1A/PO_2024/0191A6DTHP8.px"
GEONAMES = "https://download.geonames.org/export/dump/PH.zip"
IBTRACS = "https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/ibtracs.WP.list.v04r01.csv"
HEADERS = {"User-Agent": "portfolio-project/1.0 (learning project)", "Content-Type": "application/json"}
BROWSER = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}   # PSA's fallback when the plain User-Agent is refused
PAUSE = 2   # seconds after every request to PSA's server

def psa_open(body):
    try:
        req = urllib.request.Request(PSA, data=body, headers=HEADERS)
        r = urllib.request.urlopen(req, timeout=60)
        data = r.read()
    except urllib.error.HTTPError as err:
        if err.code != 403:
            raise
        print("PSA returned 403, waiting 60 seconds and retrying once")
        time.sleep(60)
        req = urllib.request.Request(PSA, data=body, headers=BROWSER)
        r = urllib.request.urlopen(req, timeout=60)
        data = r.read()
    time.sleep(PAUSE)
    return data
    

def main():
    # Build guide, Step 0.
    os.makedirs(RAW, exist_ok=True)

    #GeoNames
    req = urllib.request.Request(GEONAMES, headers=HEADERS)
    r = urllib.request.urlopen(req, timeout=60)
    data = r.read()
    path = os.path.join(RAW, "PH.zip")
    with open(path, "wb") as f:
        f.write(data)
    print(f"{path} {len(data)}")

    #IBTrACS
    #plus gzip -- refer to the readings above for the gzip.compress() function, which takes a bytes object and returns a bytes object.
    req = urllib.request.Request(IBTRACS, headers=HEADERS)
    r = urllib.request.urlopen(req, timeout=60)
    data = r.read()
    path = os.path.join(RAW, "ibtracs.WP.list.v04r01.csv.gz")
    with open(path, "wb") as f:
        f.write(gzip.compress(data, compresslevel=9, mtime=0))
    print(f"{path} {len(data)} {r.headers.get('Last-Modified')} {data.count(b'\n')} {os.path.getsize(path)}")

    #PSA
    data = psa_open(None)
    metadata = json.loads(data.decode("utf-8-sig"))
    print(metadata["title"])
    for var in metadata["variables"]:
        print(f"{var['code']} {len(var['values'])}")

    json_query = {
        "query": [
            {"code": "Geographic Location", "selection": {"filter": "all", "values": ["*"]}}, 
            {"code": "Parameter", "selection": {"filter": "item", "values": ["0"]}}
            ], 
        "response": {"format": "csv"}
    }

    for fmt in ["csv", "px"]:
        data = psa_open(json.dumps({**json_query, "response": {"format": fmt}}).encode("utf-8"))
        path = os.path.join(RAW, f"population_0191A6DTHP8.{fmt}")        
        with open(path, "wb") as f:
            f.write(data)
        print(f"{path} {len(data)}")


if __name__ == "__main__":
    main()
