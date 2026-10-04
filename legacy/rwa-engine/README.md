# Legacy capital calculator (as-is system) — DO NOT MODIFY

Lumen Bank's in-house credit-risk RWA calculator, inherited from a previous team.
Kept unchanged as the **as-is system** for discovery and as the baseline for the
Release 1 parallel run.

- Rules: Basel framework standardised approach (BCBS CRE20), simplified — not CRR3.
- Storage: local SQLite file built from `sql/schema.sql` and `sql/seed.sql`.
- Scope: loans only. No securities, no derivatives, no credit risk mitigation.
- Documentation: none beyond this file, the code and the tests.

## Run (from this folder)

    uv run python main.py --reset     # rebuilds rwa.db, prints the summary, writes a CSV
    uv run pytest                     # 53 tests

## Baseline (seed data, reporting date 2026-09-30)

Total EAD 30,826,700 · Total RWA 17,937,775 · RW density 58.2 %
