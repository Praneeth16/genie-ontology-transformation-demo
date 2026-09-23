# Genie One single chat script

This script runs the whole demo story in one Genie One conversation. Eight prompts move from
a portfolio question to an executive committee brief. Each prompt goes one level deeper, and
each one shows a different part of the ontology or of Genie One.

Northstar Group is fictional. All figures are synthetic, as at 31 August 2026.

This script was run end to end on 23 September 2026. The expected results below are the
figures that run returned, checked against the governed metric views. The watch outs are
the slips that run made, so the presenter knows them in advance.

## Before the session

- Deploy the demo, import and publish the Pages, and run the benchmark job. See `README.md`.
- Use a workspace with one copy of the demo. Genie One reads recent activity, and an older
  schema or a deleted agent from an earlier deployment can pull answers toward stale assets.
- Run the whole conversation once on the day. Each prompt takes one to three minutes, so the
  full run takes about 20 minutes. Show the finished thread in the session, and run one or two
  prompts live.
- Genie One may offer to remember your role after the first answer. Accepting shows the memory
  feature, and later answers recall it.

## Flow at a glance

| Turn | What the audience sees | Ontology or Genie One feature |
|---:|---|---|
| 1 | The headline value position | Ontology search, Pages, governed measures, a chart, memory |
| 2 | What Value at Risk means and why it is 36.8 million | Page definition, synonyms, a proof query |
| 3 | Shortfall by initiative, with owners and health | Synonym resolution, joins across value and delivery |
| 4 | One initiative in depth, with the steering memo | Documents, risks, milestones, facts kept separate from advice |
| 5 | Operating KPIs and a causation warning | A third domain, time windows, honest limits |
| 6 | Quarter end values on cumulative data | Semiadditive window measures, a chart |
| 7 | Every source, its certification, and a self check | Provenance, certification, correction against a governed measure |
| 8 | An executive committee brief | Document drafting, export, and sharing |

## The prompts

Paste each prompt into the same conversation, in order.

### Turn 1. The headline

> I run the Northstar transformation office. How is the portfolio performing against the
> approved value case as of the latest reporting date? Give me the headline numbers.

Expected: 645.0 million dollar approved target, 508.4 million realized (78.8 percent), 615.2
million forecast (95.4 percent), 36.8 million value at risk, four red initiatives, four
overdue critical risks, and seven overdue milestones. Value at risk by business unit is 11.3
million for Industrial Systems, 10.6 million for Digital Services, 8.8 million for Corporate,
and 6.2 million for Consumer Products.

Point to the search steps. Genie One reports ontology results, reads the dashboard, and opens
the Transformation Value Office, Realized Value to Date, and Forecast Value at Completion
Pages before it answers.

### Turn 2. The definition

> Before I take $36.8M to the executive committee: what exactly does Value at Risk mean here,
> how is it calculated, who owns the definition, and what else do people call it? Why is it
> not just target minus forecast?

Expected: the definition from the Value at Risk Page, the synonyms forecast shortfall, target
value at risk, and value shortfall, and a query that proves the rule. Target minus forecast is
29.8 million. Three initiatives forecast above target by 7.0 million combined, and those gains
do not offset shortfalls elsewhere, so the governed measure is 36.8 million.

Say:

> This is the definition doing its job. A naive subtraction gives 29.8 million. The approved
> rule gives 36.8 million, and the agent explains the difference from the governed Page.

### Turn 3. Shortfall, ownership, and health

> Which initiatives carry the biggest forecast shortfall, who is accountable for each, and
> which of them are red right now?

Expected: all twelve initiatives ranked by value at risk with owner and sponsor. The four red
initiatives total 28.8 million: Network footprint redesign 8.9 million, Shared services
consolidation 8.8 million, Service operations automation 7.4 million, and Demand planning
transformation 3.7 million. The four amber initiatives total 8.1 million. The four green
initiatives have no value at risk.

The prompt says forecast shortfall, a Page synonym, and Genie One resolves it to Value at Risk.

### Turn 4. One initiative in depth

> Go deep on Network footprint redesign. What is overdue, which critical risk is driving it
> and what mitigation was recorded, what does the latest steering memo actually say, and what
> decision does the executive committee need to make? Keep recorded facts separate from your
> own recommendations.

Expected: 68 days slipped, the overdue Scale rollout milestone, the critical risk RSK-001
Site consultation delay with its recorded mitigation, the 18 August 2026 Network steering memo
quoted word for word, and the September investment decision. The answer ends with a separate
section of observations that are not in the data.

### Turn 5. Business outcomes

> Now step back to business outcomes. Are the operating KPIs in Industrial Systems and Digital
> Services moving in the right direction? Compare the latest month with the trailing three
> month average, and say plainly if the data does not show that the initiatives caused the
> change.

Expected: August KPIs against target and against the trailing average for both business
units, a chart of the favorable gap, and a clear statement that the data shows correlation
and not causation.

### Turn 6. The time rule

> Show me realized value and investment at each quarter end as a chart. The monthly records are
> cumulative, so make sure you are not adding months together.

Expected: Genie One uses the period end measures in `mv_value_trend`. Realized value runs
46.7, 119.0, 201.4, 285.0, 369.8, and 455.8 million at the quarter ends from March 2025 to
June 2026, and 508.4 million in August 2026. No value exceeds the 645 million dollar target.

Say:

> The rule that stops cumulative months being added together lives in the metric view, so a
> general assistant inherits it without being told how.

### Turn 7. Provenance and a self check

> Before I trust any of this: which sources, metric views, and business definitions did you
> use across this conversation? Which are certified, which domain and subdomain owns each, and
> where did you compute something yourself instead of using a governed measure? Also re-check
> the approved investment total using the governed Approved Investment measure.

Expected: a list of the metric views, tables, and Pages it used, their certification, and the
figures it calculated itself rather than read from a governed measure. The approved investment
check returns 137.0 million dollars.

### Turn 8. The brief

> Draft a one page executive committee brief from this conversation: the headline value
> position, the four interventions with owner and decision needed, the operating outcome
> picture, and a short note on which figures are governed and certified. Keep recorded facts
> separate from recommendations.

Expected: Genie One opens an editable document beside the chat with the value table, the four
interventions and the decision each needs, the KPI tables, a causation note, and a governance
note. Use Export or Share on the document, and Share on the conversation.

## Watch outs from the verification run

Read the brief before you show it. The verification run made these slips. Each one has a line
that turns it into a point about governance.

| Where | What it said | What is true | Line to use |
|---|---|---|---|
| Turn 6 | An approved investment envelope of 108.5 million | 137.0 million, the governed `Approved Investment` measure | Turn 7 asks it to re-check against the governed measure, and it corrects itself. |
| Turn 8 | Four of twelve initiatives carry a shortfall and eight are on or above target | Eight carry a shortfall and four are on or above target | Correct it in the document. A drafted brief is a starting point for the owner, not a published fact. |
| Turns 7 and 8 | Milestones, risks, and `v_initiative_current` are not certified | All twelve curated tables and views are certified | This came from an older copy of the demo in the same workspace. Remove old copies before the session. |
| Turn 4 | Days overdue counted up to today | The reporting date is 31 August 2026 | The governed slip is 68 days, as the dashboard shows. |
| Turn 5 | A May to July average | The governed `Actual Three Month Average` covers June to August | Point out that the governed measure exists and that the agent chose its own window. |
| Any turn | "Failed to get asset info" for a Genie agent | The search index still lists an agent that was deleted | Harmless. Genie One falls back to the dashboard and the tables. |

Generated answers can vary between runs. When a number differs from this script, open the
governed measure and show the difference rather than hiding it. That is the point of the
ontology.
