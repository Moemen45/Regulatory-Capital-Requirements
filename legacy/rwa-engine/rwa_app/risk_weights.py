"""Day 4 — loading parameter tables and assigning risk weights."""
import sqlite3
from dataclasses import dataclass

from rwa_app.classification import DEFAULTED, RESIDENTIAL_RE, is_secured_by_rre
from rwa_app.models import Exposure

UNRATED_CQS = 0
DEFAULTED_PROVISION_THRESHOLD = 0.20


@dataclass
class ParameterTables:
    rating_to_cqs: dict[str, int]
    risk_weights: dict[tuple[str, int], float]   # (exposure_class, cqs) -> rw
    ccf: dict[str, float]                        # commitment_type -> ccf
    ltv_bands: list[tuple[float, float]]         # [(ltv_upper, rw)] sorted ascending


def load_parameter_tables(conn: sqlite3.Connection) -> ParameterTables:
    return ParameterTables(
        rating_to_cqs={r["rating"]: r["cqs"] for r in conn.execute("SELECT rating, cqs FROM rating_cqs")},
        risk_weights={
            (r["exposure_class"], r["cqs"]): r["risk_weight"]
            for r in conn.execute("SELECT exposure_class, cqs, risk_weight FROM risk_weight")
        },
        ccf={r["commitment_type"]: r["ccf"] for r in conn.execute("SELECT commitment_type, ccf FROM ccf")},
        ltv_bands=[
            (r["ltv_upper"], r["risk_weight"])
            for r in conn.execute("SELECT ltv_upper, risk_weight FROM rre_ltv_band ORDER BY ltv_upper")
        ],
    )


def get_cqs(rating: str | None, tables: ParameterTables) -> int:
    if rating is None:
        return UNRATED_CQS
    try:
        return tables.rating_to_cqs[rating]
    except KeyError:
        raise ValueError(f"Unknown rating {rating!r}") from None


def ltv(e: Exposure) -> float:
    return (e.drawn_amount + e.undrawn_amount) / e.property_value


def rre_risk_weight(ltv_value: float, tables: ParameterTables) -> float:
    for upper, rw in tables.ltv_bands:
        if ltv_value <= upper:
            return rw
    raise ValueError(f"LTV {ltv_value:.2%} above highest band")


def defaulted_risk_weight(e: Exposure) -> float:
    if is_secured_by_rre(e):
        return 1.00
    provision_ratio = e.specific_provisions / e.drawn_amount if e.drawn_amount else 0.0
    return 1.00 if provision_ratio >= DEFAULTED_PROVISION_THRESHOLD else 1.50


def assign_risk_weight(e: Exposure, exposure_class: str, tables: ParameterTables) -> float:
    if exposure_class == DEFAULTED:
        return defaulted_risk_weight(e)
    if exposure_class == RESIDENTIAL_RE:
        return rre_risk_weight(ltv(e), tables)
    cqs = get_cqs(e.external_rating, tables)
    key = (exposure_class, cqs)
    if key not in tables.risk_weights:          # e.g. retail: rating is irrelevant
        key = (exposure_class, UNRATED_CQS)
    return tables.risk_weights[key]
