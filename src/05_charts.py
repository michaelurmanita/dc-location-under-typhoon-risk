"""Step 5: draw the four charts from the KPI tables in outputs/ and the processed tables.

1. figures/frontier.png             two panels. Left: every network as a small grey dot, weighted km (x) against weighted passes a
                                    season (y), the frontier networks joined by a line, a box around the frontier networks within 25 km
                                    of the distance-best and a note on the next frontier step. Right: that box enlarged, each frontier
                                    point numbered by its rank, the distance-best (and the base-case choice) as a star, ranks 10 and 14 labelled with their extra km and cut in passes
2. figures/chosen_network_map.png   the 117 nodes on a longitude-latitude plane, bubble area by population, coloured by their site in the
                                    network the base scenario chooses; the three sites as stars, each labelled with its share of the
                                    people and its passes within 100 km in 45 seasons and a season; ax.set_aspect(1 / cos(mean latitude))
3. figures/distance_cost.png        horizontal bars, one per frontier network from rank 2: the extra weighted km against the distance-best,
                                    labelled with the km, the percent and the cut in weighted passes; one colour while the Luzon site
                                    stays in Metro Manila, another after
4. figures/sensitivity.png          a table-like chart: one row per cost per person-km and days per pass (9), one column per cost per
                                    disruption day (5); each cell shaded by the chosen frontier rank and labelled with the rank and the
                                    extra km; the base case outlined

One axis per panel; no secondary axes. Title each chart with the finding and a number from the outputs; say under it what is plotted;
put the source line, with the pass and straight-line caveats and "costs are assumptions", at the bottom. Compute every label from the
tables' values and round it once.

Functions to look up: plt.subplots(1, 2, gridspec_kw={"width_ratios": [...]}), ax.scatter(s=..., alpha=...), ax.plot(marker=...),
plt.Rectangle, ax.add_patch, ax.annotate(xytext=..., textcoords="offset points" or "data", arrowprops=...), ax.set_aspect, math.cos,
math.radians, ax.barh, ax.text, matplotlib.patches.Patch, ax.legend(handles=...), ax.spines[...].set_visible,
plt.savefig(dpi=150, bbox_inches="tight").
"""
import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

OUT = "outputs"
PROCESSED = "data/processed"
FIG = "figures"

# The series palette: the hex codes every reference chart uses. The guide's chart idioms refer to these names.
INK, INK2, MUTED, GRID, SURFACE, AXIS = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb", "#c3c2b7"
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"
GRAY = "#c3c2b7"   # de-emphasis
BLUES = ["#86b6ef", "#6da7ec", "#5598e7", "#3987e5", "#2a78d6", "#256abf", "#184f95", "#0d366b"]   # ordered categories, light to dark
SITE_COLORS = [BLUE, ORANGE, AQUA]   # Luzon, Visayas, Mindanao site


def main():
    # Build guide, Step 5: one function per chart, each saving a PNG.
    pass


if __name__ == "__main__":
    main()
