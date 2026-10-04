-- =====================================================================
-- RWA mini-engine — schema (SQLite; written to be easy to port to Oracle)
-- =====================================================================
DROP TABLE IF EXISTS rwa_result;
DROP TABLE IF EXISTS loan;
DROP TABLE IF EXISTS counterparty;
DROP TABLE IF EXISTS rating_cqs;
DROP TABLE IF EXISTS risk_weight;
DROP TABLE IF EXISTS ccf;
DROP TABLE IF EXISTS rre_ltv_band;

-- ---------- Business data (what a bank's source systems would provide) ----------
CREATE TABLE counterparty (
    counterparty_id      TEXT PRIMARY KEY,
    name                 TEXT NOT NULL,
    counterparty_type    TEXT NOT NULL
        CHECK (counterparty_type IN ('SOVEREIGN','INSTITUTION','CORPORATE','INDIVIDUAL')),
    country              TEXT NOT NULL,
    external_rating      TEXT,          -- S&P-style; NULL = unrated
    annual_turnover_eur  REAL           -- corporates only; used for the SME test
);

CREATE TABLE loan (
    loan_id              TEXT PRIMARY KEY,
    counterparty_id      TEXT NOT NULL REFERENCES counterparty(counterparty_id),
    reporting_date       TEXT NOT NULL,  -- ISO date
    product_type         TEXT NOT NULL,
    currency             TEXT NOT NULL DEFAULT 'EUR',
    drawn_amount         REAL NOT NULL,
    undrawn_amount       REAL NOT NULL DEFAULT 0,
    commitment_type      TEXT NOT NULL DEFAULT 'NONE',  -- NONE / COMMITTED / UNCONDITIONALLY_CANCELLABLE
    property_value       REAL,           -- filled only when secured by residential property
    days_past_due        INTEGER NOT NULL DEFAULT 0,
    specific_provisions  REAL NOT NULL DEFAULT 0
);

-- ---------- Regulatory parameter tables (Basel III SA, BCBS CRE20 — simplified) ----------
CREATE TABLE rating_cqs (            -- external rating -> credit quality step
    rating  TEXT PRIMARY KEY,
    cqs     INTEGER NOT NULL
);

CREATE TABLE risk_weight (           -- cqs 0 = unrated
    exposure_class  TEXT    NOT NULL,
    cqs             INTEGER NOT NULL,
    risk_weight     REAL    NOT NULL,
    PRIMARY KEY (exposure_class, cqs)
);

CREATE TABLE ccf (                   -- credit conversion factors for undrawn amounts
    commitment_type TEXT PRIMARY KEY,
    ccf             REAL NOT NULL
);

CREATE TABLE rre_ltv_band (          -- residential real estate, whole-loan approach
    ltv_upper    REAL PRIMARY KEY,   -- band upper bound (inclusive)
    risk_weight  REAL NOT NULL
);

-- ---------- Output ----------
CREATE TABLE rwa_result (
    loan_id          TEXT PRIMARY KEY REFERENCES loan(loan_id),
    reporting_date   TEXT NOT NULL,
    exposure_class   TEXT NOT NULL,
    ead              REAL NOT NULL,
    risk_weight      REAL NOT NULL,
    rwa              REAL NOT NULL,
    calculated_at    TEXT NOT NULL DEFAULT (datetime('now'))
);
