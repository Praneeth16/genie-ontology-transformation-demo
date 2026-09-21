# Deployment guide

## Prerequisites

The deployer needs access to the target workspace, permission to use the serverless SQL warehouse, and permission to create a schema in the selected catalog. The deployer also needs permission to create jobs, dashboards, and Genie Agents.

Pages and Domains must be enabled in the account preview settings. The deployer needs permission to create governed tag policies and needs `MANAGE DISCOVERY` to create the domain and subdomains. A Page owner or curator must review and publish the Pages.

## Configure a workspace

Choose values for your workspace.

| Setting | Value |
|---|---|
| Profile | A Databricks CLI profile for the target workspace |
| Workspace | The target Databricks workspace URL |
| Catalog | An existing Unity Catalog catalog |
| Schema | `transformation_value_office` or another demo schema |
| SQL warehouse | A serverless SQL warehouse ID |

Authenticate and deploy.

```bash
databricks auth login --profile YOUR_PROFILE \
  --host https://YOUR_WORKSPACE_HOST

make deploy \
  PROFILE=YOUR_PROFILE \
  CATALOG=YOUR_CATALOG \
  WAREHOUSE_ID=YOUR_SQL_WAREHOUSE_ID
```

Add `SCHEMA=YOUR_SCHEMA` if you want a different schema name. The `dev` target is the default, so you do not need to pass `TARGET`.

The deploy command runs four stages.

1. It checks Python and JSON files locally.
2. It validates and deploys the bundle resources.
3. It creates the governed tags and the domain records when the account has room.
4. It creates the data and semantic layer, applies the domain tags to the catalog assets, validates the data, and creates or updates the Genie Agents.

Domains and subdomains share one account wide limit of 300 combined. The setup checks whether the account has room for the root and all three subdomains before it creates any of them. If there is not enough room, the setup keeps the governed tags, prints a warning, and continues to the Genie Agents. A curator must remove unused domains or choose another account before rerunning the domain task. The setup never deletes an existing domain.

The same warning path applies when the deploying identity is not authorized to access domains. The setup keeps the governed tags and continues. Ask an account admin to enable Domains or grant `MANAGE DISCOVERY`, then rerun the setup job to create the domain and subdomains.

If the account cannot create the governed tag policies at all, no asset receives a domain tag. The data checks report a warning in that case rather than failing, so the run still reaches the Genie Agents and the dashboard. Partial tagging is still treated as a failure, because it means something changed rather than something was unavailable.

## Check workspace asset tags

After the bundle finishes, open the Enterprise Transformation domain in Discover. Confirm that the executive dashboard has the root domain tag. Confirm that each Genie Agent has the root domain tag and its matching Value Realization, Delivery and Risk, or Operating Performance subdomain tag.

The setup job applies these tags through the public Beta workspace tag API because the current bundle schema does not expose them as resource fields.

## Pages and domain

Follow [pages/README.md](pages/README.md) after the bundle deploys. Page review and publication are the only manual setup steps.

## Regression test

Run the committed benchmark suite.

```bash
make benchmark \
  PROFILE=YOUR_PROFILE \
  CATALOG=YOUR_CATALOG \
  WAREHOUSE_ID=YOUR_SQL_WAREHOUSE_ID
```

The job fails if any benchmark result is wrong, incomplete, or marked for review. A benchmark run uses model inference and can take several minutes.

A run is not deterministic. Generated SQL can differ between runs for a question that has
several valid query shapes, so an occasional single question can fail and then pass on a
rerun. In the reference verification run, one Operating Performance question failed on the
first attempt and all fourteen passed on the retry. Rerun the job before treating a single
failed question as a regression, and investigate a question that fails repeatedly. Before a
customer session, run the job early enough to rerun it once.

## Source of truth for agents

The JSON files in `src/genie` are the source of truth for the three demo agents. A deployment replaces the matching live agent configuration. Export and merge any useful workspace edits before you deploy, or the deployment will overwrite them.

The deployment only considers agents in its own folder, which defaults to
`/Workspace/Users/<you>/genie-ontology-transformation-demo`. An agent elsewhere in the
workspace that happens to share a title is never modified. Set the `agent_parent_path`
bundle variable to move the folder.

Do not commit personal access tokens, workspace configuration files, or exported customer data.

## Troubleshooting

Run `make check` first. It renders every metric view definition and validates the YAML, the business definitions, the join declarations, and the window rules without a workspace. Most metric view problems surface there.

If metric view creation still fails in the workspace, check that the workspace supports metric view YAML version 1.1 and Databricks Runtime 17.3 or later, which `joins`, `window` measures, and the `fields` keyword require. Also check that the serverless job uses client version 4.

If a governed measure returns a number far larger than the approved 645 million dollar target, a semiadditive window measure is being treated as a plain sum. Confirm that `mv_value_trend` was created with its `window` blocks intact.

If a metric view reports fewer than twelve initiatives, one of the four summary views is no longer returning exactly one row per initiative. `validate_demo.py` checks each of them and names the one that broke.

If an agent cannot query a metric view, grant the user `USE CATALOG`, `USE SCHEMA`, and `SELECT` on the source objects. The user also needs permission to use the SQL warehouse and run the agent.

If the Page citation does not appear, confirm that the Page is published, the user can access its domain, and the question uses a Page title or synonym. Draft Pages are only available to the Page owner.

If a benchmark is marked for review, confirm that its SQL answer is present and returns fewer than 5,000 rows. Review any generated SQL before changing the expected answer.
