# Ontology map

Genie Ontology combines business context that people govern with context that Databricks infers from approved assets and their use. This demo includes both parts.

## Modeled context

| Layer | Demo assets | Governance point |
|---|---|---|
| Business organization | Enterprise Transformation domain with Value Realization, Delivery and Risk, and Operating Performance subdomains | Governed tags organize the assets. A curator controls the domain and its Pages. |
| Business terms | Eight committed Page source files | Each Page has a definition, owner, synonyms, related assets, and sources. |
| Measures | `mv_value_realization`, `mv_delivery_health`, and `mv_operating_performance` | Measure logic lives in Unity Catalog and is reused by SQL, dashboards, and agents. |
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
| Value Realization | Realized Value to Date, Forecast Value at Completion, Value at Risk | `mv_value_realization` and the Value Realization Agent |
| Delivery and Risk | Delivery Health, Executive Intervention | `mv_delivery_health`, risks, milestones, documents, and the Delivery Risk Agent |
| Operating Performance | KPI Attainment, Favorable Gap | `mv_operating_performance` and the Operating Performance Agent |

The bundle creates the governed tag `Enterprise Transformation` for the domain. It also creates one tag for each subdomain by using the required `Enterprise Transformation/<subdomain>` naming pattern. The data build applies the root tag and the matching subdomain tags to every table, view, and metric view in the demo.

The bundle setup job uses the public Beta workspace tag API to apply the root domain tag to the dashboard. It applies the root and matching subdomain tags to each Genie Agent. The Page files still need review and publication in the interface.

## Data relationships

`initiatives` is the parent entity. Monthly value records, risks, milestones, and portfolio documents link to an initiative through `initiative_id`. Operating KPIs link at the business unit level. The current initiative view combines the latest value record with risk, milestone, and evidence summaries.

## Authority order used in the demo

1. Published Pages define business terms.
2. Certified metric views define measures.
3. Verified SQL shows approved query patterns.
4. Focused Genie Agents define the right source for a decision area.
5. Dashboard and query use add current inferred context.

This order is a demo operating rule. Actual retrieval remains permission aware and uses Databricks ranking.

## Quality loop

The setup job validates row counts, dates, measure values, and data invariants. Each agent stores benchmark questions with SQL answers. The regression job runs those questions as new conversations and fails if a question is wrong or still needs manual review.

Feedback alone does not change agent behavior. An editor must review failures, correct metadata or SQL, and run the benchmark job again.
