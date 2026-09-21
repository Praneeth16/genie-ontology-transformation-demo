# Genie Ontology question bank

Use these questions during the demo and during customer discovery. Start with the six question sequence. Use the larger bank when the audience wants to test a specific decision.

The Surface column shows where to ask each question. Use Genie One when the question crosses value, delivery, operating results, and management evidence. Use a focused Genie Agent when the question stays within one decision area.

All expected results refer to synthetic Northstar data as at 31 August 2026.

## Six question executive sequence

| Step | Question | Surface | What the audience should see |
|---:|---|---|---|
| 1 | How is the transformation portfolio performing against the approved value case? | Value Realization Agent | Approved target, plan to date, realized value, forecast value, value at risk, forecast attainment, and return. |
| 2 | Which initiatives have the largest forecast shortfall, and who owns them? | Value Realization Agent | A ranked list with owner, business unit, health, target, forecast, and value at risk. |
| 3 | Where does the executive committee need to intervene this month? | Delivery Risk Agent | Four red initiatives ranked by overdue critical risks, delay, and value at risk. |
| 4 | Who owns the next action for Network footprint redesign, what is due, and what decision must the executive committee make? | Delivery Risk Agent | The owner, overdue action, recorded mitigation, steering evidence, and decision request. |
| 5 | What does Value at Risk mean, how is it calculated, and where is it used? | Catalog Explorer and Genie One | The definition, synonyms, expression, owner, tags, certification, source, and related assets. |
| 6 | Which benchmark questions passed in the latest run? | Benchmark run | 14 of 14 questions passed across the three agents with no review items. |

## Portfolio and value realization

| Question | Surface | Expected result |
|---|---|---|
| How is the portfolio performing against target value, plan to date, realized value, and forecast value? | Value Realization Agent | Show all four values, value at risk, the gap to plan, and forecast attainment. Keep realized value separate from forecast value. |
| Which strategic themes drive the gap to plan and the value at risk? | Value Realization Agent | Rank themes by value gap to date and value at risk. |
| Which business units and regions have the largest forecast shortfall? | Value Realization Agent | Rank the governed value at risk measure by business unit and region. |
| What changed in planned value, realized value, and investment since the previous monthly review? | Value Realization Agent | Compare July 2026 with August 2026 using the period end measures in `mv_value_trend`. The two months must not be added together. |
| How much investment and realized value did the portfolio report at each quarter end? | Value Realization Agent | One closing row per quarter from the semiadditive period end measures. Values must never exceed the 645 million dollar approved target. |
| Is realized value still trending up month by month? | Value Realization Agent | Group the period end measures in `mv_value_trend` by month and read the closing value of each month. |
| Which initiatives have the largest protectable value? | Value Realization Agent | Rank initiatives with positive value at risk. Include the owner, health, target, forecast, and value at risk. |
| Which value types contribute most to the current forecast shortfall? | Value Realization Agent | Group value at risk by revenue, cost, working capital, and margin. |
| Is the forecast return still above the approved investment case? | Value Realization Agent | Show approved investment, forecast value, net forecast benefit, and forecast return. State that this is a forecast. |

## Initiative diagnosis and executive action

| Question | Surface | Expected result |
|---|---|---|
| Which initiatives explain the miss for each underperforming strategic theme? | Value Realization Agent | Break each theme gap into initiatives and include the accountable owner. |
| Is the value signal consistent with delivery health, risks, milestones, and steering evidence? | Genie One | Compare the governed value result with current delivery records. Cite the supporting sources and call out any disagreement. |
| Why is Network footprint redesign red, and what decision is needed next? | Delivery Risk Agent | Use the current status, schedule delay, overdue items, and Network steering memo. |
| Which red initiatives have no overdue critical risk or overdue milestone? | Delivery Risk Agent | Identify status records that need closer evidence review because the common delivery signals do not explain the red status. |
| Which risks or milestones could put the most forecast value at risk? | Genie One | Join delivery issues to initiative value at risk. Present the result as a priority list, not a causal claim. |
| What is the recommended executive action for each red initiative? | Genie One | Use recorded mitigations and decision requests. Label any additional recommendation as analysis. |
| Were the largest value gaps already recorded as delivery risks or in steering evidence? | Genie One | Match the largest gaps with open risks and the latest relevant document. Do not treat the document as proof that value was lost. |

## Owner and delivery execution

| Question | Surface | Expected result |
|---|---|---|
| How does delivery execution compare across business units? | Delivery Risk Agent | Show red and amber initiatives, progress, overdue critical risks, overdue milestones, and milestone completion. |
| Which regions have the most value at risk and the most delayed initiatives? | Genie One | Compare value at risk with schedule delay by region. |
| Which executive sponsors own the largest forecast shortfall? | Value Realization Agent | Rank sponsors by value at risk and include the initiatives behind each result. |
| Which initiative owners have overdue critical risks, and what mitigation did they record? | Delivery Risk Agent | List the risk owner, initiative owner, due date, mitigation, and evidence source. |
| How are owners executing against the milestone plan? | Delivery Risk Agent | Compare completed, overdue, due soon, and upcoming milestones by owner. |
| Which initiatives should leaders target first to protect the most value? | Genie One | Rank positive value at risk, then add health, overdue risks, overdue milestones, owner, and the latest evidence. |
| What should each owner do before the next executive review? | Genie One | Use due dates, recorded mitigation, milestone status, and decision requests. Keep facts separate from generated recommendations. |

## Operating outcomes

| Question | Surface | Expected result |
|---|---|---|
| Which operating KPIs are below target in August 2026? | Operating Performance Agent | Show business unit, KPI, actual, target, favorable gap, and attainment. |
| Which business unit has the widest KPI target gaps? | Operating Performance Agent | Compare favorable gap and attainment within each KPI. Do not add values with different units. |
| Which business units have improved forecast accuracy since January 2025? | Operating Performance Agent | Show the monthly trend and the August 2026 target result for each business unit. |
| Is the on time delivery improvement a real trend or one good month? | Operating Performance Agent | Compare the monthly Actual with Actual Three Month Average, which covers the reporting month and the two before it. |
| Which business unit has the lowest on time delivery attainment? | Operating Performance Agent | Return one business unit from the latest result with actual, target, and attainment. |
| Which KPIs show a seasonal pattern, and does the pattern repeat across business units? | Operating Performance Agent | Use the monthly series for one KPI at a time and compare the same months across business units. |
| Are operating results consistent with the initiatives in each business unit? | Genie One | Compare current initiative health with KPI attainment for the same business unit. Keep the answer descriptive. |
| Which business units lag most on both delivery and operating performance? | Genie One | Compare red work, overdue items, and current KPI attainment by business unit. |

## Ontology and governance

| Question | Surface | Expected result |
|---|---|---|
| What does Value at Risk mean in this portfolio? | Catalog Explorer or Genie One | State that it is the positive gap between the approved target and forecast value at completion. |
| What synonyms can a user use for Value at Risk? | Catalog Explorer | Show forecast shortfall and target value at risk. |
| What does the measure description say about Value at Risk? | Catalog Explorer | Read the measure comment. It states that this is a forecast shortfall, not a loss already taken. |
| What is the initiative joined to in the value metric view? | Catalog Explorer | Open the `joins` block. The reporting month record, risk summary, milestone summary, and latest document each join on `initiative_id`. |
| Why can the agent not add twelve months of realized value together? | Catalog Explorer or Genie One | The period end measures use a semiadditive window, so a period returns its closing month. The rule lives with the measure. |
| Which asset defines the Value at Risk calculation? | Catalog Explorer | Show the certified `mv_value_realization` metric view and the measure expression. |
| Who owns the value measure, and which business area governs it? | Catalog Explorer | Show the owner and the Enterprise Transformation and Value Realization tags. |
| Which dashboards and agents use the value measure? | Catalog Explorer | Show the related dashboard, setup job, and Value Realization Agent. |
| What sources and definitions supported this answer? | Genie Agent | Expand Sources, inspect the generated SQL, and open the cited measure. |
| What happens if a user cannot access one of the sources? | Presenter discussion | Explain that retrieval respects the user permission. The answer can only use sources the user can access. |
| How do modeled definitions and inferred context work together? | Presenter discussion | Explain that owners define critical terms and measures. Databricks can infer additional context from approved assets and their use. Governed definitions remain authoritative. |

## Quality and repeatability

| Question | Surface | Expected result |
|---|---|---|
| How do we know the agent returns the expected result? | Benchmark run | Show the committed question, approved SQL answer, and latest result. |
| Which test would catch a broken time rule? | Benchmark run | The quarter end benchmark. If the semiadditive window ever starts summing months, the values climb past the approved target and the run fails. |
| Can a bad metric view reach a workspace? | Repository | `make check` renders and validates every metric view definition locally before a deployment. |
| What happens when a benchmark fails? | Presenter discussion | An editor reviews the failure, fixes the definition, metadata, or approved SQL, and runs the benchmark again. |
| Can another team deploy the same demo? | Repository | Explain that the Databricks Asset Bundle creates the data, metric views, dashboard, agents, and regression job. |
| Which parts require customer review? | Presenter discussion | Business owners approve definitions, sources, permissions, agent scope, and acceptance questions. |
| What is the first useful workshop output? | Presenter discussion | A short list of leadership questions, approved measures, source owners, and test questions for one decision area. |

## Questions for customer discovery

Use these questions after the demo:

1. Which recurring leadership decision takes the most time to reconcile today?
2. Which measures cause the most disagreement across teams?
3. Who owns the business meaning of those measures?
4. Which structured sources and management documents support the decision?
5. Which user groups should see each source?
6. What answer would the business accept as correct?
7. Which wrong answer would create the most risk?
8. Which questions should become regression tests before launch?
