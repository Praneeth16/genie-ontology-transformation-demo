# Build status

Last updated 21 September 2026.

## Verified locally

These pass with `make check` and `databricks bundle validate`, with no workspace needed for
the first three.

- [x] Ruff and byte compile checks for `src` and `tests`.
- [x] Metric view YAML renders, parses, and holds its contract: version 1.1, the `fields`
      keyword, a business definition and display name on every field and measure, no
      undeclared or unused joins, and a complete order, range, and semiadditive rule on every
      window measure.
- [x] Genie Agent and dashboard JSON parse.
- [x] `databricks bundle validate` passes for the `dev` target.

## Verified in a workspace before the joins and window rework

These were confirmed against the earlier version of the semantic layer, which flattened the
entity graph into a single SQL view.

- [x] Deployed the bundle and passed the data and semantic checks.
- [x] Confirmed the dashboard datasets and visualizations through the workspace API.
- [x] Confirmed all three agents and their committed context in the workspace.
- [x] Created the four governed tag policies required by the domain design.
- [x] Ran the benchmark job and recorded the result.
- [x] Deployed from a clean public clone into a second workspace and passed all benchmarks.

## Verified in a workspace after the joins and window rework

Deployed to a live workspace on 21 September 2026, into a clean schema.

- [x] `make deploy` creates all four metric views, including the `joins` blocks and the
      window measures.
- [x] The governed measures return the committed values: 645 million dollar target,
      615.18 million dollar forecast, 36.84 million dollars at risk, 95.4 percent attainment.
- [x] `mv_value_trend` period end measures return one closing row per quarter, rising to the
      508.36 million dollar August closing and never exceeding the approved target.
- [x] The certification tags apply to all twelve curated tables and views, now that the
      metric views are tagged as `VIEW` rather than `TABLE`.
- [x] Domain tag membership matches the design: 16, 6, 9, and 3 assets.
- [x] `make benchmark` passes all 14 committed questions. One Operating Performance question
      failed on the first attempt and passed on the retry, so the suite is not deterministic.
      See the note in `docs/DEPLOYMENT.md`.

## Needs a workspace run

- [ ] Create the live domain and subdomains in an account with four available domain slots.
- [ ] Import and publish the Pages.

## Publication

- [x] Complete the plain writing review passes.
- [x] Create the revision HTML for the demo script.
- [x] Initialize Git and commit the repository.
- [x] Create the public repository.
- [x] Push the main branch and verify the public URL.
- [ ] Add dashboard and benchmark run screenshots to the README.
