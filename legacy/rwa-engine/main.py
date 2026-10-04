"""Run the whole pipeline:  python main.py [--date 2026-09-30] [--reset]"""
import argparse

from rwa_app.calculator import calculate_rwa, save_results
from rwa_app.db import DEFAULT_DB_PATH, get_connection, init_db
from rwa_app.report import export_csv, print_summary, summary_by_class
from rwa_app.repository import load_exposures
from rwa_app.risk_weights import load_parameter_tables


def main() -> None:
    parser = argparse.ArgumentParser(description="Mini Basel III SA credit-risk RWA engine")
    parser.add_argument("--date", default="2026-09-30", help="reporting date (YYYY-MM-DD)")
    parser.add_argument("--reset", action="store_true", help="rebuild the database from sql/")
    args = parser.parse_args()

    first_run = not DEFAULT_DB_PATH.exists()
    conn = get_connection()
    if first_run or args.reset:
        init_db(conn)
        print("Database (re)built from sql/schema.sql + sql/seed.sql")

    exposures = load_exposures(conn, args.date)
    tables = load_parameter_tables(conn)
    results = calculate_rwa(exposures, tables)
    save_results(conn, results, args.date)

    print(f"\nCredit-risk RWA (standardised approach) — reporting date {args.date}\n")
    print_summary(summary_by_class(conn, args.date))
    export_csv(conn, args.date, f"rwa_results_{args.date}.csv")
    print(f"\nLoan-level results written to rwa_results_{args.date}.csv")
    conn.close()


if __name__ == "__main__":
    main()
