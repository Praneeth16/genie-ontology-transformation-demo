# Build status

## Research

- [x] Review the current public Genie Ontology documentation.
- [x] Review public guidance for Unity Catalog semantics, metric views, Domains, Pages, certification, and benchmarks.
- [x] Review internal demo guidance and keep internal links out of the public repository.
- [x] Inspect the reference screenshots and capture the citation experience in the script.

## Build

- [x] Create deterministic synthetic transformation data.
- [x] Create three governed metric views.
- [x] Add table and column descriptions, keys, and certification signals.
- [x] Create three focused Genie Agent definitions.
- [x] Add verified SQL and benchmark questions to each agent.
- [x] Create the executive AI/BI dashboard.
- [x] Add Page source files and import instructions.
- [x] Add data checks and the agent benchmark job.
- [x] Write the external demo script and question bank.

## Verification

- [x] Pass local Python and JSON checks.
- [x] Pass `databricks bundle validate` in the Praneeth workspace.
- [x] Deploy the bundle and run the data and semantic checks.
- [x] Confirm the dashboard datasets and visualizations through the workspace API.
- [x] Confirm all three agents and their committed context in the workspace.
- [x] Create the four governed tag policies required by the domain design.
- [ ] Create the live domain and subdomains. The Praneeth account returns 997 domains and subdomains, but the complete demo needs four open slots and only three remain. The setup creates none of the domain records until all four slots are available.
- [x] Run the benchmark job and record the result.
- [ ] Import and publish the Pages.

## Publication

- [x] Complete the two plain writing review passes.
- [x] Create the revision HTML for the demo script.
- [ ] Initialize Git and commit the repository.
- [ ] Create the public `Praneeth16/genie-ontology-transformation-demo` repository.
- [ ] Push the main branch and verify the public URL.

## Live Praneeth workspace

| Asset | ID or result |
|---|---|
| Catalog and schema | `serverless_lakebase_praneeth_catalog.transformation_value_office` |
| Executive dashboard | `01f1b5789f3e103cae57410028c69ae1` |
| Value Realization Agent | `01f1b579e3e91313b260a2324551dece` |
| Delivery Risk Agent | `01f1b579e483177a881fb7f237171b3a` |
| Operating Performance Agent | `01f1b579e51519ca962b328a317c0464` |
| Setup job | `243470960409207` |
| Regression job | `296598498581033` |
| Final setup run | `336462085665555`, passed |
| Final benchmark run | `947921635915108`, 12 of 12 passed, 0 need review |
| Governed tags | Enterprise Transformation and its three subdomain tags |
| Catalog domain assignments | 24 assignments across 11 assets |
| Workspace domain assignments | Dashboard root tag and root plus subdomain tags on all three agents |
| Domain card | Blocked by the account domain limit. The setup made no partial domain and deleted no existing domain. |
| Pages | Source files are committed. UI review and publication remain. |
