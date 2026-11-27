"""Step 1: profile the three sources: PSA's 2024 census table (the CSV and the PX file), GeoNames' Philippines extract and the IBTrACS
Western North Pacific track file.

Print: every file in data/raw/ with its size in bytes.
For PSA: whether the CSV's bytes decode as UTF-8 (they do not: show the byte that fails and read the file as Latin-1); rows, columns
and column names; each row's level from its leading dots (0 the country, 2 a region, 4 a province or city) and the count of each; the
footnote markers at the end of the labels (MARKER) and their counts; the national total, the sum of the regions and the difference, and
the sum of the four-dot entries; the three smallest and three largest entries; from the PX file, SOURCE and LAST-UPDATED.
For GeoNames: the files inside the zip with sizes and dates; the rows and columns of PH.txt (no header row: COLS are the names in
GeoNames' readme); the counts of ADM1, ADM2 and ADM3 rows; the latest modification date.
For IBTrACS: the number of columns and the units row (the file's second line) for SEASON, LAT, LON, USA_WIND and TOKYO_WIND; rows,
storms (SID) and the first and last season; the track types (rows); storms by season and track type for 2024 to 2026; for seasons 1980
to 2024 and main tracks, rows and storms, then inside the box 0 to 30N and 105 to 145E; the share of those points with a USA_WIND and
with a TOKYO_WIND; the points at 34 kt or more on USA_WIND, their storms and how many are interpolated (IFLAG's first character P);
those points by month (UTC); the first rows of the box.

Answer the data quality notes in data/README.md from what you see.

Functions to look up: os.listdir, os.path.getsize, bytes.decode, UnicodeDecodeError (err.start), pd.read_csv(encoding="latin-1"),
Series.str.len, Series.str.lstrip, Series.str.extract, re.search, zipfile.ZipFile(...).infolist and .open,
pd.read_csv(sep="\t", header=None, names=COLS, dtype=str, keep_default_na=False, quoting=3), pd.read_csv(nrows=1),
pd.read_csv(skiprows=[1], usecols=..., keep_default_na=False, na_values=[" ", ""], low_memory=False), Series.between,
Series.nunique, groupby(...)["SID"].nunique, Series.notna().mean, Series.str[5:7].
"""
import os
import re
import zipfile

import pandas as pd

RAW = "data/raw"
CSV = "population_0191A6DTHP8.csv"
PX = "population_0191A6DTHP8.px"
ZIP = "PH.zip"
TRACKS = "data/raw/ibtracs.WP.list.v04r01.csv.gz"
COLS = ["geonameid", "name", "asciiname", "alternatenames", "latitude", "longitude", "feature_class", "feature_code", "country_code", "cc2",
        "admin1_code", "admin2_code", "admin3_code", "admin4_code", "population", "elevation", "dem", "timezone", "modification_date"]
TRACK_COLS = ["SID", "SEASON", "BASIN", "NAME", "ISO_TIME", "LAT", "LON", "TRACK_TYPE", "IFLAG", "USA_WIND", "TOKYO_WIND"]
MARKER = r"\s+(\d+/?\*{0,2}|\*{1,2}|a)$"   # PSA's footnote markers at the end of a label: "1/", "4/*", "8**", "*", "**", "a"


def main():
    # Build guide, Step 1: print each profile item listed above.
    # File list
    for f in sorted(os.listdir(RAW)):
        path = os.path.join(RAW, f)
        print(f"{f}: {os.path.getsize(path):,} bytes")

    # PSA
    with open(os.path.join(RAW, CSV), "rb") as f:
        raw = f.read()
    try:
        raw.decode("utf-8")
        print(f"{CSV} decodes as UTF-8")
    except UnicodeDecodeError as err:
        print(f"{CSV} is not UTF-8: fails at position {err.start} near {raw[err.start-10:err.start+10]!r}")
    p = pd.read_csv(os.path.join(RAW, CSV), encoding="latin-1")
    print(p.shape)
    print(p.columns.tolist())
    
    # Levels from the leading dots in the label column
    p.columns = ["label", "population"]
    p["dots"] = p["label"].str.len() - p["label"].str.lstrip(".").str.len()
    print(p["dots"].value_counts().sort_index().to_dict())

    # Footnote markers at the end of the labels
    p["text"] = p["label"].str.lstrip(".")
    p["marker"] = p["text"].str.extract(MARKER)[0]
    print(p["marker"].value_counts().sort_index().to_dict())

    # Totals and the smallest and largest entries
    # National total, sum of regions, difference, sum of four-dot entries
    national_total = p.loc[p["dots"] == 0, "population"].iloc[0]
    region_total = p.loc[p["dots"] == 2, "population"].sum()
    difference = national_total - region_total
    four_dot_total = p.loc[p["dots"] == 4, "population"].sum()
    four_dot_entries = p.loc[p["dots"] == 4, ["text", "population"]].sort_values("population")
    smallest = four_dot_entries.head(3)
    largest = four_dot_entries.tail(3).iloc[::-1]  # reverse the order of the last three rows to show largest first
    print(f"Summary of Total Values:\n National: {national_total:,}\n Regional: {region_total:,}\n Difference: {difference:,}\n Entries (Four Dots): {four_dot_total:,}")
    print(f"Smallest Four-Dot Entries:\n{smallest.to_string(index=False)}")
    print(f"Largest Four-Dot Entries:\n{largest.to_string(index=False)}")

    # PX file: source and last update
    with open(os.path.join(RAW, PX), "r", encoding="latin-1") as f:
        px = f.read()
    result_source = re.search(r'SOURCE="([^"]*)"', px).group(1)
    print(f"{PX} SOURCE: {result_source}")
    result_last_updated = re.search(r'LAST-UPDATED="([^"]*)"', px).group(1)
    print(f"{PX} LAST-UPDATED: {result_last_updated}")

    # GeoNames
    with zipfile.ZipFile(os.path.join(RAW, ZIP)) as z: # This will list the files inside the zip with sizes and dates
        for info in z.infolist():
            print(f"{info.filename}: {info.file_size:,} bytes, modified on {info.date_time}")
        with z.open("PH.txt") as f:
            ph = pd.read_csv(f, sep="\t", header=None, names=COLS, dtype=str, keep_default_na=False, quoting=3)
            print(ph.shape)



if __name__ == "__main__":
    main()
