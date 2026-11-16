# DC location under typhoon risk: three Philippine distribution sites chosen on distance and storm exposure

A one-day supply chain analytics project on real, public data, ending in a decision: **which three distribution sites, one per island group, a national distributor should study first when it weighs the distance to its customers against how often storms pass its sites.** The data are the Philippine Statistics Authority's 2024 Census of Population by province and highly urbanized city, GeoNames points for each, and 45 seasons (1980 to 2024) of tropical cyclone tracks from NOAA's IBTrACS archive. Every one of the 46,200 networks with one site in Luzon, one in the Visayas and one in Mindanao is scored on two measures, the frontier of networks not beaten on both is drawn, and three assumed prices turn the trade-off into one annual cost.

Dashboard (Power BI, with a map of the sites): add the screenshot and the file link after Step 6c of the build guide.

**Business question.** "Our three-site plan puts the Luzon distribution centre in the province closest to the people. How often do storms pass it, and what does a safer site cost us in distance?" How often did storms of tropical-storm strength pass within 100 km of each candidate site, which networks are not beaten on both distance and exposure, how many km does each step towards a lower-exposure network cost, and under which assumed costs of disruption would a safer network be cheaper overall?

**The answer from the reference run (every cost an assumption).** Study the distance-best network first: Quezon City, Cebu and Maguindanao del Norte, a population-weighted mean of 124.99 km in a straight line, whose sites storms passed within 100 km 31, 20 and 1 times in 45 seasons. Under the base assumptions it costs an assumed PHP 731.8 million a year (703.1 distance, 28.7 disruption) and no frontier network is cheaper. Across 45 combinations of the three assumed prices it stays the cheapest in 29; the chosen network is never more than 9.63 km (7.7%) farther, and the chosen network's total runs from PHP 354 million to PHP 1,664 million a year, mostly with the cost per person-km. What would change the answer: at the base disruption days and freight cost, a disruption day costing more than about PHP 32 million makes the City of Manila cheaper than Quezon City (two storms fewer in 45 seasons, which is the 100 km line rather than a lower-exposure site), more than about PHP 166 million moves the Visayas site to Negros Occidental, and the Luzon site leaves Metro Manila only if one weighted pass a season is worth more than about 1,040 km.

**Stack.** Python (pandas, numpy) to read PSA's PxWeb API, GeoNames' gazetteer and the gzipped IBTrACS file, match census names to points (Project 40's rule and crosswalk), count storm passes per point with a vectorised haversine (Project 41's rules), score every one-site-per-island-group network, find the frontier and price 45 cost scenarios; SQLite for the KPIs (central candidates ranked by exposure, the distance-best network site by site, the frontier with FIRST_VALUE and LAG, the scenario table as a CASE pivot, island-group exposure, the sites' storm months from a VALUES table); Excel for a dashboard where any frontier network and any cost per disruption day recompute with SUMIFS, COUNTIF, MIN and INDEX/MATCH; Power BI for the same dashboard, with slicers for the network and the cost a day, What-if parameters for the other two assumptions, and maps of the candidate points and the chosen sites.

## Key findings

<!-- Write this after Step 7 of the build guide: three findings, each with a number from your run and what it means for a network planner, then the recommendation with its number, its range and the one thing that would change it. Embed one chart from figures/. Say every time that distances are straight lines, that a pass is a proxy for exposure and not an impact, and that the costs are assumptions. Candidates are in the build guide, Step 7. -->

## The model in the data

```
 node            =  one PSA census entry with a GeoNames point (a province without its cities, a city, or Pateros); 117 nodes, 112,513,073 people
 pass            =  a storm whose closest point of 34 kt or more (JTWC 1-minute wind) came within 100 km of a node's point, seasons 1980 to 2024
 passes a season =  a node's passes within 100 km / 45: the exposure of that node as a site
 network         =  one site in Luzon, one in the Visayas, one in Mindanao; every node served by its nearest site in a straight line
 weighted km     =  population-weighted mean straight-line km from each node to its site
 weighted passes =  population-weighted mean passes a season at the serving site
 frontier        =  the networks no other network beats on both measures
 annual cost     =  weighted km x population x cost per person-km  +  weighted passes x days a pass x cost a day   (all three prices assumed)
```

## The data

| | |
|---|---|
| Population | Philippine Statistics Authority, [OpenSTAT](https://openstat.psa.gov.ph/), 2024 Census of Population, table `1A/PO_2024/0191A6DTHP8`, through the PxWeb API |
| Points | [GeoNames](https://www.geonames.org/) Philippines extract (`PH.zip`), CC BY 4.0 |
| Tracks | NOAA NCEI, [IBTrACS](https://www.ncei.noaa.gov/products/international-best-track-archive) v04r01, Western North Pacific CSV (last modified November 5, 2026), public domain. Citations: Knapp et al. (2010), BAMS 91, 363-376, doi:10.1175/2009BAMS2755.1; Gahtan et al. (2024), doi:10.25921/82ty-9e16 |
| Downloaded | November 6, 2026, all three |
| Coverage used | 117 nodes with 112,513,073 people (99.81% of the population PSA counts in its regions); 33,234 qualifying track points of 994 storms, seasons 1980 to 2024 |

The raw files are committed in `data/raw/` (about 12 MB together; the track file gzipped) so the snapshot is pinned. [data/README.md](data/README.md) has the sources, the definitions, the assumptions table and the data quality notes.

## Method

1. Fetch PSA's census table (CSV and PX), GeoNames' extract and the IBTrACS Western North Pacific file.
2. Profile all three: PSA's levels and notes, GeoNames' codes, the track file's units row, track types and two wind columns.
3. Clean with written rules: the 117 census nodes with points (Project 40's), the storm passes within 100 and 200 km of every node's point (Project 41's).
4. Model: the node distance matrix, every one-site-per-island-group network on two measures, a check against Project 40's p-median, the frontier, and the cheapest frontier network under 45 combinations of three assumed prices.
5. Load the six tables into SQLite.
6. Compute the KPIs in SQL: central candidates by exposure, the distance-best network, the frontier, the scenario table, island-group exposure, the storm months at the chosen sites.
7. Chart the frontier, the chosen network on a map-like plane, the distance cost of lower-exposure networks and the sensitivity of the choice.
8. Rebuild the cost view in an Excel dashboard with a network input and a cost-per-disruption-day input.
9. Write a one-page memo with the recommendation, its range and its limits.

## Repository structure

```
README.md               this file
memo.md                 one-page memo for a Director of Supply Chain
data/README.md          sources, definitions, assumptions, quality notes
data/manual_matches.csv the hand crosswalk for the ten census entries the name rule cannot match (from Project 40)
data/raw/               PSA's CSV and PX, GeoNames' PH.zip, the IBTrACS WP file gzipped (committed)
data/processed/         nodes, passes, distances, networks, assignments, scenarios (committed)
src/                    Python scripts, numbered in run order (02b is the model)
sql/                    one file per KPI query
outputs/                KPI tables as CSV (query results)
figures/                charts
excel/                  dashboard workbook and its source tables
```

## How to run

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 src/01_profile.py
python3 src/02_clean.py
python3 src/02b_model.py
python3 src/03_load_sqlite.py
python3 src/04_run_queries.py
python3 src/05_charts.py
python3 src/06_excel_export.py
```

`python3 src/01_download.py` fetches the current files into `data/raw/` (several minutes for the 115 MB track file), replacing the committed snapshot that the numbers in this repository come from, so run it only to refresh. NCEI updates IBTrACS regularly and GeoNames changes daily, so a fresh download can move the numbers; the committed files reproduce this repository.

## Supply chain concepts practiced

- Facility location with two objectives: service distance against hazard exposure, and why there is no single best network without a price.
- The Pareto frontier: the networks worth discussing, out of 46,200, and the cost of each step along it.
- Turning exposure into money with labelled assumptions, and the one ratio (km a pass is worth) the choice depends on.
- Sensitivity: the recommendation recomputed for 45 combinations of the assumptions, and the break-even cost at which it changes.
- Exposure against impact: a pass within 100 km is counted; damage is not measured.
- Noise in a threshold rule: neighbouring city points a few km apart whose pass counts differ by a storm or two.

## Limitations

- This is a method demonstration on public data, not a recommendation for any company's network. A real study would use the company's own orders by place instead of population, lane costs by road and ferry instead of an assumed cost per person-km, its own outage records instead of assumed disruption days, and site costs and capacity, which are not here.
- Distances are straight lines over land and sea; a line across water stands for a ferry or a flight.
- A pass is measured from a storm's centre to one point per node; it is a proxy for exposure, says nothing about damage, and counts storms near the site only, not along the roads to customers.
- Strength comes from one agency, the US Joint Typhoon Warning Center (1-minute winds). Seasons before 1980 are left out, and a count over 45 seasons describes a range, not a trend.
- The three costs are assumptions. Their base values are chosen for scale, not measured.
- Nothing here says anything about any province or city beyond its population, its position and the storm counts near its point.
