import pytest

from rwa_app.classification import classify
from rwa_app.repository import load_exposures
from tests.conftest import REPORTING_DATE

EXPECTED_CLASS = {
    "L001": "SOVEREIGN",
    "L002": "INSTITUTION",
    "L003": "INSTITUTION",
    "L004": "CORPORATE",
    "L005": "CORPORATE_SME",       # SME (turnover 30m) but exposure 2.5m > 1m
    "L006": "RETAIL_REGULATORY",   # SME, total exposure 600k
    "L007": "RETAIL_REGULATORY",
    "L008": "RESIDENTIAL_RE",
    "L009": "RESIDENTIAL_RE",
    "L010": "RETAIL_REGULATORY",
    "L011": "RETAIL_REGULATORY",
    "L012": "DEFAULTED",           # 120 dpd
    "L013": "DEFAULTED",           # defaulted mortgage: default check comes first
    "L014": "CORPORATE",
    "L015": "CORPORATE",
    "L016": "RETAIL_OTHER",        # individual, 1.2m > 1m
    "L017": "RETAIL_REGULATORY",   # mortgage excluded from the 1m test
    "L018": "DEFAULTED",           # 95 dpd
}


@pytest.mark.parametrize("loan_id, expected", EXPECTED_CLASS.items())
def test_exposure_class(conn, loan_id, expected):
    exposures = {e.loan_id: e for e in load_exposures(conn, REPORTING_DATE)}
    assert classify(exposures[loan_id]) == expected
