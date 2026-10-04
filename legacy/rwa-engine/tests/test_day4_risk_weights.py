import pytest

from rwa_app.classification import classify
from rwa_app.repository import load_exposures
from rwa_app.risk_weights import get_cqs, load_parameter_tables, assign_risk_weight, rre_risk_weight
from tests.conftest import REPORTING_DATE

EXPECTED_RW = {
    "L001": 0.20, "L002": 0.50, "L003": 0.75, "L004": 0.50, "L005": 0.85,
    "L006": 0.75, "L007": 0.75, "L008": 0.20, "L009": 0.40, "L010": 0.75,
    "L011": 0.75, "L012": 1.50, "L013": 1.00, "L014": 1.00, "L015": 1.50,
    "L016": 1.00, "L017": 0.75, "L018": 1.00,
}


def test_cqs_mapping(conn):
    t = load_parameter_tables(conn)
    assert get_cqs("AA-", t) == 1
    assert get_cqs("BBB+", t) == 3
    assert get_cqs(None, t) == 0


def test_unknown_rating_raises(conn):
    with pytest.raises(ValueError):
        get_cqs("XYZ", load_parameter_tables(conn))


@pytest.mark.parametrize("ltv, expected", [(0.50, 0.20), (0.5001, 0.25), (0.80, 0.30), (1.20, 0.70)])
def test_ltv_band_edges(conn, ltv, expected):
    assert rre_risk_weight(ltv, load_parameter_tables(conn)) == expected


@pytest.mark.parametrize("loan_id, expected", EXPECTED_RW.items())
def test_risk_weight(conn, loan_id, expected):
    tables = load_parameter_tables(conn)
    e = {x.loan_id: x for x in load_exposures(conn, REPORTING_DATE)}[loan_id]
    assert assign_risk_weight(e, classify(e), tables) == pytest.approx(expected)
