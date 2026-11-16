"""Step 6: write excel/kpi_tables.xlsx with one sheet per table: nodes, passes, distances, networks, assignments and scenarios from
data/processed/, and the six KPI tables from outputs/ as central_exposure, distance_best, frontier, scenario_costs, island_exposure and
site_months.

Arial throughout, bold header row, sensible column widths, frozen header. The dashboard you build by hand in Excel reads the frontier,
assignments, nodes and scenarios sheets.

Functions to look up: pd.ExcelWriter(engine="openpyxl"), DataFrame.to_excel(sheet_name=..., index=False), writer.sheets[name],
openpyxl Font, ws.column_dimensions[...].width, ws.freeze_panes.
"""
import pandas as pd
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

OUT = "outputs"
PROCESSED = "data/processed"
XLSX = "excel/kpi_tables.xlsx"


def main():
    # Build guide, Step 6.
    pass


if __name__ == "__main__":
    main()
