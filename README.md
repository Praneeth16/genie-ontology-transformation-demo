# Genie Ontology enterprise transformation demo

This repository builds a customer demo of Genie Ontology for an enterprise transformation value office. It gives a consulting team one synthetic portfolio with governed measures, business definitions, delivery evidence, three focused Genie Agents, an executive dashboard, and benchmark tests.

Northstar Group is fictional. The repository contains no customer data or internal Databricks content.

## What the demo proves

- Unity Catalog metric views define value, delivery, and operating measures once.
- Unity Catalog metadata records ownership, definitions, relationships, and certification signals.
- Pages define the business terms that leaders use in transformation reviews.
- Three Genie Agents answer focused questions with verified SQL examples.
- An AI/BI dashboard uses the same governed data as the agents.
- Benchmarks compare generated results with committed SQL answers.
- Genie One can show which governed and inferred sources supported an answer.

See [DEMO_SCRIPT.md](DEMO_SCRIPT.md) for the customer talk track and [docs/ONTOLOGY.md](docs/ONTOLOGY.md) for the full ontology map.

## Build it

You need Python 3.12, `uv`, `jq`, Databricks CLI 1.14 or later, and access to a Databricks workspace with serverless compute. The workspace must have Genie, Genie One, Unity Catalog metric views, Domains, and Pages enabled.

The default target uses Praneeth's Lakebase workspace. It deploys into the existing `serverless_lakebase_praneeth_catalog` catalog.

```bash
databricks auth login --profile fe-vm-lakebase-praneeth \
  --host https://fevm-serverless-lakebase-praneeth.cloud.databricks.com

make deploy PROFILE=fe-vm-lakebase-praneeth TARGET=praneeth
```

The command validates the bundle and deploys the dashboard and jobs. The setup job creates the governed domain tags, synthetic data, and metric views. It applies domain tags to the catalog and workspace assets, runs data checks, and creates or updates the three Genie Agents. It also creates the domain and subdomains when the account has room.

If the Databricks account does not have room for the root and all three subdomains, the setup creates none of them. It keeps the required governed tags and continues to the agents. It does not delete an existing domain. See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for the recovery step.

Run the benchmark suite after the setup job finishes.

```bash
make benchmark PROFILE=fe-vm-lakebase-praneeth TARGET=praneeth
```

For another workspace, update the `dev` target values in `databricks.yml`, then deploy with `TARGET=dev` and the matching profile.

## Import the Pages

The setup job creates the domain and subdomains through the current Domains API. It uses the public Beta workspace tag API to add the dashboard and three Genie Agents to their matching governed tags. Databricks does not yet expose a stable public Pages API. Import the committed Page files after the bundle deploys. The process takes a few minutes and is described in [docs/pages/README.md](docs/pages/README.md).

The bundle remains the source for data, metric views, agents, the dashboard, and tests. The Page files remain the source for the business definitions.

## Repository map

| Path | Purpose |
|---|---|
| `src/data/build_demo.py` | Creates deterministic synthetic data, views, metric views, metadata, relationships, and certification tags. |
| `src/data/validate_demo.py` | Checks row counts, invariants, and governed measures. |
| `src/ontology` | Creates domains and governed tags for catalog and workspace assets. |
| `src/genie` | Stores the three agent definitions, verified SQL, benchmarks, and deployment scripts. |
| `src/dashboards` | Stores the executive AI/BI dashboard. |
| `docs/pages` | Stores the Page source files and import instructions. |
| `resources` | Defines the Databricks bundle resources and jobs. |
| `DEMO_SCRIPT.md` | Gives the external customer talk track. |
| `QUESTION_BANK.md` | Lists the questions to use in Genie One and the focused agents. |

## Product status

The public Databricks documentation marked Genie Ontology and Domains as Public Preview and Pages as Beta when this repository was prepared on 21 September 2026. Preview access and supported regions can change. Check [docs/SOURCES.md](docs/SOURCES.md) before a customer session.

## Design choices

The demo uses three focused agents instead of one large agent. Each agent has a clear decision boundary and a small source set. This makes wrong answers easier to trace and benchmark.

The setup uses a fixed reporting date of 31 August 2026. A fixed date keeps query results and benchmark results stable across deployments.

The committed JSON is the source of truth for the three Genie Agents. A deployment replaces the configuration of a live agent with the same title. Export and merge any workspace edits that you want to keep before you deploy.

Pages require a short import step. The repository uses the public Domains API and does not call an unpublished Pages API.

## License

This project uses the MIT License.
