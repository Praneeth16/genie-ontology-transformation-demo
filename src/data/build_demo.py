"""Build the synthetic data and governed semantics for the demo.

The data represents Northstar Group, a fictional multi-business enterprise.
The script is deterministic for a fixed as-of date and safe to rerun.
"""

from __future__ import annotations

import argparse
import re

from pyspark.sql import SparkSession

SAFE_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def checked_identifier(value: str, label: str) -> str:
    if not SAFE_IDENTIFIER.fullmatch(value):
        raise SystemExit(f"{label} must contain only letters, numbers, and underscores: {value!r}")
    return value


def run(spark: SparkSession, statement: str, label: str) -> None:
    spark.sql(statement)
    print(f"Created {label}")


def try_sql(spark: SparkSession, statement: str, label: str) -> None:
    try:
        spark.sql(statement)
        print(f"Applied {label}")
    except Exception as exc:  # noqa: BLE001  # Preview features fail with several Spark errors.
        print(f"WARNING: Could not apply {label}: {exc}")


def metric_view_sql(name: str, source: str, comment: str, dimensions: str, measures: str) -> str:
    return f"""CREATE OR REPLACE VIEW {name}
WITH METRICS
LANGUAGE YAML
AS $$
version: 1.1
source: {source}
comment: |-
  {comment}
dimensions:
{dimensions}
measures:
{measures}
$$"""


def ensure_table_tag(
    spark: SparkSession,
    catalog: str,
    schema: str,
    object_type: str,
    object_name: str,
    tag_key: str,
) -> None:
    existing = spark.sql(
        f"""
        SELECT 1
        FROM {catalog}.information_schema.table_tags
        WHERE catalog_name = '{catalog}'
          AND schema_name = '{schema}'
          AND table_name = '{object_name}'
          AND tag_name = '{tag_key}'
        LIMIT 1
        """
    ).count()
    if existing:
        print(f"Domain tag already exists on {object_name}: {tag_key}")
        return

    try:
        spark.sql(
            f"SET TAG ON {object_type} {catalog}.{schema}.{object_name} `{tag_key}`"
        )
    except Exception as exc:  # noqa: BLE001  # Tag policies can be missing in restricted accounts.
        print(f"WARNING: Could not apply domain tag on {object_name}: {tag_key}: {exc}")
        return
    print(f"Applied domain tag on {object_name}: {tag_key}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--as-of-date", required=True)
    args = parser.parse_args()

    catalog = checked_identifier(args.catalog, "catalog")
    schema = checked_identifier(args.schema, "schema")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.as_of_date):
        raise SystemExit("--as-of-date must use YYYY-MM-DD")

    spark = SparkSession.builder.getOrCreate()
    fq = f"{catalog}.{schema}"
    as_of = args.as_of_date

    run(
        spark,
        f"""
        CREATE OR REPLACE TABLE {fq}.initiatives
        COMMENT 'Synthetic Northstar Group transformation initiatives. One row per initiative.'
        AS
        SELECT * FROM VALUES
          ('TVO-001', 'Pricing excellence', 'Commercial growth', 'Growth', 'Consumer Products', 'North America',
           'Elena Torres', 'Marcus Lee', 'Revenue', 62000000D, 8000000D,
           DATE'2025-01-01', DATE'2026-12-31', 0.92D, 0.96D, 0.91D, 24, 'Amber'),
          ('TVO-002', 'Strategic sourcing', 'Cost transformation', 'Procurement', 'Corporate', 'Global',
           'Amina Yusuf', 'Priya Nair', 'Cost', 88000000D, 10000000D,
           DATE'2025-01-01', DATE'2026-09-30', 1.06D, 1.04D, 1.03D, 0, 'Green'),
          ('TVO-003', 'Network footprint redesign', 'Operations', 'Supply chain', 'Industrial Systems', 'Europe',
           'Jonas Becker', 'Sofia Marin', 'Cost', 74000000D, 22000000D,
           DATE'2025-02-01', DATE'2026-11-30', 0.83D, 0.88D, 0.79D, 68, 'Red'),
          ('TVO-004', 'Demand planning transformation', 'Operations', 'Supply chain', 'Consumer Products', 'Asia Pacific',
           'Mei Chen', 'Arjun Rao', 'Working capital', 41000000D, 12000000D,
           DATE'2025-03-01', DATE'2026-10-31', 0.87D, 0.91D, 0.82D, 52, 'Red'),
          ('TVO-005', 'Shared services consolidation', 'Operating model', 'Finance', 'Corporate', 'Global',
           'David Kim', 'Nadia Petrova', 'Cost', 55000000D, 18000000D,
           DATE'2025-01-01', DATE'2026-12-31', 0.78D, 0.84D, 0.75D, 90, 'Red'),
          ('TVO-006', 'Cloud cost optimization', 'Technology', 'Technology', 'Digital Services', 'Global',
           'Ravi Shah', 'Lina Gomez', 'Cost', 36000000D, 5000000D,
           DATE'2025-04-01', DATE'2026-06-30', 1.08D, 1.06D, 1.02D, 0, 'Green'),
          ('TVO-007', 'Sales force effectiveness', 'Commercial growth', 'Sales', 'Industrial Systems', 'North America',
           'Elena Torres', 'Noah Williams', 'Revenue', 48000000D, 14000000D,
           DATE'2025-05-01', DATE'2027-01-31', 0.93D, 0.95D, 0.88D, 30, 'Amber'),
          ('TVO-008', 'Working capital reset', 'Cash', 'Finance', 'Industrial Systems', 'Europe',
           'David Kim', 'Hannah Evans', 'Working capital', 52000000D, 6000000D,
           DATE'2025-02-01', DATE'2026-12-31', 0.97D, 1.00D, 0.96D, 12, 'Green'),
          ('TVO-009', 'Field service productivity', 'Operations', 'Service', 'Digital Services', 'Asia Pacific',
           'Jonas Becker', 'Kenji Sato', 'Cost', 38000000D, 9000000D,
           DATE'2025-06-01', DATE'2027-02-28', 0.89D, 0.94D, 0.85D, 35, 'Amber'),
          ('TVO-010', 'Customer retention program', 'Commercial growth', 'Customer', 'Digital Services', 'Global',
           'Mei Chen', 'Fatima Rahman', 'Revenue', 45000000D, 11000000D,
           DATE'2025-03-01', DATE'2026-12-31', 0.95D, 0.98D, 0.93D, 15, 'Amber'),
          ('TVO-011', 'Product portfolio simplification', 'Portfolio', 'Product', 'Consumer Products', 'Global',
           'Amina Yusuf', 'Oliver Grant', 'Margin', 67000000D, 7000000D,
           DATE'2025-01-01', DATE'2026-10-31', 1.02D, 1.02D, 0.98D, 0, 'Green'),
          ('TVO-012', 'Service operations automation', 'Technology', 'Service', 'Digital Services', 'Europe',
           'Ravi Shah', 'Claire Dubois', 'Cost', 39000000D, 15000000D,
           DATE'2025-07-01', DATE'2027-03-31', 0.72D, 0.81D, 0.69D, 105, 'Red')
        AS t(
          initiative_id, initiative_name, strategic_theme, workstream, business_unit, region,
          executive_sponsor, initiative_owner, value_type, target_value_usd, approved_investment_usd,
          start_date, planned_end_date, realization_factor, forecast_factor, execution_factor,
          days_slipped, health
        )
        """,
        f"{fq}.initiatives",
    )

    run(
        spark,
        f"""
        CREATE OR REPLACE TABLE {fq}.portfolio_monthly
        COMMENT 'Monthly planned, realized, forecast, investment, and delivery measures by initiative.'
        AS
        WITH expanded AS (
          SELECT i.*, month_date,
                 MONTHS_BETWEEN(month_date, DATE_TRUNC('MONTH', start_date)) + 1 AS elapsed_months,
                 GREATEST(MONTHS_BETWEEN(DATE_TRUNC('MONTH', planned_end_date),
                                         DATE_TRUNC('MONTH', start_date)) + 1, 1) AS duration_months
          FROM {fq}.initiatives i
          LATERAL VIEW EXPLODE(
            SEQUENCE(DATE_TRUNC('MONTH', start_date), DATE_TRUNC('MONTH', DATE'{as_of}'), INTERVAL 1 MONTH)
          ) months AS month_date
        ),
        progress AS (
          SELECT *,
                 LEAST(GREATEST(elapsed_months / duration_months, 0), 1) AS planned_progress_pct,
                 LEAST(
                   GREATEST(
                     (elapsed_months / duration_months) * execution_factor
                     * (0.92 + 0.08 * LEAST(elapsed_months / duration_months, 1)),
                     0
                   ),
                   1
                 ) AS actual_progress_pct
          FROM expanded
        )
        SELECT
          initiative_id,
          CAST(month_date AS DATE) AS month_date,
          ROUND(planned_progress_pct, 4) AS planned_progress_pct,
          ROUND(actual_progress_pct, 4) AS actual_progress_pct,
          ROUND(target_value_usd * planned_progress_pct, 2) AS planned_value_to_date_usd,
          ROUND(
            target_value_usd * planned_progress_pct * realization_factor
            * (0.95 + 0.05 * LEAST(elapsed_months / duration_months, 1)),
            2
          ) AS realized_value_to_date_usd,
          ROUND(target_value_usd * forecast_factor, 2) AS forecast_value_at_completion_usd,
          ROUND(
            approved_investment_usd * actual_progress_pct
            * CASE health WHEN 'Red' THEN 1.10 WHEN 'Amber' THEN 1.03 ELSE 0.96 END,
            2
          ) AS investment_to_date_usd,
          ROUND(
            0.55 + 0.40 * LEAST(actual_progress_pct, 1)
            - CASE health WHEN 'Red' THEN 0.20 WHEN 'Amber' THEN 0.08 ELSE 0 END,
            3
          ) AS benefit_confidence_score
        FROM progress
        """,
        f"{fq}.portfolio_monthly",
    )

    run(
        spark,
        f"""
        CREATE OR REPLACE TABLE {fq}.risks
        COMMENT 'Open and closed delivery risks for the transformation portfolio.'
        AS
        SELECT * FROM VALUES
          ('RSK-001', 'TVO-003', 'Site consultation delay', 'Change adoption', 'Critical', 'Mitigating',
           DATE'2026-04-12', DATE'2026-07-15', 'Sofia Marin',
           'Complete union consultation and agree a phased site transition.', 'Network steering memo'),
          ('RSK-002', 'TVO-003', 'Closure cost estimate is stale', 'Financial', 'High', 'Open',
           DATE'2026-05-02', DATE'2026-08-15', 'Marcus Lee',
           'Refresh site exit costs before the September investment committee.', 'Network finance note'),
          ('RSK-003', 'TVO-004', 'Product hierarchy mismatch', 'Data', 'Critical', 'Mitigating',
           DATE'2026-03-18', DATE'2026-07-31', 'Arjun Rao',
           'Reconcile product identifiers across ERP and demand planning systems.', 'Demand planning data review'),
          ('RSK-004', 'TVO-004', 'Forecast adoption below target', 'Change adoption', 'High', 'Open',
           DATE'2026-06-01', DATE'2026-09-15', 'Mei Chen',
           'Add planner coaching and track override quality by market.', 'Planning adoption review'),
          ('RSK-005', 'TVO-005', 'Country design decisions are late', 'Decision', 'Critical', 'Open',
           DATE'2026-02-20', DATE'2026-06-30', 'Nadia Petrova',
           'Escalate five unresolved country scope decisions to the executive sponsor.', 'Shared services committee'),
          ('RSK-006', 'TVO-005', 'Finance process variants remain high', 'Process', 'High', 'Mitigating',
           DATE'2026-05-10', DATE'2026-09-30', 'David Kim',
           'Retire local variants before the next migration wave.', 'Finance design authority'),
          ('RSK-007', 'TVO-012', 'Automation vendor integration failed', 'Technology', 'Critical', 'Open',
           DATE'2026-04-25', DATE'2026-07-20', 'Claire Dubois',
           'Replace the custom connector with the supported event interface.', 'Automation recovery plan'),
          ('RSK-008', 'TVO-012', 'Control evidence is incomplete', 'Compliance', 'High', 'Mitigating',
           DATE'2026-06-11', DATE'2026-09-10', 'Ravi Shah',
           'Add evidence capture to the automated workflow before scale rollout.', 'Controls review'),
          ('RSK-009', 'TVO-007', 'Territory model approval is late', 'Decision', 'High', 'Mitigating',
           DATE'2026-05-19', DATE'2026-08-20', 'Noah Williams',
           'Approve the final territory exceptions for two regions.', 'Sales design note'),
          ('RSK-010', 'TVO-009', 'Mobile workflow latency', 'Technology', 'High', 'Open',
           DATE'2026-06-23', DATE'2026-09-05', 'Kenji Sato',
           'Move the inspection cache closer to field users.', 'Field service weekly report'),
          ('RSK-011', 'TVO-010', 'Retention offer margin erosion', 'Financial', 'Medium', 'Mitigating',
           DATE'2026-07-04', DATE'2026-10-01', 'Fatima Rahman',
           'Set offer guardrails by customer segment.', 'Retention economics review'),
          ('RSK-012', 'TVO-001', 'Discount guardrails vary by channel', 'Process', 'Medium', 'Open',
           DATE'2026-06-14', DATE'2026-09-20', 'Marcus Lee',
           'Use one approval policy across direct and partner channels.', 'Pricing council minutes'),
          ('RSK-013', 'TVO-002', 'Supplier baseline challenge', 'Data', 'Low', 'Closed',
           DATE'2026-01-11', DATE'2026-03-31', 'Priya Nair',
           'Reconcile purchase price variance with the signed sourcing baseline.', 'Sourcing benefits review'),
          ('RSK-014', 'TVO-008', 'Inventory policy ownership', 'Operating model', 'Medium', 'Closed',
           DATE'2026-02-15', DATE'2026-05-30', 'Hannah Evans',
           'Assign policy ownership to business unit finance leads.', 'Working capital review'),
          ('RSK-015', 'TVO-011', 'SKU exit communication', 'Customer', 'Low', 'Mitigating',
           DATE'2026-07-01', DATE'2026-10-15', 'Oliver Grant',
           'Notify customers before the final SKU retirement wave.', 'Portfolio council update')
        AS t(
          risk_id, initiative_id, risk_title, risk_category, severity, risk_status,
          opened_date, due_date, risk_owner, mitigation_action, source_document
        )
        """,
        f"{fq}.risks",
    )

    run(
        spark,
        f"""
        CREATE OR REPLACE TABLE {fq}.milestones
        COMMENT 'Four standard delivery milestones for every transformation initiative.'
        AS
        WITH latest AS (
          SELECT p.*
          FROM {fq}.portfolio_monthly p
          QUALIFY ROW_NUMBER() OVER (PARTITION BY initiative_id ORDER BY month_date DESC) = 1
        ),
        expanded AS (
          SELECT i.*, l.actual_progress_pct, milestone_number
          FROM {fq}.initiatives i
          JOIN latest l USING (initiative_id)
          LATERAL VIEW EXPLODE(SEQUENCE(1, 4)) m AS milestone_number
        )
        SELECT
          CONCAT(initiative_id, '-M', milestone_number) AS milestone_id,
          initiative_id,
          CASE milestone_number
            WHEN 1 THEN 'Design approved'
            WHEN 2 THEN 'Pilot complete'
            WHEN 3 THEN 'Scale rollout complete'
            ELSE 'Benefits validated'
          END AS milestone_name,
          DATE_ADD(
            start_date,
            CAST(DATEDIFF(planned_end_date, start_date) * milestone_number / 4 AS INT)
          ) AS planned_date,
          CASE
            WHEN actual_progress_pct >= milestone_number / 4D THEN DATE_ADD(
              DATE_ADD(
                start_date,
                CAST(DATEDIFF(planned_end_date, start_date) * milestone_number / 4 AS INT)
              ),
              CAST(days_slipped * milestone_number / 4 AS INT)
            )
          END AS actual_date,
          CASE
            WHEN actual_progress_pct >= milestone_number / 4D THEN 'Complete'
            WHEN DATE_ADD(
              start_date,
              CAST(DATEDIFF(planned_end_date, start_date) * milestone_number / 4 AS INT)
            ) < DATE'{as_of}' THEN 'Overdue'
            WHEN DATE_ADD(
              start_date,
              CAST(DATEDIFF(planned_end_date, start_date) * milestone_number / 4 AS INT)
            ) <= DATE_ADD(DATE'{as_of}', 60) THEN 'Due soon'
            ELSE 'Upcoming'
          END AS milestone_status,
          initiative_owner AS milestone_owner
        FROM expanded
        """,
        f"{fq}.milestones",
    )

    run(
        spark,
        f"""
        CREATE OR REPLACE TABLE {fq}.portfolio_documents
        COMMENT 'Synthetic unstructured context from steering notes, reviews, and decision records.'
        AS
        SELECT * FROM VALUES
          ('DOC-001', 'TVO-003', 'Network steering memo', 'Steering memo', DATE'2026-08-18',
           'The network program remains red. Site consultation is 68 days behind plan. The committee asked for a phased transition and a refreshed closure cost estimate before the September investment decision.',
           'Transformation Office', 'Confidential synthetic demo content'),
          ('DOC-002', 'TVO-004', 'Demand planning data review', 'Data review', DATE'2026-08-12',
           'Forecast accuracy improved in two markets, but product hierarchy mismatches still prevent one regional rollout. The team must reconcile ERP and planning identifiers before scale approval.',
           'Data Office', 'Confidential synthetic demo content'),
          ('DOC-003', 'TVO-005', 'Shared services committee', 'Committee minutes', DATE'2026-08-21',
           'Five country scope decisions remain open. The unresolved choices block migration design and put forecast savings at risk. The executive sponsor will decide the remaining scope by 15 September.',
           'Finance Transformation', 'Confidential synthetic demo content'),
          ('DOC-004', 'TVO-012', 'Automation recovery plan', 'Recovery plan', DATE'2026-08-25',
           'The custom vendor connector failed integration testing. The team will move to the supported event interface, add control evidence capture, and repeat the pilot before any wider rollout.',
           'Technology Office', 'Confidential synthetic demo content'),
          ('DOC-005', 'TVO-002', 'Sourcing benefits review', 'Benefits review', DATE'2026-08-10',
           'Strategic sourcing is ahead of plan. Signed supplier actions support the forecast. Finance confirmed the purchase price baseline and the next review will focus on benefit sustainability.',
           'Procurement', 'Confidential synthetic demo content'),
          ('DOC-006', 'TVO-011', 'Portfolio council update', 'Council update', DATE'2026-08-17',
           'Product simplification remains green. Margin benefits are ahead of plan. The main remaining action is customer communication before the final retirement wave.',
           'Product Office', 'Confidential synthetic demo content'),
          ('DOC-007', 'TVO-001', 'Pricing council minutes', 'Council minutes', DATE'2026-08-19',
           'Pricing value is close to plan. Channel discount rules still differ, so the council asked for one approval policy and one definition of realized pricing value.',
           'Commercial Office', 'Confidential synthetic demo content'),
          ('DOC-008', NULL, 'Northstar transformation charter', 'Program charter', DATE'2025-01-05',
           'Northstar 2027 will track value through approved finance baselines. Initiative owners report delivery. Finance owns benefit validation. The transformation office reports target, plan, realized value, forecast, investment, risk, and decision status.',
           'Transformation Office', 'Confidential synthetic demo content')
        AS t(
          document_id, initiative_id, document_title, document_type, document_date,
          document_text, document_owner, classification
        )
        """,
        f"{fq}.portfolio_documents",
    )

    run(
        spark,
        f"""
        CREATE OR REPLACE TABLE {fq}.operating_kpi_monthly
        COMMENT 'Monthly operating KPIs that connect transformation work to business outcomes.'
        AS
        WITH kpis AS (
          SELECT * FROM VALUES
            ('EBITDA margin', 'Percent', 'HIGHER_BETTER', 14.0D, 18.0D),
            ('Forecast accuracy', 'Percent', 'HIGHER_BETTER', 68.0D, 85.0D),
            ('On time delivery', 'Percent', 'HIGHER_BETTER', 82.0D, 94.0D),
            ('Net promoter score', 'Points', 'HIGHER_BETTER', 31.0D, 48.0D),
            ('Working capital days', 'Days', 'LOWER_BETTER', 62.0D, 48.0D),
            ('Cost to serve', 'USD per order', 'LOWER_BETTER', 29.0D, 22.0D)
          AS t(kpi_name, unit, direction, baseline_value, target_value)
        ),
        units AS (
          SELECT * FROM VALUES
            ('Consumer Products', -0.02D),
            ('Industrial Systems', 0.01D),
            ('Digital Services', -0.05D),
            ('Corporate', 0.03D)
          AS t(business_unit, performance_offset)
        ),
        months AS (
          SELECT EXPLODE(
            SEQUENCE(DATE'2025-01-01', DATE_TRUNC('MONTH', DATE'{as_of}'), INTERVAL 1 MONTH)
          ) AS month_date
        ),
        expanded AS (
          SELECT k.*, u.*, m.month_date,
                 MONTHS_BETWEEN(m.month_date, DATE'2025-01-01') / 19D AS progress
          FROM kpis k CROSS JOIN units u CROSS JOIN months m
        )
        SELECT
          CAST(month_date AS DATE) AS month_date,
          business_unit,
          kpi_name,
          unit,
          direction,
          target_value,
          ROUND(
            CASE direction
              WHEN 'HIGHER_BETTER' THEN baseline_value
                + (target_value - baseline_value)
                  * LEAST(GREATEST(progress + performance_offset, 0), 1)
              ELSE baseline_value
                - (baseline_value - target_value)
                  * LEAST(GREATEST(progress + performance_offset, 0), 1)
            END
            + CASE
                WHEN unit = 'Percent' THEN SIN(MONTH(month_date)) * 0.6
                WHEN unit = 'Points' THEN SIN(MONTH(month_date)) * 1.2
                ELSE SIN(MONTH(month_date)) * 0.4
              END,
            2
          ) AS actual_value
        FROM expanded
        """,
        f"{fq}.operating_kpi_monthly",
    )

    run(
        spark,
        f"""
        CREATE OR REPLACE VIEW {fq}.v_initiative_current
        COMMENT 'One current row per initiative with value, delivery, risk, and decision context.'
        AS
        WITH latest AS (
          SELECT p.*
          FROM {fq}.portfolio_monthly p
          QUALIFY ROW_NUMBER() OVER (PARTITION BY initiative_id ORDER BY month_date DESC) = 1
        ),
        risk_summary AS (
          SELECT initiative_id,
                 COUNT(*) FILTER (WHERE risk_status <> 'Closed') AS open_risk_count,
                 COUNT(*) FILTER (WHERE risk_status <> 'Closed' AND severity = 'Critical')
                   AS open_critical_risk_count,
                 COUNT(*) FILTER (
                   WHERE risk_status <> 'Closed' AND severity = 'Critical' AND due_date < DATE'{as_of}'
                 ) AS overdue_critical_risk_count
          FROM {fq}.risks
          GROUP BY initiative_id
        ),
        milestone_summary AS (
          SELECT initiative_id,
                 COUNT(*) AS milestone_count,
                 COUNT(*) FILTER (WHERE milestone_status = 'Complete') AS completed_milestone_count,
                 COUNT(*) FILTER (WHERE milestone_status = 'Overdue') AS overdue_milestone_count,
                 MIN(planned_date) FILTER (WHERE milestone_status IN ('Due soon', 'Upcoming'))
                   AS next_milestone_date
          FROM {fq}.milestones
          GROUP BY initiative_id
        ),
        latest_document AS (
          SELECT initiative_id, document_title, document_text
          FROM {fq}.portfolio_documents
          WHERE initiative_id IS NOT NULL
          QUALIFY ROW_NUMBER() OVER (PARTITION BY initiative_id ORDER BY document_date DESC) = 1
        )
        SELECT
          i.*,
          l.month_date AS reporting_month,
          l.planned_progress_pct,
          l.actual_progress_pct,
          l.planned_value_to_date_usd,
          l.realized_value_to_date_usd,
          l.forecast_value_at_completion_usd,
          l.investment_to_date_usd,
          l.benefit_confidence_score,
          GREATEST(l.planned_value_to_date_usd - l.realized_value_to_date_usd, 0)
            AS value_gap_to_date_usd,
          GREATEST(i.target_value_usd - l.forecast_value_at_completion_usd, 0)
            AS value_at_risk_usd,
          COALESCE(r.open_risk_count, 0) AS open_risk_count,
          COALESCE(r.open_critical_risk_count, 0) AS open_critical_risk_count,
          COALESCE(r.overdue_critical_risk_count, 0) AS overdue_critical_risk_count,
          COALESCE(m.milestone_count, 0) AS milestone_count,
          COALESCE(m.completed_milestone_count, 0) AS completed_milestone_count,
          COALESCE(m.overdue_milestone_count, 0) AS overdue_milestone_count,
          m.next_milestone_date,
          d.document_title AS latest_document_title,
          d.document_text AS latest_document_summary,
          CASE
            WHEN l.actual_progress_pct < 0.35 THEN 'Design'
            WHEN l.actual_progress_pct < 0.65 THEN 'Pilot'
            WHEN l.actual_progress_pct < 0.90 THEN 'Scale'
            ELSE 'Benefits validation'
          END AS current_stage
        FROM {fq}.initiatives i
        JOIN latest l USING (initiative_id)
        LEFT JOIN risk_summary r USING (initiative_id)
        LEFT JOIN milestone_summary m USING (initiative_id)
        LEFT JOIN latest_document d USING (initiative_id)
        """,
        f"{fq}.v_initiative_current",
    )

    run(
        spark,
        f"""
        CREATE OR REPLACE VIEW {fq}.v_operating_kpi_current
        COMMENT 'Latest month for each operating KPI and business unit.'
        AS
        SELECT *,
               CASE direction
                 WHEN 'HIGHER_BETTER' THEN actual_value - target_value
                 ELSE target_value - actual_value
               END AS favorable_gap,
               CASE direction
                 WHEN 'HIGHER_BETTER' THEN actual_value / NULLIF(target_value, 0)
                 ELSE target_value / NULLIF(actual_value, 0)
               END AS attainment_ratio
        FROM {fq}.operating_kpi_monthly
        QUALIFY ROW_NUMBER() OVER (
          PARTITION BY business_unit, kpi_name ORDER BY month_date DESC
        ) = 1
        """,
        f"{fq}.v_operating_kpi_current",
    )

    value_dimensions = """  - name: Initiative ID
    expr: initiative_id
    display_name: Initiative ID
    synonyms: [program ID, workstream ID]
  - name: Initiative
    expr: initiative_name
    display_name: Initiative
    synonyms: [program, project, transformation initiative]
  - name: Strategic Theme
    expr: strategic_theme
    display_name: Strategic Theme
  - name: Workstream
    expr: workstream
    display_name: Workstream
  - name: Business Unit
    expr: business_unit
    display_name: Business Unit
    synonyms: [division, BU]
  - name: Region
    expr: region
    display_name: Region
  - name: Executive Sponsor
    expr: executive_sponsor
    display_name: Executive Sponsor
  - name: Initiative Owner
    expr: initiative_owner
    display_name: Initiative Owner
    synonyms: [owner, accountable lead]
  - name: Value Type
    expr: value_type
    display_name: Value Type
  - name: Health
    expr: health
    display_name: Health
    synonyms: [RAG, traffic light, status]
  - name: Current Stage
    expr: current_stage
    display_name: Current Stage
  - name: Reporting Month
    expr: reporting_month
    display_name: Reporting Month
"""
    value_measures = """  - name: Initiative Count
    expr: COUNT(DISTINCT initiative_id)
    display_name: Initiative Count
    format: {type: number}
  - name: Target Value
    expr: SUM(target_value_usd)
    display_name: Target Value
    synonyms: [approved value, full potential, target benefits]
    format: {type: currency, currency_code: USD}
  - name: Planned Value to Date
    expr: SUM(planned_value_to_date_usd)
    display_name: Planned Value to Date
    synonyms: [plan to date]
    format: {type: currency, currency_code: USD}
  - name: Realized Value to Date
    expr: SUM(realized_value_to_date_usd)
    display_name: Realized Value to Date
    synonyms: [banked value, validated value, actual benefits]
    format: {type: currency, currency_code: USD}
  - name: Forecast Value at Completion
    expr: SUM(forecast_value_at_completion_usd)
    display_name: Forecast Value at Completion
    synonyms: [forecast value, expected benefits]
    format: {type: currency, currency_code: USD}
  - name: Value Gap to Date
    expr: SUM(value_gap_to_date_usd)
    display_name: Value Gap to Date
    synonyms: [plan gap, value shortfall]
    format: {type: currency, currency_code: USD}
  - name: Value at Risk
    expr: SUM(value_at_risk_usd)
    display_name: Value at Risk
    synonyms: [forecast shortfall, target value at risk]
    format: {type: currency, currency_code: USD}
  - name: Approved Investment
    expr: SUM(approved_investment_usd)
    display_name: Approved Investment
    format: {type: currency, currency_code: USD}
  - name: Investment to Date
    expr: SUM(investment_to_date_usd)
    display_name: Investment to Date
    format: {type: currency, currency_code: USD}
  - name: Net Forecast Benefit
    expr: MEASURE(`Forecast Value at Completion`) - MEASURE(`Approved Investment`)
    display_name: Net Forecast Benefit
    format: {type: currency, currency_code: USD}
  - name: Forecast ROI
    expr: MEASURE(`Net Forecast Benefit`) / NULLIF(MEASURE(`Approved Investment`), 0)
    display_name: Forecast ROI
    synonyms: [return on investment]
    format: {type: percentage}
  - name: Forecast Attainment
    expr: MEASURE(`Forecast Value at Completion`) / NULLIF(MEASURE(`Target Value`), 0)
    display_name: Forecast Attainment
    synonyms: [forecast versus target, forecast achievement]
    format: {type: percentage}
"""
    run(
        spark,
        metric_view_sql(
            f"{fq}.mv_value_realization",
            f"{fq}.v_initiative_current",
            "Governed value realization measures for the Northstar transformation portfolio. "
            "Finance validates Realized Value to Date. Value at Risk is the positive gap "
            "between approved target and forecast value at completion.",
            value_dimensions,
            value_measures,
        ),
        f"{fq}.mv_value_realization",
    )

    delivery_measures = """  - name: Initiative Count
    expr: COUNT(DISTINCT initiative_id)
    display_name: Initiative Count
    format: {type: number}
  - name: Red Initiatives
    expr: COUNT(DISTINCT initiative_id) FILTER (WHERE health = 'Red')
    display_name: Red Initiatives
    format: {type: number}
  - name: Amber Initiatives
    expr: COUNT(DISTINCT initiative_id) FILTER (WHERE health = 'Amber')
    display_name: Amber Initiatives
    format: {type: number}
  - name: Average Progress
    expr: AVG(actual_progress_pct)
    display_name: Average Progress
    format: {type: percentage}
  - name: Maximum Days Slipped
    expr: MAX(days_slipped)
    display_name: Maximum Days Slipped
    format: {type: number}
  - name: Open Risks
    expr: SUM(open_risk_count)
    display_name: Open Risks
    format: {type: number}
  - name: Open Critical Risks
    expr: SUM(open_critical_risk_count)
    display_name: Open Critical Risks
    format: {type: number}
  - name: Overdue Critical Risks
    expr: SUM(overdue_critical_risk_count)
    display_name: Overdue Critical Risks
    format: {type: number}
  - name: Overdue Milestones
    expr: SUM(overdue_milestone_count)
    display_name: Overdue Milestones
    format: {type: number}
  - name: Milestone Completion
    expr: SUM(completed_milestone_count) / NULLIF(SUM(milestone_count), 0)
    display_name: Milestone Completion
    format: {type: percentage}
"""
    run(
        spark,
        metric_view_sql(
            f"{fq}.mv_delivery_health",
            f"{fq}.v_initiative_current",
            "Current initiative delivery health, milestones, risks, ownership, and schedule. "
            "Use the latest document summary for the reported reason behind an initiative status.",
            value_dimensions,
            delivery_measures,
        ),
        f"{fq}.mv_delivery_health",
    )

    operating_dimensions = """  - name: Month
    expr: month_date
    display_name: Month
  - name: Business Unit
    expr: business_unit
    display_name: Business Unit
    synonyms: [division, BU]
  - name: KPI
    expr: kpi_name
    display_name: KPI
    synonyms: [metric, operating measure]
  - name: Unit
    expr: unit
    display_name: Unit
  - name: Direction
    expr: direction
    display_name: Direction
"""
    operating_measures = """  - name: Actual
    expr: AVG(actual_value)
    display_name: Actual
  - name: Target
    expr: AVG(target_value)
    display_name: Target
  - name: Favorable Gap
    expr: AVG(CASE direction WHEN 'HIGHER_BETTER' THEN actual_value - target_value ELSE target_value - actual_value END)
    display_name: Favorable Gap
  - name: Attainment
    expr: AVG(CASE direction WHEN 'HIGHER_BETTER' THEN actual_value / NULLIF(target_value, 0) ELSE target_value / NULLIF(actual_value, 0) END)
    display_name: Attainment
    format: {type: percentage}
"""
    run(
        spark,
        metric_view_sql(
            f"{fq}.mv_operating_performance",
            f"{fq}.operating_kpi_monthly",
            "Monthly operating KPIs by business unit. Never combine different KPIs into "
            "one aggregate because their units differ. Compare Actual and Target only "
            "within one KPI.",
            operating_dimensions,
            operating_measures,
        ),
        f"{fq}.mv_operating_performance",
    )

    column_comments = {
        "initiatives": {
            "initiative_id": "Stable identifier for one transformation initiative.",
            "target_value_usd": "Finance-approved full program value target in USD.",
            "realization_factor": "Synthetic factor used to create the benefit curve.",
            "forecast_factor": "Forecast value at completion divided by target value.",
            "health": "Current delivery health. Allowed values are Green, Amber, and Red.",
        },
        "portfolio_monthly": {
            "planned_value_to_date_usd": "Cumulative value expected by the reporting month.",
            "realized_value_to_date_usd": "Cumulative value validated by finance.",
            "benefit_confidence_score": "Synthetic score from zero to one for forecast confidence.",
        },
        "risks": {
            "severity": "Allowed values are Critical, High, Medium, and Low.",
            "risk_status": "Allowed values are Open, Mitigating, and Closed.",
        },
    }
    for table, comments in column_comments.items():
        for column, comment in comments.items():
            try_sql(
                spark,
                f"ALTER TABLE {fq}.{table} ALTER COLUMN {column} COMMENT '{comment}'",
                f"{table}.{column} comment",
            )

    run(
        spark,
        f"ALTER TABLE {fq}.initiatives ALTER COLUMN initiative_id SET NOT NULL",
        "initiatives initiative_id not null constraint",
    )
    run(
        spark,
        f"ALTER TABLE {fq}.initiatives ADD CONSTRAINT initiatives_pk "
        "PRIMARY KEY (initiative_id) NOT ENFORCED",
        "initiatives primary key",
    )
    for table in ("portfolio_monthly", "risks", "milestones"):
        run(
            spark,
            f"ALTER TABLE {fq}.{table} ADD CONSTRAINT {table}_initiative_fk "
            f"FOREIGN KEY (initiative_id) REFERENCES {fq}.initiatives",
            f"{table} foreign key",
        )

    certified_assets = [
        ("TABLE", "initiatives"),
        ("TABLE", "portfolio_monthly"),
        ("TABLE", "risks"),
        ("TABLE", "milestones"),
        ("TABLE", "portfolio_documents"),
        ("TABLE", "operating_kpi_monthly"),
        ("TABLE", "mv_value_realization"),
        ("TABLE", "mv_delivery_health"),
        ("TABLE", "mv_operating_performance"),
    ]
    for object_type, name in certified_assets:
        try_sql(
            spark,
            f"SET TAG ON {object_type} {fq}.{name} "
            "`system.certification_status` = `certified`",
            f"certification tag on {name}",
        )

    domain_membership = {
        "Enterprise Transformation": [
            ("TABLE", "initiatives"),
            ("TABLE", "portfolio_monthly"),
            ("TABLE", "risks"),
            ("TABLE", "milestones"),
            ("TABLE", "portfolio_documents"),
            ("TABLE", "operating_kpi_monthly"),
            ("VIEW", "v_initiative_current"),
            ("VIEW", "v_operating_kpi_current"),
            ("VIEW", "mv_value_realization"),
            ("VIEW", "mv_delivery_health"),
            ("VIEW", "mv_operating_performance"),
        ],
        "Enterprise Transformation/Value Realization": [
            ("TABLE", "initiatives"),
            ("TABLE", "portfolio_monthly"),
            ("VIEW", "v_initiative_current"),
            ("VIEW", "mv_value_realization"),
        ],
        "Enterprise Transformation/Delivery and Risk": [
            ("TABLE", "initiatives"),
            ("TABLE", "risks"),
            ("TABLE", "milestones"),
            ("TABLE", "portfolio_documents"),
            ("VIEW", "v_initiative_current"),
            ("VIEW", "mv_delivery_health"),
        ],
        "Enterprise Transformation/Operating Performance": [
            ("TABLE", "operating_kpi_monthly"),
            ("VIEW", "v_operating_kpi_current"),
            ("VIEW", "mv_operating_performance"),
        ],
    }
    for tag_key, objects in domain_membership.items():
        for object_type, object_name in objects:
            ensure_table_tag(
                spark,
                catalog,
                schema,
                object_type,
                object_name,
                tag_key,
            )

    for table in (
        "initiatives",
        "portfolio_monthly",
        "risks",
        "milestones",
        "portfolio_documents",
        "operating_kpi_monthly",
    ):
        try_sql(spark, f"ANALYZE TABLE {fq}.{table} COMPUTE STATISTICS", f"statistics on {table}")

    print("Synthetic data and Unity Catalog semantics are ready.")


if __name__ == "__main__":
    main()
