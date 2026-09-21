# Demo design

## Audience

The main audience is enterprise Data and AI leaders, transformation leaders, and executive sponsors. Business unit leaders and data teams can also use the demo.

## Business setting

Northstar Group is a fictional enterprise with twelve transformation initiatives across growth, cost, cash, operations, technology, and operating model work. The portfolio tracks approved value, realized value, forecast value, investment, delivery health, risks, milestones, and operating KPIs.

The demo answers one leadership question: where should the executive committee intervene now to protect value and improve business outcomes?

## Story

The story moves through three decisions.

1. Confirm whether the portfolio is delivering the approved value case.
2. Identify the initiatives that need executive intervention and show the evidence.
3. Check whether operating KPIs are moving in the expected direction.

The demo then opens the cited business definition, shows its domain and owner, and runs the benchmark suite. This proves that the answer has governed business meaning and a quality process behind it.

## Components

| Component | Purpose |
|---|---|
| Synthetic Delta tables | Provide deterministic portfolio, risk, milestone, document, and KPI data. |
| Metric views | Define value, delivery, and operating measures. |
| Unity Catalog metadata | Records descriptions, column meaning, keys, and certification signals. |
| Domain and subdomains | Organize assets by business purpose. |
| Pages | Define transformation terms and their authoritative sources. |
| Value Realization Agent | Answers value case and return questions. |
| Delivery Risk Agent | Answers intervention, risk, milestone, and evidence questions. |
| Operating Performance Agent | Answers KPI and target questions. |
| AI/BI dashboard | Gives executives a stable starting point. |
| Benchmarks | Compare agent answers with committed SQL results. |

## Brand and presentation

Use a direct executive style. Start with the decision and numbers. Show definitions only when they help the audience trust or challenge the answer. Keep the Northstar name visible so no one mistakes synthetic data for a customer result.

Use the Databricks product interface as the main visual. Do not add third party marks or imply customer endorsement in the public repository.

## Architecture

The bundle creates the data and governed metric layer in Unity Catalog. The dashboard and Genie Agents query that layer. Pages add approved business definitions. Genie Ontology combines this modeled context with context inferred from the dashboard, queries, and agents. Genie One retrieves the sources that the user is allowed to see and shows citations in the answer.

## Success criteria

- The bundle can be deployed from a clean clone with one `make deploy` command.
- The setup job passes every data and semantic check.
- All three agents include sample questions, verified SQL, and benchmark questions.
- The dashboard opens without dataset errors.
- A customer can inspect a cited Page and see its domain, owner, synonyms, definition, and related assets.
- The benchmark job reports a result for every committed benchmark question.
- The presenter states that the data is synthetic and that preview features can change.
