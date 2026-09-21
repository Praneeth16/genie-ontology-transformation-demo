"""Apply governed domain tags to the demo dashboard and Genie Agents."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.tags import TagAssignment


def load_manifest(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        manifest = json.load(handle)
    if not manifest.get("dashboard") or not manifest.get("agents"):
        raise ValueError("Manifest must define the dashboard and at least one agent")
    return manifest


def list_spaces(client: WorkspaceClient) -> dict[str, Any]:
    spaces: dict[str, Any] = {}
    page_token: str | None = None
    while True:
        response = client.genie.list_spaces(page_size=100, page_token=page_token)
        for space in response.spaces or []:
            if space.title:
                spaces[space.title] = space
        page_token = response.next_page_token
        if not page_token:
            return spaces


def ensure_tags(
    client: WorkspaceClient,
    entity_type: str,
    entity_id: str,
    tag_keys: list[str],
) -> None:
    existing = {
        assignment.tag_key
        for assignment in client.workspace_entity_tag_assignments.list_tag_assignments(
            entity_type,
            entity_id,
        )
    }
    for tag_key in tag_keys:
        if tag_key in existing:
            print(f"Governed tag already present: {entity_type} {entity_id} {tag_key}")
            continue
        try:
            client.workspace_entity_tag_assignments.create_tag_assignment(
                TagAssignment(
                    entity_type=entity_type,
                    entity_id=entity_id,
                    tag_key=tag_key,
                )
            )
        except Exception as exc:  # noqa: BLE001  # Tag policies can be missing in restricted accounts.
            print(
                f"WARNING: Could not apply governed tag {tag_key} to "
                f"{entity_type} {entity_id}: {exc}"
            )
            continue
        print(f"Applied governed tag: {entity_type} {entity_id} {tag_key}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dashboard-id", required=True)
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()

    manifest = load_manifest(Path(args.manifest))
    client = WorkspaceClient()

    ensure_tags(
        client,
        "dashboards",
        args.dashboard_id,
        manifest["dashboard"]["domain_tags"],
    )

    spaces = list_spaces(client)
    for agent in manifest["agents"]:
        space = spaces.get(agent["title"])
        if space is None:
            raise ValueError(f"Genie Agent was not found: {agent['title']}")
        ensure_tags(
            client,
            "geniespaces",
            space.space_id,
            agent["domain_tags"],
        )


if __name__ == "__main__":
    main()
