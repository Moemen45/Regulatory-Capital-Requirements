import pytest

from rwa_app.calculator import calculate_ead, calculate_rwa, save_results
from rwa_app.repository import load_exposures
from rwa_app.risk_weights import load_parameter_tables
from tests.conftest import REPORTING_DATE


def _run(conn):
    return calculate_rwa(load_exposures(conn, REPORTING_DATE), load_parameter_tables(conn))


def test_ead_applies_ccf_to_undrawn(conn):
    tables = load_parameter_tables(conn)
    e = {x.loan_id: x for x in load_exposures(conn, REPORTING_DATE)}
    assert calculate_ead(e["L004"], tables) == pytest.approx(6_200_000)   # 5m + 40% x 3m
    assert calculate_ead(e["L011"], tables) == pytest.approx(3_700)       # 3k + 10% x 7k


def test_ead_net_of_specific_provisions(conn):
    tables = load_parameter_tables(conn)
    e = {x.loan_id: x for x in load_exposures(conn, REPORTING_DATE)}
    assert calculate_ead(e["L013"], tables) == pytest.approx(120_000)     # 150k - 30k


def test_total_rwa(conn):
    results = _run(conn)
    assert sum(r.ead for r in results) == pytest.approx(30_826_700)
    assert sum(r.rwa for r in results) == pytest.approx(17_937_775)


def test_results_are_saved_and_rerun_is_idempotent(conn):
    results = _run(conn)
    save_results(conn, results, REPORTING_DATE)
    save_results(conn, results, REPORTING_DATE)   # running twice must not duplicate
    n, total = conn.execute(
        "SELECT COUNT(*), SUM(rwa) FROM rwa_result WHERE reporting_date = ?", (REPORTING_DATE,)
    ).fetchone()
    assert n == 18
    assert total == pytest.approx(17_937_775)
