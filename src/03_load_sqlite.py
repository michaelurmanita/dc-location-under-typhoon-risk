"""Step 3: load nodes.csv, passes.csv, distances.csv, networks.csv, assignments.csv and scenarios.csv into data/processed/typhoon_dc.db
as tables of the same names, and add three indexes: assignments (network_id, node_id), passes (node_id, month), networks (frontier_rank).

Print each table's row count, then run one sanity query: for each frontier network in assignments, joined to nodes twice (once for the
node, once for its site) and to networks, the nodes, the population, the weighted mean km (SUM(population_2024 * km) / SUM(population_2024),
2 decimals) and the weighted passes (SUM(population_2024 * site's passes_100km / 45.0) / SUM(population_2024), 4 decimals), beside
weighted_km and weighted_passes from networks. The pairs must agree in every row.

Functions to look up: sqlite3.connect, DataFrame.to_sql(if_exists="replace", index=False), con.execute("CREATE INDEX IF NOT EXISTS ..."),
pd.read_sql_query.
"""
import sqlite3

import pandas as pd

OUT = "data/processed"
DB = "data/processed/typhoon_dc.db"
TABLES = ["nodes", "passes", "distances", "networks", "assignments", "scenarios"]


def main():
    # Build guide, Step 3.
    pass


if __name__ == "__main__":
    main()
