"""Validate the synthetic data and semantic layer created for the demo."""

from __future__ import annotations

import argparse
import datetime as dt
import re
from typing import Any

from pyspark.sql import SparkSession

SAFE_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def checked_identifier(value: str, label: str) -> str:
    if not SAFE_IDENTIFIER.fullmatch(value):
        raise SystemExit(f"{label} must contain only letters, numbers, and underscores: {value!r}")
    return value


def scalar(spark: SparkSession, statement: str) -> Any:
    row = spark.sql(statement).first()
    if row is None:
        raise AssertionError(f"Query returned no rows: {statement}")
    return row[0]


def expect_equal(label: str, actual: Any, expected: Any) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")
    print(f"PASS {label}: {actual}")


def expect_between(label: str, actual: float, lower: float, upper: float) -> None:
    if not lower <= actual <= upper:
        raise AssertionError(f"{label}: expected {lower} to {upper}, got {actual}")
    print(f"PASS {label}: {actual}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--as-of-date", required=True)
    args = parser.parse_args()

    catalog = checked_identifier(args.catalog, "catalog")
    schema = checked_identifier(args.schema, "schema")
    try:
        as_of_date = dt.date.fromisoformat(args.as_of_date)
    except ValueError as exc:
        raise SystemExit("--as-of-date must use YYYY-MM-DD") from exc

    spark = SparkSession.builder.getOrCreate()
    fq = f"{catalog}.{schema}"

    # The four summary views must return exactly one row per initiative. The
    # metric view joins use the default many_to_one cardinality, so a summary
    # view that dropped or duplicated an initiative would silently change every
    # governed measure.
    expected_counts = {
        "initiatives": 12,
        "risks": 15,
        "milestones": 48,
        "portfolio_documents": 8,
        "operating_kpi_monthly": 480,
        "v_initiative_progress": 12,
        "v_initiative_risk_summary": 12,
        "v_initiative_milestone_summary": 12,
        "v_initiative_latest_document": 12,
        "v_initiative_current": 12,
    }
    for object_name, expected in expected_counts.items():
        actual = scalar(spark, f"SELECT COUNT(*) FROM {fq}.{object_name}")
        expect_equal(f"row count for {object_name}", actual, expected)

    expect_equal(
        "latest reporting month",
        scalar(spark, f"SELECT MAX(reporting_month) FROM {fq}.v_initiative_current"),
        as_of_date.replace(day=1),
    )
    expect_equal(
        "current health values",
        scalar(spark, f"SELECT COUNT(DISTINCT health) FROM {fq}.v_initiative_current"),
        3,
    )
    expect_equal(
        "initiatives with an owner",
        scalar(
            spark,
            f"SELECT COUNT(*) FROM {fq}.v_initiative_current "
            "WHERE initiative_owner IS NOT NULL",
        ),
        12,
    )

    value_row = spark.sql(
        f"""
        SELECT
          MEASURE(`Initiative Count`) AS initiatives,
          MEASURE(`Target Value`) AS target_value,
          MEASURE(`Forecast Value at Completion`) AS forecast_value,
          MEASURE(`Forecast Attainment`) AS forecast_attainment
        FROM {fq}.mv_value_realization
        """
    ).first()
    if value_row is None:
        raise AssertionError("Value realization metric view returned no rows")
    expect_equal("metric initiative count", value_row.initiatives, 12)
    expect_equal("metric target value", float(value_row.target_value), 645_000_000.0)
    expect_between("metric forecast value", float(value_row.forecast_value), 610_000_000, 620_000_000)
    expect_between("metric forecast attainment", float(value_row.forecast_attainment), 0.94, 0.97)

    delivery_row = spark.sql(
        f"""
        SELECT
          MEASURE(`Red Initiatives`) AS red_initiatives,
          MEASURE(`Open Critical Risks`) AS open_critical_risks,
          MEASURE(`Overdue Critical Risks`) AS overdue_critical_risks
        FROM {fq}.mv_delivery_health
        """
    ).first()
    if delivery_row is None:
        raise AssertionError("Delivery health metric view returned no rows")
    expect_equal("red initiatives", delivery_row.red_initiatives, 4)
    expect_equal("open critical risks", delivery_row.open_critical_risks, 4)
    expect_equal("overdue critical risks", delivery_row.overdue_critical_risks, 4)

    trend_row = spark.sql(
        f"""
        SELECT
          MEASURE(`Realized Value at Period End`) AS realized_at_period_end,
          MEASURE(`Investment at Period End`) AS investment_at_period_end
        FROM {fq}.mv_value_trend
        """
    ).first()
    if trend_row is None:
        raise AssertionError("Value trend metric view returned no rows")
    closing_month = spark.sql(
        f"""
        SELECT
          ROUND(SUM(realized_value_to_date_usd), 2) AS realized,
          ROUND(SUM(investment_to_date_usd), 2) AS investment
        FROM {fq}.portfolio_monthly
        WHERE month_date = DATE'{as_of_date.replace(day=1)}'
        """
    ).first()
    if closing_month is None:
        raise AssertionError("Closing month query returned no rows")
    # Each semiadditive window must take the closing month, not the sum of every
    # month, because the stored records are already cumulative to date. Check
    # every windowed measure, not just one of them.
    expect_equal(
        "semiadditive realized value at period end",
        round(float(trend_row.realized_at_period_end), 2),
        round(float(closing_month.realized), 2),
    )
    expect_equal(
        "semiadditive investment at period end",
        round(float(trend_row.investment_at_period_end), 2),
        round(float(closing_month.investment), 2),
    )

    kpi_rows = spark.sql(
        f"""
        SELECT `Business Unit`, MEASURE(`Actual`) AS actual, MEASURE(`Target`) AS target
        FROM {fq}.mv_operating_performance
        WHERE `KPI` = 'EBITDA margin' AND `Month` = DATE'{as_of_date.replace(day=1)}'
        GROUP BY `Business Unit`
        ORDER BY `Business Unit`
        """
    ).collect()
    expect_equal("business units in operating metric view", len(kpi_rows), 4)

    invalid_value_rows = scalar(
        spark,
        f"""
        SELECT COUNT(*)
        FROM {fq}.v_initiative_current
        WHERE realized_value_to_date_usd < 0
           OR forecast_value_at_completion_usd < 0
           OR target_value_usd <= 0
           OR actual_progress_pct NOT BETWEEN 0 AND 1
        """,
    )
    expect_equal("invalid value or progress rows", invalid_value_rows, 0)

    expect_equal(
        "primary key constraints",
        scalar(
            spark,
            f"""
            SELECT COUNT(*)
            FROM {catalog}.information_schema.table_constraints
            WHERE table_schema = '{schema}'
              AND constraint_type = 'PRIMARY KEY'
            """,
        ),
        1,
    )
    expect_equal(
        "foreign key constraints",
        scalar(
            spark,
            f"""
            SELECT COUNT(*)
            FROM {catalog}.information_schema.table_constraints
            WHERE table_schema = '{schema}'
              AND constraint_type = 'FOREIGN KEY'
            """,
        ),
        3,
    )

    certified_assets = scalar(
        spark,
        f"""
        SELECT COUNT(*)
        FROM {catalog}.information_schema.table_tags
        WHERE catalog_name = '{catalog}'
          AND schema_name = '{schema}'
          AND tag_name = 'system.certification_status'
          AND tag_value = 'certified'
        """,
    )
    if certified_assets == 0:
        # Consistent with the domain tag check below. An identity that cannot
        # apply tags at all should not stop the agents and dashboard from
        # deploying. Partial application is still a failure.
        print(
            "WARNING: no asset carries the certification tag. This identity may not "
            "have APPLY TAG on the schema. The demo still works, but the presenter "
            "should not claim that the assets are certified."
        )
    else:
        expect_equal("certified assets", certified_assets, 12)

    expected_domain_tags = {
        "Enterprise Transformation": 16,
        "Enterprise Transformation/Value Realization": 6,
        "Enterprise Transformation/Delivery and Risk": 9,
        "Enterprise Transformation/Operating Performance": 3,
    }
    domain_tag_rows = spark.sql(
        f"""
        SELECT tag_name, COUNT(*) AS tagged_assets
        FROM {catalog}.information_schema.table_tags
        WHERE schema_name = '{schema}'
          AND tag_name LIKE 'Enterprise Transformation%'
        GROUP BY tag_name
        """
    ).collect()
    actual_domain_tags = {row.tag_name: row.tagged_assets for row in domain_tag_rows}
    if not actual_domain_tags:
        # The governed tag policies could not be created, so no asset carries a
        # domain tag. The demo still works without domains, and the setup job
        # must continue to the Genie Agents. Partial tagging is still a failure.
        print(
            "WARNING: no domain tags are present on the demo assets. The account "
            "could not create the governed tag policies, or this identity cannot "
            "assign them. Genie Agents and the dashboard still work. See "
            "docs/DEPLOYMENT.md to finish the domain setup."
        )
    else:
        expect_equal("domain tag membership", actual_domain_tags, expected_domain_tags)

    print("All data and semantic layer checks passed.")


if __name__ == "__main__":
    main()
