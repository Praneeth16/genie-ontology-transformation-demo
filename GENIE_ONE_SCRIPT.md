# Genie One single chat script

This script tells the whole demo story in one Genie One conversation. The presenter plays the
head of the Northstar transformation office, who prepares the monthly executive committee
review. Eleven prompts move from a portfolio question to a committee brief, and then to a
routine that runs without the presenter.

Northstar Group is fictional. All figures are synthetic, as at 31 August 2026.

This script was run end to end on 23 September 2026. The expected results below are the
figures that run returned, checked against the governed metric views. The watch outs are
the slips that run made, so the presenter knows them in advance.

## The story

| Part | Turns | The leader's question | What it shows |
|---|---|---|---|
| Understand | 1 and 2 | Where do we stand, and what does the number mean? | Ontology search, Pages, governed measures, memory |
| Diagnose | 3 and 4 | Where is the problem, and why? | Synonyms, joins across value and delivery, documents |
| Check outcomes | 5 and 6 | Is the business improving, and is the trend real? | A third domain, time windows, semiadditive measures |
| Trust | 7 | Can I defend this in the room? | Provenance, certification, what was computed |
| Act | 8 | What do I take to the committee? | Document drafting, export, and sharing |
| Make it repeatable | 9, 10, and 11 | How do I stop doing this by hand every month? | A skill, a new agent, and a scheduled task, each created from the chat |

The last three turns follow from the brief. Having built one good brief, the leader saves the
method, hands the day to day questions to the sponsors, and puts the whole review on a
schedule.

## Before the session

- Deploy the demo, import and publish the Pages, and run the benchmark job. See `README.md`.
- Use a workspace with one copy of the demo. Genie One reads recent activity and memory, and
  an older schema or a deleted agent from an earlier deployment can pull answers toward stale
  assets.
- Open Customizations in Genie One and check the saved memory. If it names Genie Agent IDs
  that no longer exist, edit or remove them.
- Run the whole conversation once on the day. Each prompt takes one to three minutes, so the
  full run takes about 30 minutes. Show the finished thread in the session, and run one or two
  prompts live.
- Turns 9 to 11 create a skill, a Genie Agent, and a scheduled task in the workspace. Rename or
  remove them after a rehearsal so the live run creates them fresh.

## The prompts

Paste each prompt into the same conversation, in order.

### Turn 1. The headline

> I run the Northstar transformation office and prepare the monthly executive committee
> review. How is the portfolio performing against the approved value case as of the latest
> reporting date? Give me the headline numbers.

Expected: 645.0 million dollar approved target, 548.5 million planned to date, 508.4 million
realized, 615.2 million forecast (95.4 percent attainment), 36.8 million value at risk, 137.0
million approved investment, and a 3.49 times forecast return.

Point to the search steps. Genie One reports ontology results, finds the Northstar Value
Realization agent, and reads the Pages before it answers. It then offers to remember your
role. Accept it, and later answers recall it.

### Turn 2. The definition

Use this prompt if the first answer describes Value at Risk as target minus forecast, which
the verification run did:

> You labelled Value at Risk as target minus forecast, but $645M minus $615.2M is $29.8M, not
> $36.8M. Before I take this to the executive committee: what exactly does Value at Risk mean
> here, how is it calculated, who owns the definition, and what else do people call it?

Otherwise use:

> Before I take $36.8M to the executive committee: what exactly does Value at Risk mean here,
> how is it calculated, who owns the definition, and what else do people call it? Why is it
> not just target minus forecast?

Expected: the definition from the Value at Risk Page, the owner, and the synonyms forecast
shortfall, target value at risk, and value shortfall. It proves the rule on initiative data:
eight initiatives carry a shortfall summing to 36.8 million, three forecast above target by 7.0
million combined, and those gains do not offset the shortfalls.

The verification run also separated this term from a capital markets Value at Risk Page in
another domain. Point that out: domains keep two teams' meanings apart.

### Turn 3. Shortfall, ownership, and health

> Which initiatives carry the biggest forecast shortfall, who is accountable for each, and
> which of them are red right now?

Expected: the four red initiatives carry 28.8 million, 78 percent of the value at risk.
Network footprint redesign 8.9 million, Shared services consolidation 8.8 million, Service
operations automation 7.4 million, and Demand planning transformation 3.7 million, each with
owner, sponsor, days slipped, and the overdue critical risk. The four amber initiatives carry
8.1 million.

The prompt says forecast shortfall, a Page synonym, and Genie One resolves it to Value at Risk.

### Turn 4. One initiative in depth

> Go deep on Network footprint redesign. What is overdue, which critical risk is driving it
> and what mitigation was recorded, what does the latest steering memo actually say, and what
> decision does the executive committee need to make? Keep recorded facts separate from your
> own recommendations.

Expected: 68 days slipped, the overdue Scale rollout milestone, the critical risk RSK-001 Site
consultation delay with its recorded mitigation, the 18 August 2026 Network steering memo
quoted word for word, and the September investment decision. Observations that are not in the
data sit in a separate section at the end.

### Turn 5. Business outcomes

> Now step back to business outcomes. Are the operating KPIs in Industrial Systems and Digital
> Services moving in the right direction? Use the governed Actual Three Month Average to compare
> with the latest month, and say plainly if the data does not show that the initiatives caused
> the change.

Expected: all twelve KPIs are better in August than their governed three month average.
Industrial Systems has four of six above target and Digital Services two of six. For example,
Industrial Systems EBITDA margin is 18.59 percent against an 18.09 percent average. The answer
says the data shows correlation, not causation.

### Turn 6. The time rule

> Show me realized value and investment at each quarter end as a chart. The monthly records are
> cumulative, so make sure you are not adding months together.

Expected: Genie One uses the period end measures in `mv_value_trend`. Realized value runs 46.7,
119.0, 201.4, 285.0, 369.8, and 455.8 million at the quarter ends from March 2025 to June 2026,
and 508.4 million in August 2026. Investment reaches 99.9 million of the 137.0 million approved.

Say:

> The rule that stops cumulative months being added together lives in the metric view, so a
> general assistant inherits it without being told how.

### Turn 7. Provenance

> Before I trust any of this: which sources, metric views, and business definitions did you
> use across this conversation? Which are certified, which domain and subdomain owns each, and
> where did you compute something yourself instead of using a governed measure?

Expected: every metric view, table, Genie Agent, and Page it used, with its domain and
subdomain, and a list of the figures it calculated itself, such as the 40.2 million gap to
plan.

### Turn 8. The brief

> Draft a one page executive committee brief from this conversation: the headline value
> position, the four interventions with owner and decision needed, the operating outcome
> picture, and a short note on which figures are governed. Keep recorded facts separate from
> recommendations.

Expected: an editable document beside the chat with the value table, the four interventions
with owner, sponsor, recorded mitigation, and decision needed, the KPI tables, a causation
caveat, and a governance note. Use Export or Share on the document.

### Turn 9. Save the method as a skill

> This is exactly how I want every monthly committee brief built. Save the method as a skill my
> team can reuse: use the governed Value at Risk from mv_value_realization, never target minus
> forecast; take quarter end values from the period end measures in mv_value_trend; apply the
> decision rule from the Transformation Value Office page; keep recorded facts separate from
> recommendations; and end with a note on which figures are governed.

Expected: Genie One creates a skill, named `northstar-committee-brief` in the verification run,
and says it will load when anyone asks for the committee brief.

Say:

> The governed definitions protect the numbers. The skill protects the method. A new analyst
> gets the same brief as the head of the office.

### Turn 10. Create an agent for the sponsors

> Between reviews my executive sponsors keep asking me the same questions about their own
> initiatives. Create an agent for them called Northstar Sponsor Desk that answers only from
> the Northstar value and delivery sources, follows the same rules as the committee brief
> skill, and says so when a question falls outside the transformation portfolio.

Expected: Genie One checks access to each source, then creates a Genie Agent with the four
certified metric views and the risks, milestones, and document tables, instructions that carry
the skill's rules, a scope boundary, and example questions. Open it from Agents to show it.

### Turn 11. Put it on a schedule

> Last step: make this a routine. On the first business day of every month, prepare the
> committee brief with that skill for the latest reporting month and send it to me, and call out
> any initiative that has turned red since the previous month.

Expected: a scheduled task, named Northstar Monthly Committee Brief in the verification run,
with a Run now button. The schedule cannot express first business day, so Genie One sets the
first of the month and says so.

Close with:

> We started with one question. We ended with a governed answer, a brief for the committee, a
> method the team can reuse, an agent for the sponsors, and a review that runs itself. Every
> step used the same definitions.

## Watch outs from the verification run

Read each answer before you show it. The verification run made these slips. Each one has a
line that turns it into a point about governance.

| Where | What it said | What is true | Line to use |
|---|---|---|---|
| Turn 1 | Value at Risk is target minus forecast | It is summed per initiative with a zero floor | Use the first version of Turn 2. The correction is the point of the demo. |
| Turn 2 | Four initiatives forecast above target | Three are above target and one is exactly on target | The governed total is unaffected. Open the per initiative table. |
| Turn 7 | Risks, milestones, documents, and `v_initiative_current` are not certified | All twelve curated tables and views are certified | Open the table in Catalog Explorer and show the certified badge. |
| Turn 4 | Days overdue counted up to today | The reporting date is 31 August 2026 | The governed slip is 68 days, as the dashboard shows. |
| Turn 11 | The first of the month | The prompt asked for the first business day | Genie One says so itself. Ask it to move the day if you want. |
| Any turn | A Genie Agent was "trashed" or "Failed to get asset info" | A saved memory or the search index names a deleted agent | Harmless. Genie One falls back to the live agent and the tables. Clean the memory before the session. |

An earlier run also stated a 108.5 million dollar approved investment in the quarter end turn
and flipped the count of initiatives with a shortfall in the brief. Neither happened in this
run, but check both figures. Approved investment is 137.0 million, and eight initiatives carry
a shortfall.

Generated answers can vary between runs. When a number differs from this script, open the
governed measure and show the difference rather than hiding it. That is the point of the
ontology.
