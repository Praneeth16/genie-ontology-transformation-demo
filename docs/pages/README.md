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

Open Discover, then Pages, then Create page. Open Genie Code and choose Bulk import pages. Upload every Markdown file in this folder except this README.

Ask Genie Code to create each Page in the domain or subdomain named in its source file. Review the proposed Pages before creation. Resolve any duplicate or low confidence warning. Create the Pages as drafts.

For each draft, add the related metric view, dashboard, or Genie Agent through the Page editor. Publish the Page after the owner and related assets are correct.

## Check the result

Ask Genie One this question:

> How is the Northstar transformation portfolio performing against the approved value case, and where should leadership intervene?

Open a citation in the answer. Confirm that the Page shows its domain, owner, synonyms, description, body, sources, and related assets.

If Genie One does not cite a Page, confirm that the Page is published and that the user can access its domain. Try the exact Page title or one of its synonyms in the question.

## Safety

The Page files contain synthetic definitions only. Databricks Pages documentation warns against putting personal, regulated, or sensitive data in Page names, descriptions, synonyms, or body text. Keep customer data out of these demo Pages.
