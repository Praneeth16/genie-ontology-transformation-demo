# Ontology map

Genie Ontology combines business context that people govern with context that Databricks infers from approved assets and their use. This demo includes both parts.

## Modeled context

| Layer | Demo assets | Governance point |
|---|---|---|
| Business organization | Enterprise Transformation domain with Value Realization, Delivery and Risk, and Operating Performance subdomains | Governed tags organize the assets. A curator controls the domain and its Pages. |
| Business terms | Eight committed Page source files | Each Page has a definition, owner, synonyms, related assets, and sources. |
| Measures | `mv_value_realization`, `mv_delivery_health`, `mv_value_trend`, and `mv_operating_performance` | Measure logic lives in Unity Catalog and is reused by SQL, dashboards, and agents. |
| Measure meaning | A `comment`, `display_name`, `format`, and `synonyms` on every field and measure | The definition travels with the measure instead of sitting in a document beside it. |
| Relationships | `joins` in `mv_value_realization` and `mv_delivery_health` | The entity graph is governed. An agent does not invent a join or get the grain wrong. |
| Time rules | Semiadditive and trailing `window` measures in `mv_value_trend` and `mv_operating_performance` | Cumulative records are never added across months, in every tool that reads the measure. |
| Data meaning | Table comments, column comments, primary keys, and foreign keys | The catalog records grain, relationships, and business meaning. |
| Trust signal | Certification tags on curated tables and metric views | Certification tells users and Genie which assets the owner vouches for. |
| Access | Unity Catalog and workspace permissions | A user can only retrieve sources that the user can access. |

## Inferred context

| Source | What Genie can infer in this demo |
|---|---|
| AI/BI dashboard | Which measures leaders use together and which views support executive review. |
| Verified SQL | Which source and measure answer a known business question. |
| Genie Agents | Which agent is authoritative for value, delivery, or operating performance. |
| SQL queries | Common filters, groupings, and relationships used in analysis. |
| Asset use | Which approved context is used often and remains current. |

Databricks ranks inferred context by authority, use, and freshness. It also checks permissions before retrieval. Modeled definitions should win when a critical business term conflicts with context that Genie inferred elsewhere.

## Domain design

| Domain or subdomain | Included Pages | Main assets |
|---|---|---|
| Enterprise Transformation | Transformation Value Office | Executive dashboard and all three agents |
| Value Realization | Realized Value to Date, Forecast Value at Completion, Value at Risk | `mv_value_realization`, `mv_value_trend`, `v_initiative_progress`, and the Value Realization Agent |
| Delivery and Risk | Delivery Health, Executive Intervention | `mv_delivery_health`, risks, milestones, documents, the three initiative summary views, and the Delivery Risk Agent |
| Operating Performance | KPI Attainment, Favorable Gap | `mv_operating_performance` and the Operating Performance Agent |

The bundle creates the governed tag `Enterprise Transformation` for the domain. It also creates one tag for each subdomain by using the required `Enterprise Transformation/<subdomain>` naming pattern. The data build applies the root tag and the matching subdomain tags to every table, view, and metric view in the demo.

The bundle setup job uses the public Beta workspace tag API to apply the root domain tag to the dashboard. It applies the root and matching subdomain tags to each Genie Agent. The Page files still need review and publication in the interface.

## Data relationships

`initiatives` is the parent entity. Monthly value records, risks, milestones, and portfolio
documents link to an initiative through `initiative_id`. Operating KPIs link at the business
unit level.

The relationships are modeled in the metric views rather than written out per query.
`mv_value_realization` and `mv_delivery_health` source `initiatives` and declare `joins` to
four summary views, each of which returns exactly one row per initiative:

| Join name | Source | Contributes |
|---|---|---|
| `progress` | `v_initiative_progress` | Reporting month plan, realized value, forecast, investment, value at risk, and stage. |
| `risk` | `v_initiative_risk_summary` | Open, critical, and overdue critical risk counts. |
| `milestone` | `v_initiative_milestone_summary` | Milestone counts, overdue milestones, and the next milestone date. |
| `evidence` | `v_initiative_latest_document` | The title of the most recent management document. |

`mv_value_trend` works at a different grain. It sources `portfolio_monthly` and joins
`initiatives` as a dimension, so the same initiative attributes describe a time series.

The one row per initiative contract is what allows the default `many_to_one` cardinality. A
summary view that dropped or duplicated an initiative would silently change every governed
measure, so `validate_demo.py` asserts the row count of each one.

`v_initiative_current` remains for row level questions and for the dashboard detail table.
It is now a thin join of the same summary views rather than a separate calculation, so it
cannot disagree with the metric views.

## Semiadditive measures

`portfolio_monthly` stores cumulative to date values. Adding twenty months of a running
total produces a number several times larger than the approved target, and it looks
plausible. `mv_value_trend` solves this in the model rather than in each query:

```yaml
  - name: Realized Value at Period End
    expr: SUM(realized_value_to_date_usd)
    window:
      - order: Month
        range: current
        semiadditive: last
```

A quarter returns its closing month. A year returns its closing month. Every agent,
dashboard, and BI tool that reads the measure inherits the rule, and a committed benchmark
fails if the behavior ever changes.

Three details here were confirmed against a warehouse rather than inferred, and each one
fails in a way that still returns a plausible looking number:

| Detail | Why it matters |
|---|---|
| `order` names the field `Month`, not the source column `month_date` | The engine rejects a source column outright: `window.order field must reference existing dimension columns`. |
| `range: current`, not `range: all` | `all` returns the same grand total for every period. On this data that reported 4.95 billion dollars against a 645 million dollar target. |
| A join alias must not match a field name | Name resolution is case insensitive, so an alias `initiative` beside a field `Initiative` makes the engine try to read a struct member from a string. The trend view uses `initiative_dim`. |

`range: trailing N month` excludes the current period. `Actual Three Month Average` in
`mv_operating_performance` adds `offset: 1 month` so that it covers the reporting month and
the two before it, which is what a reader assumes a three month average means.

`make check` enforces the first and third of these, so neither can reach a workspace again.

## Authority order used in the demo

1. Published Pages define business terms.
2. Certified metric views define measures.
3. Verified SQL shows approved query patterns.
4. Focused Genie Agents define the right source for a decision area.
5. Dashboard and query use add current inferred context.

This order is a demo operating rule. Actual retrieval remains permission aware and uses Databricks ranking.

## Quality loop

`make check` renders every metric view definition locally and validates it before a
deployment can reach a workspace. It fails when the YAML does not parse, when a field or
measure has no business definition, when a metric view refers to a join it does not declare,
or when a window measure is missing its order, range, or semiadditive rule.

The setup job then validates row counts, join grain, dates, measure values, data invariants,
certification, and domain tag membership. Each agent stores benchmark questions with SQL
answers. The regression job runs those questions as new conversations and fails if a question
is wrong or still needs manual review.

Feedback alone does not change agent behavior. An editor must review failures, correct metadata or SQL, and run the benchmark job again.
