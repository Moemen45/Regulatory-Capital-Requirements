"""Day 3 — exposure class identification (simplified Basel III SA waterfall)."""
from rwa_app.models import Exposure

DEFAULT_DPD_THRESHOLD = 90           # more than 90 days past due => defaulted
SME_TURNOVER_LIMIT = 50_000_000      # EUR
RETAIL_EXPOSURE_LIMIT = 1_000_000    # EUR, aggregate per counterparty excl. RRE

SOVEREIGN = "SOVEREIGN"
INSTITUTION = "INSTITUTION"
CORPORATE = "CORPORATE"
CORPORATE_SME = "CORPORATE_SME"
RETAIL_REGULATORY = "RETAIL_REGULATORY"
RETAIL_OTHER = "RETAIL_OTHER"
RESIDENTIAL_RE = "RESIDENTIAL_RE"
DEFAULTED = "DEFAULTED"


def is_defaulted(e: Exposure) -> bool:
    return e.days_past_due > DEFAULT_DPD_THRESHOLD


def is_secured_by_rre(e: Exposure) -> bool:
    return e.property_value is not None and e.property_value > 0


def is_sme(e: Exposure) -> bool:
    return (
        e.counterparty_type == "CORPORATE"
        and e.annual_turnover_eur is not None
        and e.annual_turnover_eur <= SME_TURNOVER_LIMIT
    )


def meets_retail_size_limit(e: Exposure) -> bool:
    return e.counterparty_total_non_rre <= RETAIL_EXPOSURE_LIMIT


def classify(e: Exposure) -> str:
    if is_defaulted(e):
        return DEFAULTED
    if is_secured_by_rre(e):
        return RESIDENTIAL_RE
    if e.counterparty_type == "SOVEREIGN":
        return SOVEREIGN
    if e.counterparty_type == "INSTITUTION":
        return INSTITUTION
    if e.counterparty_type == "INDIVIDUAL":
        return RETAIL_REGULATORY if meets_retail_size_limit(e) else RETAIL_OTHER
    if e.counterparty_type == "CORPORATE":
        if is_sme(e):
            return RETAIL_REGULATORY if meets_retail_size_limit(e) else CORPORATE_SME
        return CORPORATE
    raise ValueError(f"{e.loan_id}: unknown counterparty_type {e.counterparty_type!r}")
