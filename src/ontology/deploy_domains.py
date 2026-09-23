"""Create or update the demo domain and subdomains."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import BadRequest, InternalError, PermissionDenied
from databricks.sdk.service.domains import Domain
from databricks.sdk.service.tags import TagPolicy
from google.protobuf.field_mask_pb2 import FieldMask


def load_definition(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def ensure_tag_policy(
    client: WorkspaceClient,
    tag_key: str,
    description: str,
    existing_by_key: dict[str, TagPolicy],
) -> None:
    if tag_key in existing_by_key:
        print(f"Governed tag already exists: {tag_key}")
        return

    try:
        created = client.tag_policies.create_tag_policy(
            TagPolicy(tag_key=tag_key, description=description)
        )
    except (BadRequest, PermissionDenied) as exc:
        print(
            f"WARNING: Could not create governed tag {tag_key}: {exc}. The "
            "account may have reached its tag policy limit, or this identity "
            "may not have permission to create tag policies. The remaining "
            "demo setup can continue without the tag."
        )
        return
    existing_by_key[tag_key] = created
    print(f"Created governed tag: {tag_key} ({created.id})")


def upsert_domain(
    client: WorkspaceClient,
    spec: dict[str, str],
    existing_by_key: dict[tuple[str, str | None], Domain],
    parent_domain_id: str | None = None,
) -> Domain | None:
    key = (spec["tag_key"], parent_domain_id)
    existing = existing_by_key.get(key)
    domain = Domain(
        tag_key=spec["tag_key"],
        subtitle=spec["subtitle"],
        description=spec["description"],
        parent_domain_id=parent_domain_id,
        draft=False,
    )
    if existing:
        updated = client.domains.update_domain(
            existing.name,
            domain,
            FieldMask(paths=["subtitle", "description", "draft"]),
        )
        print(f"Updated domain: {spec['tag_key']} ({updated.domain_id})")
        return updated

    try:
        created = client.domains.create_domain(domain)
    except (BadRequest, InternalError) as exc:
        # A full account answers with an internal error rather than a clear
        # limit error. The documented limit is 300, but accounts can hold more,
        # so the count alone cannot predict the failure.
        print(
            f"WARNING: Could not create domain {spec['tag_key']}: {exc}. This account "
            f"returns {len(existing_by_key)} domains and subdomains and has probably "
            "reached its domain limit. The governed tags exist, and the remaining demo "
            "setup can continue. Remove unused domains or use another account, then "
            "run this task again."
        )
        return None
    print(f"Created domain: {spec['tag_key']} ({created.domain_id})")
    existing_by_key[key] = created
    return created


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--definition", required=True)
    args = parser.parse_args()

    definition = load_definition(Path(args.definition))
    client = WorkspaceClient()
    existing_tags_by_key = {
        tag_policy.tag_key: tag_policy
        for tag_policy in client.tag_policies.list_tag_policies(page_size=500)
    }

    root_spec = definition["root"]
    ensure_tag_policy(
        client,
        root_spec["tag_key"],
        root_spec["description"],
        existing_tags_by_key,
    )
    subdomain_specs = [
        {
            **subdomain,
            "tag_key": f"{root_spec['tag_key']}/{subdomain['tag_key']}",
        }
        for subdomain in definition["subdomains"]
    ]
    for subdomain_spec in subdomain_specs:
        ensure_tag_policy(
            client,
            subdomain_spec["tag_key"],
            subdomain_spec["description"],
            existing_tags_by_key,
        )

    try:
        existing_by_key = {
            (domain.tag_key, domain.parent_domain_id): domain
            for domain in client.domains.list_domains(page_size=500)
        }
        root = upsert_domain(client, root_spec, existing_by_key)
        if root is None:
            return
        for subdomain_spec in subdomain_specs:
            upsert_domain(client, subdomain_spec, existing_by_key, root.domain_id)
    except PermissionDenied:
        print(
            "WARNING: Domain setup was skipped because this identity is not "
            "authorized to access domains. The governed tags exist, and the "
            "remaining demo setup can continue. Ask an account admin to enable "
            "Domains or grant MANAGE DISCOVERY, then run this task again."
        )


if __name__ == "__main__":
    main()
