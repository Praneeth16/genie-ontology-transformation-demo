# Public sources

The repository uses public sources for every published product claim. Internal Databricks material helped with demo design but is not cited or copied here.

Checked on 21 September 2026.

- [Genie Ontology](https://docs.databricks.com/aws/en/genie/genie-ontology)
- [Unity Catalog semantics](https://docs.databricks.com/aws/en/uc-semantics)
- [Unity Catalog metric views](https://docs.databricks.com/aws/en/uc-semantics/metric-views)
- [Metric view YAML syntax reference](https://docs.databricks.com/aws/en/uc-semantics/metric-views/yaml-reference)
- [Tutorial: build a metric view with joins and data modeling](https://docs.databricks.com/aws/en/uc-semantics/metric-views/tpch-example)
- [Agent metadata in metric views](https://docs.databricks.com/aws/en/uc-semantics/agent-metadata)
- [Resource limits](https://docs.databricks.com/aws/en/resources/limits)
- [SET TAG](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-set-tag)
- [Domains and subdomains](https://docs.databricks.com/aws/en/uc-semantics/domains)
- [Pages](https://docs.databricks.com/aws/en/uc-semantics/pages)
- [Apply tags to Unity Catalog objects](https://docs.databricks.com/aws/en/database-objects/tags)
- [Manage dashboard tags](https://docs.databricks.com/aws/en/dashboards/manage/settings#tags)
- [Add tags to a Genie Agent](https://docs.databricks.com/aws/en/genie-agents/set-up#tags)
- [Flag data as certified or deprecated](https://docs.databricks.com/aws/en/data-governance/unity-catalog/certify-deprecate-data)
- [Test and monitor a Genie Agent](https://docs.databricks.com/aws/en/genie-agents/monitor)
- [Databricks Asset Bundle resources](https://docs.databricks.com/aws/en/dev-tools/bundles/resources)
- [Operationalizing Genie Ontology in your data stack](https://www.databricks.com/blog/operationalizing-genie-ontology-your-data-stack)

## Claims to recheck before a customer session

- Genie Ontology preview status and region support.
- Domains preview status.
- Pages Beta status, storage, and encryption guidance.
- Genie Agent benchmark limits and required permissions.
- Support for the Genie Agent export format used by the workspace.
- The account limit on domains and subdomains combined, which `src/ontology/deploy_domains.py` reads as 300.
- Metric view YAML support for `joins`, `window` measures, and the `fields` keyword in the target workspace.
