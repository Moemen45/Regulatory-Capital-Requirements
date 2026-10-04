"""Plain data containers. Provided complete."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Exposure:
    """One loan joined with its counterparty — the input to the RWA engine."""
    loan_id: str
    counterparty_id: str
    counterparty_type: str            # SOVEREIGN / INSTITUTION / CORPORATE / INDIVIDUAL
    external_rating: str | None       # None = unrated
    annual_turnover_eur: float | None
    product_type: str
    drawn_amount: float
    undrawn_amount: float
    commitment_type: str              # NONE / COMMITTED / UNCONDITIONALLY_CANCELLABLE
    property_value: float | None      # not None => secured by residential property
    days_past_due: int
    specific_provisions: float
    counterparty_total_non_rre: float # sum of drawn+undrawn over the counterparty's non-RRE loans


@dataclass(frozen=True)
class RwaResult:
    loan_id: str
    exposure_class: str
    ead: float
    risk_weight: float
    rwa: float
