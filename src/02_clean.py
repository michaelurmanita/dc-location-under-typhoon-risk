"""Step 2: build data/processed/nodes.csv (one row per demand node, with its census population, its GeoNames point and the storm passes
near that point) and data/processed/passes.csv (one row per storm and node within 200 km).

data/processed/nodes.csv   node_id, name, kind, region, island_group, population_2024, lat, lon, match_method, geonameid, geonames_name,
                           passes_100km, passes_200km, mean_annual_passes_100km, typhoon_passes_100km
                           one row per PSA four-dot entry that has a coordinate (117 rows), in the order of PSA's table, node_id from 0.
                           The first eleven columns are Project 40's nodes.csv, built by its rules: name is PSA's label without the
                           leading dots, the footnote marker and a bracket at the end; kind is ncr_city, municipality, other, huc or
                           province; region from REGIONS; island_group from ISLAND_GROUP; lat, lon, geonameid and geonames_name from the
                           GeoNames row matched; match_method rule or manual.
                           passes_100km: passes with min_km <= 100; passes_200km: all passes; mean_annual_passes_100km: passes_100km / 45,
                           3 decimals; typhoon_passes_100km: passes within 100 km with wind_kt >= 64; 0 where a node has none.
data/processed/passes.csv  sid, season, name, node_id, node, closest_time, month, min_km, wind_kt
                           one row per storm and node where the storm's closest qualifying point came within 200 km of the node's point,
                           sorted by season, sid, node_id. A qualifying point: seasons 1980 to 2024, TRACK_TYPE main, LAT 0 to 30, LON
                           105 to 145, USA_WIND >= 34. min_km: haversine km rounded to 0.1 at once; the closest point per storm and
                           node, the earliest on a tie. month: of closest_time (UTC). wind_kt: USA_WIND at that point.

The match (Project 40): a city looks among GeoNames' ADM3 rows, anything else among the ADM2 rows, in the same region (GN_REGION),
for the same core_name(); exactly one hit is a match. The entries the rule cannot match must be exactly the rows of
data/manual_matches.csv (assert it); a crosswalk row with a geonameid gives the point (match_method manual); the entry whose row has no
geonameid is printed with its population and share, and left out. The passes (Project 41): the haversine between every qualifying
point and every node point as one numpy matrix. The full rules are in the build guide, Step 2. Complete core_name(), haversine_km()
and main(), and print the counts the guide's checkpoint lists.

Functions to look up: pd.read_csv(encoding="latin-1"), Series.str.lstrip, Series.str.extract, Series.str.replace(regex=True),
Series.where(...).ffill(), Series.map(dict), DataFrame.loc[mask, column] = value, re.sub, DataFrame.iterrows, zipfile.ZipFile(...).open,
pd.read_csv(sep="\t", header=None, names=COLS, dtype=str, keep_default_na=False, quoting=3), DataFrame.merge(on=..., how="left"),
DataFrame.insert, assert, pd.read_csv(skiprows=[1], usecols=..., keep_default_na=False, na_values=[" ", ""]), Series.between,
np.radians, np.sin, np.cos, np.arcsin, broadcasting with [:, None] and [None, :], ndarray.round, np.where, DataFrame.sort_values,
DataFrame.drop_duplicates, groupby(...).size, Series.fillna.
"""
import re
import zipfile

import numpy as np
import pandas as pd

RAW = "data/raw"
OUT = "data/processed"
CSV = "population_0191A6DTHP8.csv"
ZIP = "PH.zip"
TRACKS = "data/raw/ibtracs.WP.list.v04r01.csv.gz"
MANUAL = "data/manual_matches.csv"
COLS = ["geonameid", "name", "asciiname", "alternatenames", "latitude", "longitude", "feature_class", "feature_code", "country_code", "cc2",
        "admin1_code", "admin2_code", "admin3_code", "admin4_code", "population", "elevation", "dem", "timezone", "modification_date"]
TRACK_COLS = ["SID", "SEASON", "NAME", "ISO_TIME", "LAT", "LON", "TRACK_TYPE", "IFLAG", "USA_WIND"]
MARKER = r"\s+(\d+/?\*{0,2}|\*{1,2}|a)$"   # PSA's footnote markers at the end of a label: "1/", "4/*", "8**", "*", "**", "a"
REGIONS = {"National Capital Region (NCR)": "NCR", "Cordillera Administrative Region (CAR)": "CAR", "Region I (Ilocos Region)": "Region I",
           "Region II (Cagayan Valley)": "Region II", "Region III (Central Luzon)": "Region III", "Region IV-A (CALABARZON)": "Region IV-A",
           "MIMAROPA Region": "MIMAROPA", "Region V (Bicol Region)": "Region V", "Region VI (Western Visayas)": "Region VI",
           "Negros Island Region (NIR)": "NIR", "Region VII (Central Visayas)": "Region VII", "Region VIII (Eastern Visayas)": "Region VIII",
           "Region IX (Zamboanga Peninsula)": "Region IX", "Region X (Northern Mindanao)": "Region X", "Region XI (Davao Region)": "Region XI",
           "Region XII (SOCCSKSARGEN)": "Region XII", "Region XIII (Caraga)": "Region XIII",
           "Bangsamoro Autonomous Region In Muslim Mindanao (BARMM)": "BARMM"}
ISLAND_GROUP = {"NCR": "Luzon", "CAR": "Luzon", "Region I": "Luzon", "Region II": "Luzon", "Region III": "Luzon", "Region IV-A": "Luzon",
                "MIMAROPA": "Luzon", "Region V": "Luzon", "Region VI": "Visayas", "NIR": "Visayas", "Region VII": "Visayas", "Region VIII": "Visayas",
                "Region IX": "Mindanao", "Region X": "Mindanao", "Region XI": "Mindanao", "Region XII": "Mindanao", "Region XIII": "Mindanao", "BARMM": "Mindanao"}
GN_REGION = {"NCR": "NCR", "15": "CAR", "01": "Region I", "02": "Region II", "03": "Region III", "40": "Region IV-A", "41": "MIMAROPA",   # GeoNames admin1 code
             "05": "Region V", "06": "Region VI", "07": "Region VII", "08": "Region VIII", "09": "Region IX", "10": "Region X",          # to PSA region, read off
             "11": "Region XI", "12": "Region XII", "13": "Region XIII", "14": "BARMM"}                                                 # the 17 ADM1 names
FIRST, LAST = 1980, 2024                 # analysis seasons; 45 of them
SEASONS = LAST - FIRST + 1
TS_KT, TY_KT = 34, 64                    # tropical-storm and typhoon strength on USA_WIND (JTWC, 1-minute, knots)
NEAR_KM, FAR_KM = 100, 200               # the pass radius and the wider band
EARTH_KM = 6371.0


def core_name(name):
    """The part of a name both sources share: no bracket at the end, no "Province of " or "City of " in front, no " City" at the end, lower case."""
    pass


def haversine_km(lat1, lon1, lat2, lon2):
    # Build guide, Step 2: great-circle km, working on single numbers and on numpy arrays.
    pass


def build_nodes():
    # Build guide, Step 2, rules 1 to 9 (Project 40's): PSA entries, GeoNames rows, the rule match, the crosswalk; return the nodes.
    pass


def build_passes(n):
    # Build guide, Step 2, rules 10 to 12 (Project 41's): qualifying points, the distance matrix, the closest point per storm and node.
    pass


def main():
    # Build guide, Step 2: build_nodes(), build_passes(), the pass counts on each node (rule 13), write nodes.csv and passes.csv,
    # print the checkpoint counts.
    pass


if __name__ == "__main__":
    main()
