from rwa_app.repository import load_exposures
from tests.conftest import REPORTING_DATE


def _by_id(conn):
    return {e.loan_id: e for e in load_exposures(conn, REPORTING_DATE)}


def test_loads_all_loans_for_the_date(conn):
    assert len(load_exposures(conn, REPORTING_DATE)) == 18


def test_unknown_date_returns_nothing(conn):
    assert load_exposures(conn, "1999-12-31") == []


def test_counterparty_fields_are_joined(conn):
    e = _by_id(conn)["L004"]
    assert e.counterparty_type == "CORPORATE"
    assert e.external_rating == "A-"
    assert e.annual_turnover_eur == 400_000_000


def test_unrated_is_none(conn):
    assert _by_id(conn)["L003"].external_rating is None


def test_counterparty_total_sums_all_non_rre_loans(conn):
    # C006 has L006 (400k drawn) and L007 (50k drawn + 150k undrawn)
    exps = _by_id(conn)
    assert exps["L006"].counterparty_total_non_rre == 600_000
    assert exps["L007"].counterparty_total_non_rre == 600_000


def test_counterparty_total_excludes_mortgages(conn):
    # C007 has a 180k mortgage (L008) and a 20k consumer loan (L017)
    exps = _by_id(conn)
    assert exps["L017"].counterparty_total_non_rre == 20_000
