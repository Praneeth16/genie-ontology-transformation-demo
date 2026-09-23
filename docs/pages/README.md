# Import the Pages

The setup job creates the `Enterprise Transformation` domain and its three subdomains when the account allows it. Check the output of its `deploy_domains` task first. If that task printed a warning, fix the cause from `docs/DEPLOYMENT.md` and rerun the setup job before you import the Pages, because each Page belongs to a domain.

## Check the domain

Open Discover in the Databricks workspace and find the `Enterprise Transformation` domain. It should have this description:

> Governed terms, measures, data, and AI assets for enterprise transformation value realization, delivery risk, and operating performance.

Confirm that it has these subdomains:

- `Value Realization`
- `Delivery and Risk`
- `Operating Performance`

## Import the Pages

A Page's domain is fixed when the Page is created, and one Genie Code bulk import puts every
Page it creates into one domain. Import each domain separately, starting from that domain:

| Domain to open | Page files |
|---|---|
| `Enterprise Transformation` | `transformation-value-office.md` |
| `Value Realization` | `realized-value-to-date.md`, `forecast-value-at-completion.md`, `value-at-risk.md` |
| `Delivery and Risk` | `delivery-health.md`, `executive-intervention.md` |
| `Operating Performance` | `kpi-attainment.md`, `favorable-gap.md` |

For each row:

1. Open the domain or subdomain in Discover and choose Create page. The domain field shows
   the domain you opened.
2. In the Genie Code panel, choose Bulk import pages.
3. Paste the contents of the Page files for that row into the chat. Genie Code does not
   accept `.md` uploads. Add one sentence that names your catalog and schema, for example:
   "Resolve every table, view, and metric view under Related assets in
   `YOUR_CATALOG.YOUR_SCHEMA` and never in any other schema."
4. Review the proposal. An overlap warning between these Pages is expected, because they
   share metric views. Create the Pages as drafts.

Then open each draft and check its related assets before you publish it. Genie Code
resolves assets by name, so in a workspace with an older copy of the demo it can link a
table in the wrong schema or the wrong dashboard. Point each link at the schema and the
dashboard this deployment created, then publish the Page.

## Check the result

Ask Genie One this question:

> How is the Northstar transformation portfolio performing against the approved value case, and where should leadership intervene?

Open a citation in the answer. Confirm that the Page shows its domain, owner, synonyms, description, body, sources, and related assets.

If Genie One does not cite a Page, confirm that the Page is published and that the user can access its domain. Try the exact Page title or one of its synonyms in the question.

Genie One also reads recent activity. In a workspace that still holds an older copy of the demo, it can query the older schema or try an agent that was deleted. Remove old copies before a customer session.

## Safety

The Page files contain synthetic definitions only. Databricks Pages documentation warns against putting personal, regulated, or sensitive data in Page names, descriptions, synonyms, or body text. Keep customer data out of these demo Pages.
