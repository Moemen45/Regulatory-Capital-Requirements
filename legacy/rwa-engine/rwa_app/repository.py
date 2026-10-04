"""Day 2 — reading exposures from the database."""
import sqlite3

from rwa_app.models import Exposure

LOAD_EXPOSURES_SQL = """
SELECT
    l.loan_id,
    l.counterparty_id,
    c.counterparty_type,
    c.external_rating,
    c.annual_turnover_eur,
    l.product_type,
    l.drawn_amount,
    l.undrawn_amount,
    l.commitment_type,
    l.property_value,
    l.days_past_due,
    l.specific_provisions,
    SUM(CASE WHEN l.property_value IS NULL
             THEN l.drawn_amount + l.undrawn_amount ELSE 0 END)
        OVER (PARTITION BY l.counterparty_id) AS counterparty_total_non_rre
FROM loan l
JOIN counterparty c ON c.counterparty_id = l.counterparty_id
WHERE l.reporting_date = ?
ORDER BY l.loan_id
"""


def load_exposures(conn: sqlite3.Connection, reporting_date: str) -> list[Exposure]:
    rows = conn.execute(LOAD_EXPOSURES_SQL, (reporting_date,)).fetchall()
    return [Exposure(**dict(row)) for row in rows]
