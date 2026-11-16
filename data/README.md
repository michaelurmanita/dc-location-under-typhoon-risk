# Data

## Source

Three public sources, downloaded on November 6, 2026 by `src/01_download.py` and committed in `data/raw/` so the snapshot is pinned.

| File | Source | As committed |
|---|---|---|
| `population_0191A6DTHP8.csv` | Philippine Statistics Authority (PSA), OpenSTAT, table `1A/PO_2024/0191A6DTHP8.px` "Total Population, Household Population, Number of Households and Average Household Size by Region, Province, and Highly Urbanized City: Philippines, 2024", Parameter = Total Population, through the PxWeb API | 4,115 bytes as received: 137 rows and 2 columns (Geographic Location, Total Population), Latin-1 text |
| `population_0191A6DTHP8.px` | The same query returned in PC-Axis format | 12,067 bytes as received; the header carries SOURCE, LAST-UPDATED and PSA's notes (NOTEX) |
| `PH.zip` | [GeoNames](https://www.geonames.org/) gazetteer extract for the Philippines, `https://download.geonames.org/export/dump/PH.zip` (last modified November 6, 2026) | 2,555,692 bytes as downloaded: `PH.txt` (tab-separated, no header) and `readme.txt` |
| `ibtracs.WP.list.v04r01.csv.gz` | NOAA NCEI, International Best Track Archive for Climate Stewardship (IBTrACS) v04r01, Western North Pacific CSV: `https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/ibtracs.WP.list.v04r01.csv` (last modified November 5, 2026) | 9,488,128 bytes: the CSV as served (114,716,773 bytes, 249,274 lines), gzipped by the download script with `gzip.compress(data, compresslevel=9, mtime=0)` and otherwise unchanged; the file as served is over GitHub's 100 MB limit |

`data/manual_matches.csv` is the hand crosswalk of Project 40 (philippine-dc-location): ten PSA entries the name rule cannot match to GeoNames, one row each with a note.

| | |
|---|---|
| PSA terms | OpenSTAT data for public use with attribution ("Philippine Statistics Authority, 2024 Census of Population, OpenSTAT, downloaded November 6, 2026"). PSA answers a request that is too large or too fast with a 403 page; the download script pauses two seconds after every PSA request and, on a 403, waits a minute and retries with the User-Agent "Mozilla/5.0" (on November 6, 2026 the plain User-Agent was accepted) |
| GeoNames terms | Creative Commons Attribution 4.0 ("GeoNames, geonames.org, CC BY 4.0"); the readme says the data is provided "as is" without warranty of accuracy |
| IBTrACS terms | NOAA data, public domain. NCEI asks for both citations: Knapp, K. R., M. C. Kruk, D. H. Levinson, H. J. Diamond, and C. J. Neumann, 2010: The International Best Track Archive for Climate Stewardship (IBTrACS): Unifying tropical cyclone best track data. Bulletin of the American Meteorological Society, 91, 363-376, doi:10.1175/2009BAMS2755.1; and Gahtan, J., K. R. Knapp, C. J. Schreck, H. J. Diamond, J. P. Kossin, M. C. Kruk, 2024: IBTrACS Project, Version 4r01, Western North Pacific subset, NOAA NCEI, doi:10.25921/82ty-9e16, accessed November 6, 2026 |
| IBTrACS documentation | [Column documentation](https://www.ncei.noaa.gov/sites/default/files/2025-09/IBTrACS_v04r01_column_documentation.pdf) and [technical details](https://www.ncei.noaa.gov/sites/default/files/2025-04/IBTrACS_version4r01_Technical_Details.pdf) |
| Units | Persons; decimal degrees (WGS84); knots (USA_WIND, the Joint Typhoon Warning Center's 1-minute wind); km computed in this project; costs in Philippine pesos, all assumed |

## Definitions used in this project

- Node (Project 40's rules): a PSA four-dot entry (a province without its highly urbanized cities, a city, or Pateros) with a GeoNames point: 117 of the 118 entries. The Special Geographic Area in BARMM has no GeoNames row and is left out (214,703 people, 0.19% of the population in PSA's regions). Names are matched by a core-name rule within the same region; the ten entries the rule cannot match come from `data/manual_matches.csv`. Island group from PSA's region: Luzon (NCR, CAR, Regions I, II, III, IV-A and V, and MIMAROPA), the Visayas (Regions VI to VIII and the Negros Island Region), Mindanao (Regions IX to XIII and BARMM).
- Population: PSA's 2024 census count of the node; the demand weight. Every person weighs the same.
- Distance: great-circle km between two node points (haversine, Earth radius 6,371 km), rounded to 0.1 km; a straight line over land and sea.
- Qualifying track point (Project 41's rules): seasons 1980 to 2024, TRACK_TYPE main, latitude 0 to 30N and longitude 105 to 145E inclusive, USA_WIND of 34 kt or more (tropical-storm strength on JTWC's 1-minute wind). Every 3-hourly point counts, interpolated or not.
- Pass: for each storm and node, the qualifying point closest to the node's point (the earliest on a tie), kept when it is 200 km or less away; "within 100 km" means 100 km or less. The month is that point's month (UTC). A typhoon-strength pass has a wind of 64 kt or more at that point.
- Passes a season of a candidate site: its passes within 100 km over 1980 to 2024, divided by 45. A pass is a proxy for exposure (a storm's centre came near the point), not a measure of damage or of any impact.
- Network: three sites, one node in each island group (60 x 22 x 35 = 46,200 networks). Every node is served by its nearest site in a straight line (the lower node_id on a tie), whatever its island group.
- Weighted km of a network: population-weighted mean km from each node to its site. Weighted passes: population-weighted mean of the serving site's passes a season, so the storm exposure of the site the average person depends on.
- Frontier: the networks that no other network beats on both measures (no other network has a weighted km as low or lower and a lower weighted passes). Frontier rank 1 is the distance-best network.
- Annual cost of a network: distance cost (weighted km x population x cost per person-km) plus disruption cost (weighted passes x disruption days a pass x cost per disruption day). Every one of the three prices is an assumption (below). The chosen network of a scenario is the frontier network with the lowest annual cost; the cheapest network of all is always on the frontier, because a network off it is beaten on both measures by one that is.

## Assumptions

None of these numbers is in the data. They are stand-ins so the method can run; the method, not the number, is the point. Replace each with a company's own figure before using the answer.

| Assumption | Values (base in bold) | Unit | Why this value | Source |
|---|---|---|---|---|
| Disruption days for each storm pass within 100 km of a site | 1, **3**, 7 | days of lost or delayed deliveries from that site | A range from a one-day closure to a week of disruption, to show how much the answer moves; no public source gives a Philippine warehouse figure | assumed; replace with your own outage records |
| Cost of one disruption day | 5, 10, **20**, 40, 80 | PHP million for a day without deliveries to the whole network's demand (a site serving 54% of the people costs 54% of it) | For scale only: a distributor with assumed sales of PHP 20 billion a year sells about PHP 55 million a day; the base takes a bit over a third of that as lost margin and recovery cost | assumed; replace with your own |
| Cost to serve one person one km a year | 0.025, **0.05**, 0.1 | PHP per person-km a year | Sets the distance cost of the distance-best network at about PHP 703 million a year at base (a few percent of the assumed PHP 20 billion of sales); halved and doubled for the range | assumed; replace with your own lane costs |
| Demand | 2024 census population | persons | Every person weighs the same; a company's own orders by place would replace it | PSA (data, used as a stand-in for demand) |
| Who a pass affects | the serving site's share of demand | | A pass is counted at the site only; storms between a site and its customers, and passes near customers, are not counted | assumed |

The choice depends on the three prices only through one ratio: the weighted km that one weighted pass a season is worth, `days_per_pass x cost_per_day / (cost_per_person_km x population)` (`km_per_pass` in `scenarios.csv`). At the base values it is 10.67 km.

## Processed tables

| File | Grain | Columns |
|---|---|---|
| `nodes.csv` | one row per node (117), in PSA's table order | node_id (0 to 116), name, kind, region, island_group, population_2024, lat, lon, match_method (rule or manual), geonameid, geonames_name, passes_100km, passes_200km, mean_annual_passes_100km (passes_100km / 45, 3 decimals), typhoon_passes_100km |
| `passes.csv` | one row per storm and node within 200 km (6,726) | sid, season, name, node_id, node, closest_time, month, min_km, wind_kt |
| `distances.csv` | one row per pair of nodes, from_id < to_id (6,786) | from_id, to_id, km (one decimal) |
| `networks.csv` | one row per network with one site per island group (46,200) | network_id, luzon_site_id, visayas_site_id, mindanao_site_id, luzon_site, visayas_site, mindanao_site, sites, weighted_km (4 decimals), weighted_passes (6 decimals), on_frontier (1 or 0), frontier_rank (blank off the frontier) |
| `assignments.csv` | one row per frontier network and node (3,978: 34 networks x 117 nodes) | network_id, node_id, site_id, km |
| `scenarios.csv` | one row per combination of the three assumptions (45) | scenario_id, days_per_pass, cost_per_day_php_m, cost_per_person_km_php, is_base, km_per_pass, chosen_network_id, chosen_frontier_rank, chosen_sites, weighted_km, weighted_passes, distance_cost_php_m, disruption_cost_php_m, total_cost_php_m, distance_best_total_php_m, saving_vs_distance_best_php_m, extra_km_vs_distance_best |

## Data quality notes

<!-- Fill this in after Step 1 of the build guide: PSA's Latin-1 encoding and the byte that shows it; the levels in the leading dots and the footnote markers; the regions against the national total (the 1,708 people abroad); the GeoNames file without a header and its own region codes; the ten entries the name rule cannot match and the one left without a point; the IBTrACS units row and the blank-as-space fields; the provisional 2025 and 2026 tracks; the share of points with a USA_WIND and with a TOKYO_WIND; the interpolated 3-hourly points; the months of the qualifying points; the Metro Manila city points a few km apart whose pass counts differ by a storm or two; and any Step 2 rule you changed from the Definitions above. -->
