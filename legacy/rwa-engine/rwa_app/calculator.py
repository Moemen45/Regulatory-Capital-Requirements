"""Day 5 — EAD, RWA, and persisting results."""
import sqlite3

from rwa_app.classification import classify
from rwa_app.models import Exposure, RwaResult
from rwa_app.risk_weights import ParameterTables, assign_risk_weight


def calculate_ead(e: Exposure, tables: ParameterTables) -> float:
    return e.drawn_amount - e.specific_provisions + tables.ccf[e.commitment_type] * e.undrawn_amount


def calculate_rwa(exposures: list[Exposure], tables: ParameterTables) -> list[RwaResult]:
    results = []
    for e in exposures:
        exposure_class = classify(e)
        ead = calculate_ead(e, tables)
        rw = assign_risk_weight(e, exposure_class, tables)
        results.append(RwaResult(e.loan_id, exposure_class, ead, rw, ead * rw))
    return results


def save_results(conn: sqlite3.Connection, results: list[RwaResult], reporting_date: str) -> None:
    conn.execute("DELETE FROM rwa_result WHERE reporting_date = ?", (reporting_date,))
    conn.executemany(
        "INSERT INTO rwa_result (loan_id, reporting_date, exposure_class, ead, risk_weight, rwa) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        [(r.loan_id, reporting_date, r.exposure_class, r.ead, r.risk_weight, r.rwa) for r in results],
    )
    conn.commit()
