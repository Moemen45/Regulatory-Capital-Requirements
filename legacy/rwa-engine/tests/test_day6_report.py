import pytest

from rwa_app.calculator import calculate_rwa, save_results
from rwa_app.report import summary_by_class
from rwa_app.repository import load_exposures
from rwa_app.risk_weights import load_parameter_tables
from tests.conftest import REPORTING_DATE


def test_summary_by_class(conn):
    results = calculate_rwa(load_exposures(conn, REPORTING_DATE), load_parameter_tables(conn))
    save_results(conn, results, REPORTING_DATE)
    rows = {r["exposure_class"]: r for r in summary_by_class(conn, REPORTING_DATE)}

    assert len(rows) == 8
    assert rows["CORPORATE"]["n_loans"] == 3
    assert rows["CORPORATE"]["total_rwa"] == pytest.approx(9_350_000)
    assert rows["RETAIL_REGULATORY"]["rw_density"] == pytest.approx(0.75)
    assert rows["DEFAULTED"]["total_ead"] == pytest.approx(488_000)
