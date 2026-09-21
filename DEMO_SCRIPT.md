# Customer demo script

This script is for a 20 minute customer conversation. Use the sections marked Core for a 10 minute version.

## Before the meeting

- Run `make benchmark` and review every result.
- Open the dashboard, Genie One, the three Genie Agents, and the Value at Risk Page in separate tabs.
- Confirm that the Pages are published and the presenter can open their citations.
- Reset each agent to a new conversation.
- Keep the fixed reporting date of 31 August 2026 visible.

## Storyline at a glance

Before the first click, tell the audience how the story will move:

1. Detect the portfolio signal that needs attention.
2. Explain the value and delivery drivers behind it.
3. Show who owns the recorded action and which decision is due.
4. Prove that the answer uses approved definitions and has passed its tests.

Say:

> We will follow one management question from signal to action. We will see where value is at risk and why the work is off track. We will then see who owns the next action and whether the answer uses approved definitions.

## 1. Set the business problem. Core. Two minutes.

Open the Enterprise Transformation Value Office dashboard.

Say:

> Northstar Group is a fictional enterprise with twelve transformation initiatives. Its leadership team has approved 645 million dollars of value. The team needs one clear view of value, delivery risk, and operating outcomes. All data in this demo is synthetic.

> Northstar's transformation office should not spend the executive review reconciling different numbers and status reports. Business unit leaders need answers that use the same definitions and source records.

> The goal is a review where leaders can move from a portfolio signal to its driver and source evidence. They can then see the owner and next decision. People have defined the value and delivery measures in Unity Catalog. They have also defined KPI attainment. The dashboard, Genie Agents, and Genie One can use that shared context.

Point to the value cards, the value at risk chart, and the executive intervention list.

Do not read every number. Establish the decision the audience will follow and show that the dashboard and agents use the same governed data.

## 2. Ask the cross domain question in Genie One. Core. Three minutes.

Open Genie One and ask:

> How is the Northstar transformation portfolio performing against the approved value case, and where should leadership intervene this month?

Let the answer finish. Look for target value, realized value, forecast value, value at risk, red initiatives, and named owners.

Follow Network footprint redesign for the rest of the demo. This initiative has a value signal and delivery issues. It also has an accountable owner and steering evidence.

Say:

> This question crosses value, delivery, and operating context. Genie One searched the Genie Ontology, selected sources that I can access, and returned one answer. The citation icons show which sources supported each part.

> We have detected the signal. The next steps will explain it and connect it to recorded evidence. We will then identify the action and test the answer.

Open the citation for Value at Risk or Realized Value to Date.

Show the Page title, domain, owner, synonyms, definition, related assets, and sources.

Say:

> A business owner has defined this term. On the Page, the owner defines Value at Risk as a forecast shortfall. The term does not mean that the value has already been lost. That difference changes the management decision.

If the Page citation does not appear, ask:

> Using the Value at Risk definition, which business units have the largest forecast shortfall?

## 3. Inspect the governed measure. Core. Two minutes.

Open the `mv_value_realization` metric view in Catalog Explorer.

Show the definitions for Target Value, Realized Value to Date, Forecast Value at Completion, Value at Risk, and Forecast Attainment.

Say:

> The Page defines the business term. The metric view defines the calculation. A dashboard author or agent can group these measures by business unit, region, theme, or owner without copying the formula.

Show the certification signal and the table and column descriptions.

Say:

> A data owner marks an asset as certified to show that the owner approves it. Permissions still decide which sources each user can retrieve.

## 4. Test value realization. Core. Three minutes.

Open the Northstar Value Realization Agent and ask:

> Which initiatives have the largest forecast shortfall, and who owns them?

Check that the answer gives a ranked list with initiative, business unit, owner, health, target, forecast, and value at risk.

Keep Network footprint redesign visible when it appears. The next section will connect its value signal to delivery evidence and an executive decision.

Open the generated SQL.

Say:

> This agent has a narrow job. It uses the value metric view, the monthly value records, and a current initiative view. We stored verified SQL for common questions in the repository. This gives the agent an approved query pattern that we can test.

Ask a follow up:

> What is the forecast portfolio return on approved investment?

Call out that forecast return is not realized return.

If the customer wants a deeper diagnosis, ask:

> Which strategic themes drive the gap to plan and the value at risk?

Then ask:

> What changed in planned value, realized value, and investment since the previous monthly review?

The agent uses the current metric view for the first question and the cumulative monthly records for the second question. Do not add the July and August values together.

## 5. Move from status to accountable action. Core. Three minutes.

Open the Northstar Delivery Risk Agent and ask:

> Where does the executive committee need to intervene this month?

The expected answer starts with the four red initiatives. It should name the owner, delay, overdue critical risks, value at risk, and the latest steering evidence.

Ask:

> What evidence explains the network footprint status?

Open the result for the Network steering memo.

Say:

> The structured data tells us that the initiative is red and 68 days late. The steering evidence says that site consultation is late and that leaders need to decide the closure cost estimate. We can review the measure and its management context together.

Ask:

> Who owns the next action for Network footprint redesign, what is due, and what decision must the executive committee make?

Check that the answer separates the recorded mitigation and decision request from any additional analysis.

Say:

> We started with a portfolio value signal. Leadership now has the accountable owner, the recorded next action, and the decision that is due.

Do not claim that the document proves that value was lost. It records the reason for intervention.

## 6. Connect the portfolio to operating outcomes. Two minutes.

Open the Northstar Operating Performance Agent and ask:

> Which operating KPIs are below target in August 2026?

Then ask:

> How has forecast accuracy changed since January 2025?

Say:

> The metric definition records whether a higher or lower value is better for each KPI. The agent compares one KPI at a time because the units differ. It can show that an operating trend happened during the transformation period. It does not claim that an initiative caused the change.

## 7. Show how quality is managed. Core. Three minutes.

Say:

> We have explained the issue and named the action. The remaining question is whether leaders can trust the answer and get the same governed result in the next review.

Open the Benchmarks tab in one agent.

Show a benchmark question, its SQL answer, and the latest evaluation result.

Say:

> Each benchmark runs as a new conversation. For chat mode, Databricks compares the generated result with the result from the approved SQL answer. We store the questions and SQL answers with the agent definition, so another team can deploy the same checks.

> User feedback does not change the agent by itself. An editor reviews a failure, corrects the definition, metadata, or verified SQL, and runs the benchmark again.

If time permits, show the setup job. Point out the data checks that run before the agents are updated.

## 8. Close with the customer path. Core. Two minutes.

Return to the dashboard.

Say:

> We followed one management question from the portfolio signal to its drivers and source evidence. We identified the owner and next decision. We then checked the definition and calculation behind the answer. The benchmark confirmed the expected result.

> We started with one decision area and a small set of measures that leaders must trust. A customer can replace the synthetic tables with its own value ledger, delivery system, and operating KPI sources. The domain owners then review the Pages, metric logic, agent sources, and benchmark questions.

> The first useful workshop output is a short list of executive questions, approved measures, source owners, and test questions. That gives the team a build plan and an acceptance test.

Ask the customer:

> Which recurring leadership decision would benefit most from one governed answer across metrics, definitions, and supporting evidence?

## Expected proof points

| Proof point | What to show |
|---|---|
| Shared meaning | A Page and the matching metric view measure. |
| Source authority | Page owner, certification signal, and verified SQL. |
| Structured and text context | A metric result and the related steering evidence. |
| Permission aware retrieval | Explain that users only retrieve sources they can access. |
| Reuse | The same metric view supports the dashboard and agents. |
| Quality control | A benchmark question with an approved SQL answer. |
| Portability | The bundle, Page sources, fixed data, and deployment guide in GitHub. |

## Recovery lines

If an answer differs from the expected wording, inspect the generated SQL and compare the numbers. Do not hide the difference. Say:

> The wording can vary. The acceptance test is the governed result. Let us inspect the SQL and the cited definition.

If a source is missing, say:

> The answer can only use sources that this user can access. We will check the asset permission and the Page publication state.

If a preview feature is unavailable, use the metric views, agents, dashboard, and committed Page files. State that the Page or Domain step depends on workspace preview access.

## Product status statement

Say this once if the customer asks about availability:

> As of 21 September 2026, the public documentation marks Genie Ontology and Domains as Public Preview and Pages as Beta. We will confirm region support, account access, and current terms for your workspace before planning production use.
