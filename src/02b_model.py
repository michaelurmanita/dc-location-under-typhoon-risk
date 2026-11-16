"""Step 2b: the distance-against-exposure trade-off for a three-site network. Write distances.csv, networks.csv, assignments.csv and
scenarios.csv in data/processed/.

distances.csv    from_id, to_id, km
                 every pair of nodes once (from_id < to_id, 6,786 rows): haversine km between node points, rounded to one decimal.
                 Build the full 117 by 117 matrix, round it, and use the rounded matrix everywhere in the model.
networks.csv     network_id, luzon_site_id, visayas_site_id, mindanao_site_id, luzon_site, visayas_site, mindanao_site, sites,
                 weighted_km, weighted_passes, on_frontier, frontier_rank
                 one row per network with one site in each island group (60 x 22 x 35 = 46,200 rows), network_id from 1 in the order
                 itertools.product gives (Luzon nodes, then Visayas, then Mindanao, each in node_id order). Every node is served by its
                 nearest site (the lower node_id on a tie). weighted_km: population-weighted mean km to that site, 4 decimals.
                 weighted_passes: population-weighted mean of the serving site's passes_100km / 45, 6 decimals. sites: the three names
                 joined with "; " in island-group order. on_frontier: 1 when no other network has both a lower or equal weighted_km
                 and a lower weighted_passes (frontier()); frontier_rank: 1 for the distance-best, then by weighted_km; blank off it.
assignments.csv  network_id, node_id, site_id, km
                 each node's site and km for every frontier network (117 rows per network).
scenarios.csv    scenario_id, days_per_pass, cost_per_day_php_m, cost_per_person_km_php, is_base, km_per_pass, chosen_network_id,
                 chosen_frontier_rank, chosen_sites, weighted_km, weighted_passes, distance_cost_php_m, disruption_cost_php_m,
                 total_cost_php_m, distance_best_total_php_m, saving_vs_distance_best_php_m, extra_km_vs_distance_best
                 one row per combination of the three assumption lists (3 x 5 x 3 = 45 rows, in itertools.product order): the frontier
                 network with the lowest annual_cost() total (the lower frontier rank on a tie). km_per_pass: days_per_pass x cost per
                 day / (cost per person-km x population), the weighted km one pass a season is worth (2 decimals). Costs in PHP million,
                 1 decimal; weighted_km 2 decimals; weighted_passes 4 decimals; extra_km_vs_distance_best 2 decimals.

The assumptions (DAYS_PER_PASS, COST_PER_DAY_PHP_M, COST_PER_PERSON_KM_PHP, BASE) are stand-ins, not data: the build guide's Step 2b
and data/README.md give each one's reason. Write the functions below, then main(). Print what the guide's checkpoint lists: the
number of networks, the distance-best network and the check against Project 40's greedy plus swap, the lowest-exposure network, the
frontier with each network's extra km and passes, the break-even km per pass of each frontier step, the networks that are the cheapest at some price (and from which km per pass), the base scenario's choice and
costs, the chosen frontier rank for every scenario, and the row counts.

Functions to look up: np.radians, np.sin, np.cos, np.arcsin, broadcasting with lat[:, None] and lat[None, :], ndarray.round,
np.triu_indices(n, k=1), np.argmin(axis=1), np.arange, the @ operator (a dot product), itertools.product, DataFrame.sort_values,
DataFrame.itertuples, Series.isin, Series.map, astype("Int64"), np.diff, DataFrame.pivot, pd.concat.
"""
import itertools

import numpy as np
import pandas as pd

OUT = "data/processed"
EARTH_KM = 6371.0
SEASONS = 45                      # 1980 to 2024
GROUPS = ["Luzon", "Visayas", "Mindanao"]
# Assumptions (stand-ins, not data; the build guide's Step 2b and data/README.md say why each value was picked)
DAYS_PER_PASS = [1, 3, 7]                       # disruption days at a site for each storm pass within 100 km; base 3
COST_PER_DAY_PHP_M = [5, 10, 20, 40, 80]        # PHP million for one day without deliveries to the whole network's demand; base 20
COST_PER_PERSON_KM_PHP = [0.025, 0.05, 0.1]     # PHP a year to serve one person one km from the site; base 0.05
BASE = {"days_per_pass": 3, "cost_per_day_php_m": 20, "cost_per_person_km_php": 0.05}


def haversine_km(lat1, lon1, lat2, lon2):
    # Build guide, Step 2b: the formula from Step 2, for the node-to-node matrix.
    pass


def assign(D, sites):
    # Build guide, Step 2b: each node's nearest site (the lower node_id on a tie) and the km to it.
    pass


def score(D, pop, rate, sites):
    # Build guide, Step 2b: the two measures of a network: weighted mean km and weighted passes a season at the serving site.
    pass


def greedy(D, pop, p):
    # Build guide, Step 2b: Project 40's greedy add, for the check.
    pass


def swap(D, pop, sites):
    # Build guide, Step 2b: Project 40's one-swap, for the check.
    pass


def frontier(net):
    # Build guide, Step 2b: the network_ids no other network beats on both measures, in order of weighted km.
    pass


def annual_cost(weighted_km, weighted_passes, population, days_per_pass, cost_per_day_php_m, cost_per_person_km_php):
    # Build guide, Step 2b: the distance cost and the disruption cost a year, in PHP million.
    pass


def main():
    # Build guide, Step 2b: the matrix and distances.csv; every network and its two measures; the check; the frontier; the
    # assignments of the frontier networks; the scenarios; the break-even; the prints; the four files.
    pass


if __name__ == "__main__":
    main()
