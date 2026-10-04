"""Day 6 — summary report straight from the results table."""
import csv
import sqlite3
from pathlib import Path

SUMMARY_SQL = """
SELECT exposure_class,
       COUNT(*)                 AS n_loans,
       SUM(ead)                 AS total_ead,
       SUM(rwa)                 AS total_rwa,
       SUM(rwa) / SUM(ead)      AS rw_density
FROM rwa_result
WHERE reporting_date = ?
GROUP BY exposure_class
ORDER BY total_rwa DESC
"""


def summary_by_class(conn: sqlite3.Connection, reporting_date: str) -> list[dict]:
    return [dict(r) for r in conn.execute(SUMMARY_SQL, (reporting_date,))]


def print_summary(rows: list[dict]) -> None:
    header = f"{'Exposure class':<20}{'Loans':>6}{'EAD':>16}{'RWA':>16}{'RW dens.':>10}"
    print(header)
    print("-" * len(header))
    for r in rows:
        print(f"{r['exposure_class']:<20}{r['n_loans']:>6}{r['total_ead']:>16,.0f}"
              f"{r['total_rwa']:>16,.0f}{r['rw_density']:>10.1%}")
    ead = sum(r["total_ead"] for r in rows)
    rwa = sum(r["total_rwa"] for r in rows)
    print("-" * len(header))
    print(f"{'TOTAL':<20}{sum(r['n_loans'] for r in rows):>6}{ead:>16,.0f}{rwa:>16,.0f}{rwa / ead:>10.1%}")


def export_csv(conn: sqlite3.Connection, reporting_date: str, path: Path | str) -> None:
    rows = conn.execute(
        "SELECT loan_id, exposure_class, ead, risk_weight, rwa FROM rwa_result "
        "WHERE reporting_date = ? ORDER BY loan_id", (reporting_date,)
    ).fetchall()
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["loan_id", "exposure_class", "ead", "risk_weight", "rwa"])
        writer.writerows([tuple(r) for r in rows])
