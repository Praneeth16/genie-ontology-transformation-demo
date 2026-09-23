# Verification status

Last updated 23 September 2026.

## Checked on every change

`make check` runs these with no workspace needed.

- [x] Ruff and byte compile checks for `src` and `tests`.
- [x] Metric view YAML renders, parses, and holds its contract: version 1.1, the `fields`
      keyword, a business definition and display name on every field and measure, no
      undeclared or unused joins, and a complete order, range, and semiadditive rule on every
      window measure.
- [x] Genie Agent and dashboard JSON parse.

## Checked on every setup run

The `validate_demo` task fails the setup job if any of these change.

- [x] Row counts, one row per initiative in each summary view, keys, and certification.
- [x] Every figure the demo script quotes: 645 million dollar target, 548.5 million dollar
      plan to date, 508.36 million dollars realized, 615.18 million dollar forecast, 36.84
      million dollars at risk, 95.4 percent attainment, a 3.49 times forecast return, four
      red initiatives, and 68 days slipped on Network footprint redesign.
- [x] The semiadditive period end measures return the closing month rather than a sum.
- [x] Domain tag membership of 16, 6, 9, and 3 assets, when the tag policies exist.

## Verified in a workspace

Deployed on 23 September 2026 into a clean schema.

- [x] `make deploy` creates the schema, the four metric views, the dashboard, the jobs, and
      the three Genie Agents, and every setup check passes.
- [x] A second deploy updates the three agents in place rather than creating copies.
- [x] When the account has reached its domain limit, the setup warns and continues.
- [x] `make benchmark` passes all 14 committed questions. A single question can fail on one
      run and pass on the next. See the note in `docs/DEPLOYMENT.md`.

## Not yet verified in a workspace

- [ ] Creating the domain and subdomains. The test account was at its domain limit.
- [ ] Importing and publishing the Pages, and the Page citation in Genie One (Acts 4 and 5 of
      `DEMO_SCRIPT.md`). There is no public Pages API, and each Page needs a domain.
- [ ] Dashboard and benchmark screenshots for this README.
