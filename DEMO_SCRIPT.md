# Genie Ontology executive demo

This guide supports a 20 minute customer conversation. It shows how an enterprise leader can move from a portfolio signal to a decision while every answer uses approved definitions, sources, and tests.

Northstar Group is fictional. All figures and documents in this demo are synthetic.

## Audience and outcome

Use this demo with enterprise Data and AI leaders, transformation leaders, and executive sponsors. By the end of the session, the audience should see how Databricks connects five parts of a trusted decision:

1. A business question in plain language.
2. A governed measure with one calculation.
3. The owner and meaning of the business term.
4. The supporting data and management evidence.
5. A test that checks the answer before it reaches a leadership meeting.

## Executive framing

Say:

> Leaders already have dashboards, status reports, and AI assistants. The harder problem is shared business context. A measure needs one definition, one owner, approved sources, and a clear test. This demo shows how Genie Ontology connects that context to the dashboards and agents that leaders use.

> We will follow one question from portfolio performance to the action that is due. We will then open the definition and calculation behind the answer. We will finish by showing the test results.

## Flow at a glance

| Act | Time | Open | Main question | Proof for the audience |
|---|---:|---|---|---|
| 1. Find the signal | 2 minutes | Executive dashboard | Where does the portfolio need attention? | The dashboard shows value, delivery, and operating signals from governed sources. |
| 2. Get the governed answer | 4 minutes | Value Realization Agent | How is the portfolio performing against the approved value case? | The answer uses the certified value metric view and shows its sources. |
| 3. Move to action | 4 minutes | Delivery Risk Agent | Where should the executive committee intervene this month? | The answer connects a signal to an owner, an overdue item, and recorded evidence. |
| 4. Inspect the business context | 5 minutes | Catalog Explorer | What does Value at Risk mean, how is it calculated, and what is it joined to? | The measure shows its definition, synonyms, expression, format, owner, tags, and certification. The metric view shows the modeled entity relationships. |
| 5. Search across the ontology | 3 minutes | Genie One | Which approved sources can answer the broader leadership question? | Genie One finds the dashboard and related ontology results that the user can access. |
| 6. Prove quality | 2 minutes | Benchmark run | Does the demo return the expected governed results? | All 14 benchmark questions pass across the three agents. |
| 7. Close with the customer path | 1 minute | Dashboard | Which leadership decision should we model first? | The audience leaves with a clear first workshop outcome. |

For a 10 minute version, run Acts 1, 2, 4, 6, and 7.

## Act 1. Find the signal

Open the Enterprise Transformation Value Office dashboard.

Say:

> Northstar Group has twelve transformation initiatives. Leaders approved 645 million dollars of value. The portfolio has realized 508.4 million dollars to date and forecasts 615 million dollars at completion. The current forecast leaves 36.8 million dollars at risk. Four initiatives need executive attention.

> The dashboard gives us the signal. It does not ask leaders to accept a number without context. We can open the same measures in an agent, inspect their definitions, and trace the supporting sources.

Point to these items:

- Approved value target.
- Realized value to date.
- Value at risk.
- Red initiatives.
- Value at risk by business unit.
- Operating KPIs below target.

Do not read every number. Give the audience one decision to follow.

Say:

> The decision is where leadership should intervene now to protect the approved value case.

## Act 2. Get the governed answer

Open the Northstar Value Realization Agent.

Ask:

> How is the transformation portfolio performing against the approved value case?

Let the answer finish before you speak.

The answer should show:

- 645 million dollars of approved target value.
- 549 million dollars of planned value to date.
- 508 million dollars of realized value to date.
- 615 million dollars of forecast value at completion.
- 36.8 million dollars of value at risk.
- 95.4 percent forecast attainment.
- 349 percent forecast return on approved investment, or 3.5 times.

Say:

> The agent has a focused job. It uses the certified value metric view and approved query patterns. The response separates realized value from forecast value. That distinction changes the management decision.

Expand Sources.

Say:

> The response shows the query results that support each claim. A reviewer can inspect the generated SQL and the source measure.

Then ask a question that most semantic layers get wrong:

> How did realized value and investment move at each quarter end?

Say:

> These monthly records are cumulative. Adding twenty months of a running total together
> gives a number many times larger than the approved 645 million dollar target, and it looks
> plausible on a chart. The governed measure handles it. It is defined as a semiadditive
> window that takes the closing month of whatever period you ask for, so a quarter returns
> its last month and never a sum.

> This is the difference between a metric view and a saved query. The rule lives with the
> measure, so every agent, dashboard, and BI tool inherits it. Nobody has to remember it.

## Act 3. Move from signal to action

Open the Northstar Delivery Risk Agent.

Ask:

> Where does the executive committee need to intervene this month?

The answer should start with four red initiatives. It should include the owner, schedule delay, overdue critical risks, value at risk, and the latest steering evidence.

Follow Network footprint redesign.

Ask:

> Who owns the next action for Network footprint redesign, what is due, and what decision must the executive committee make?

Open the cited Network steering memo.

Say:

> The structured record says that the initiative is red and 68 days late. The steering memo says that site consultation is late and that leaders need to decide the closure cost estimate. The answer connects the portfolio signal to an accountable owner and a recorded decision.

> The evidence explains why leaders should intervene. It does not prove that 36.8 million dollars has already been lost. Value at Risk is a forecast shortfall.

This distinction is part of the ontology. The term and the calculation stay consistent as the user moves from the dashboard to the agent and the evidence.

## Act 4. Inspect the business context

Open `mv_value_realization` in Catalog Explorer. Select Value at Risk.

Show these fields:

- The business name is Value at Risk.
- The description reads: the positive gap between approved target and forecast value at
  completion, summed by initiative. A forecast shortfall, not a loss already taken.
- The synonyms include forecast shortfall and target value at risk.
- The expression is `SUM(progress.value_at_risk_usd)`.
- The format is US dollars.
- The owner is named.
- The asset has the Enterprise Transformation and Value Realization tags.
- The asset is certified.
- The dashboard, setup job, and Value Realization Agent appear as related assets.

Say:

> Every measure in this view carries that description. It is not documentation that sits
> beside the data and drifts. It is part of the measure, so Catalog Explorer, the agents, and
> any BI tool read the same sentence. The warning in the description is the one that matters
> to this audience: a forecast shortfall is not a loss already taken.

Now open the metric view definition itself and point at the `joins` block.

Say:

> This is the part a customer should copy. The view does not start from a hand-written SQL
> join. It declares that the initiative is the entity, and that the reporting month record,
> the risk summary, the milestone summary, and the latest management document each join to it
> on `initiative_id`.

> The relationships are now part of the governed model. When someone asks a question that
> needs risk and value together, the agent does not have to invent a join, and it cannot get
> the grain wrong. Add a new fact next quarter and every existing measure keeps working.

> Many teams keep these relationships in a long hand-written SQL view. That view is exactly
> the thing an ontology replaces.

Say:

> The business term gives people shared meaning. The metric view gives the calculation and
> the relationships. The tags place the asset in a business area. Certification records that
> an owner approves the asset. Related assets show where that context is used.

> Genie Ontology can also use context from approved assets and their use. A governed
> definition remains the authority when inferred context conflicts with a critical business
> term.

## Act 5. Search across the ontology

Open Genie One.

Ask:

> How is the Northstar transformation portfolio performing against the approved value case, and where should leadership intervene this month?

Show the search steps before the final answer.

Say:

> Genie One found the Enterprise Transformation Value Office dashboard and four ontology results for this question. It selected sources that this user can access. The focused agents remain the approved source for detailed value, delivery, and operating questions.

> This gives leaders one entry point while the implementation keeps clear boundaries behind the scenes.

If the answer does not return the expected numeric detail, open the cited dashboard or the focused agent. Do not hide the difference.

Say:

> Genie One found the right context. We will now open the focused governed source for the exact number.

## Act 6. Prove quality

Open the successful regression run.

Show these results:

- Value Realization Agent. 5 of 5 correct.
- Delivery Risk Agent. 5 of 5 correct.
- Operating Performance Agent. 4 of 4 correct.
- No questions need review.

Say:

> The repository stores each benchmark question with an approved SQL answer. The run starts a new conversation for every question and compares the result with the approved answer. All 14 questions passed in this run.

> One of these tests exists only to catch the cumulative value mistake from earlier. If a
> future change breaks the semiadditive rule, the quarter end numbers climb past the approved
> target and this run fails before anyone sees it in a leadership meeting.

> User feedback does not change the agent by itself. An editor reviews a failure, corrects the definition, metadata, or approved SQL, and runs the benchmark again.

## Act 7. Close with the customer path

Return to the dashboard.

Say:

> We started with a portfolio signal. We obtained a governed answer and moved to the action that is due. We inspected the term, its definition, the calculation, the modeled relationships, the owner, and the related assets. We then checked the answer with a committed benchmark.

> A customer can replace the synthetic sources with its own portfolio ledger, delivery system, operating measures, and management documents. The first workshop should select one recurring leadership decision. The team should then agree on the measures, owners, sources, and test questions for that decision.

Ask:

> Which recurring leadership decision would benefit most from one governed answer across measures, definitions, and supporting evidence?

## What this demo proves

| Capability | Evidence in the demo |
|---|---|
| Shared business meaning | Metric names, descriptions, synonyms, owners, and tags are recorded in Unity Catalog. |
| Governed calculations | Metric views define value, delivery, and operating measures once. |
| Modeled relationships | The metric views declare `joins` from the initiative entity, so the entity graph is governed rather than rewritten per query. |
| Time rules that hold | Semiadditive window measures stop cumulative months being added together, in every tool that reads the measure. |
| Definitions that travel | Every field and measure carries its business definition, synonyms, and format. |
| Structured and document context | Agents use tables, metric views, and synthetic steering documents. |
| Clear agent roles | Three agents cover value realization, delivery risk, and operating performance. |
| Cross domain discovery | Genie One finds approved assets and ontology results that the user can access. |
| Traceable answers | Responses expose sources and generated SQL. |
| Quality control | A regression run checks 14 committed benchmark questions, including one that guards the cumulative value rule. |
| Repeatable deployment | The public repository deploys the data, dashboard, agents, and tests with a Databricks Asset Bundle. |

## Presenter guardrails

- State that Northstar Group and all data are synthetic.
- Say forecast when a result is forecast. Do not describe forecast value as realized value.
- Describe Value at Risk as a forecast shortfall. Do not say the value has already been lost.
- Describe operating results and initiative status together. Do not claim causation unless the source records it.
- Keep source facts separate from generated recommendations.
- Confirm current product availability, region support, and account access before the meeting.

## Recovery lines

If a benchmark question failed in the run you are showing, say:

> Generated SQL can differ between runs when a question has several valid query shapes. That
> is why the suite is committed and repeatable. We rerun it, and we investigate anything that
> fails twice rather than guessing.

Run the suite early enough before the session that you can rerun it once.

If the wording differs from the expected answer, say:

> The wording can vary. The acceptance test is the governed result. Let us inspect the SQL and the cited definition.

If a source is missing, say:

> The answer can only use sources that this user can access. We will check the asset permission and publication state.

If a preview feature is unavailable, say:

> We will continue with the metric views, focused agents, dashboard, and committed test results. We will confirm preview access before planning production use.

## Product status note

The public documentation marked Genie Ontology and Domains as Public Preview and Pages as Beta when this guide was prepared on 21 September 2026. Product status can change. Confirm current availability before a customer session.
