"""Apply governed domain tags to the demo dashboard and Genie Agents."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound, PermissionDenied
from databricks.sdk.service.tags import TagAssignment


def load_manifest(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        manifest = json.load(handle)
    if not manifest.get("dashboard") or not manifest.get("agents"):
        raise ValueError("Manifest must define the dashboard and at least one agent")
    return manifest


def normalized_path(path: str | None) -> str | None:
    """Reduce a workspace path to a comparable form.

    `get_space` returns a folder as `/Users/<user>/<folder>` while the bundle
    variable spells it `/Workspace/Users/<user>/<folder>`. Comparing the raw
    strings never matches, and a missed match makes a deployment create a second
    space with the same title instead of updating the existing one.
    """
    if path is None:
        return None
    trimmed = path.rstrip("/")
    if trimmed.startswith("/Workspace/"):
        trimmed = trimmed[len("/Workspace") :]
    return trimmed or "/"


def spaces_by_title(client: WorkspaceClient) -> dict[str, list[Any]]:
    """List every visible Genie space once, grouped by title."""
    spaces: dict[str, list[Any]] = {}
    page_token: str | None = None
    while True:
        response = client.genie.list_spaces(page_size=100, page_token=page_token)
        for space in response.spaces or []:
            if space.title:
                spaces.setdefault(space.title, []).append(space)
        page_token = response.next_page_token
        if not page_token:
            return spaces


def space_parent_path(client: WorkspaceClient, space: Any) -> str | None:
    """Return the folder that holds a space.

    `list_spaces` leaves `parent_path` unset, so the folder has to be read from
    the space itself.
    """
    if space.parent_path is not None:
        return normalized_path(space.parent_path)
    try:
        return normalized_path(client.genie.get_space(space.space_id).parent_path)
    except (NotFound, PermissionDenied) as exc:  # A space may be readable only by its owner.
        print(
            f"WARNING: could not read the folder of Genie space {space.space_id}: {exc}. "
            "Treating it as outside this deployment."
        )
        return None


def resolve_space(
    client: WorkspaceClient,
    spaces: dict[str, list[Any]],
    title: str,
    parent_path: str,
) -> Any | None:
    """Resolve one Genie space by title inside the demo folder.

    Matching on the title alone can select a space that another team owns and
    happens to have titled the same way. An update would then replace that
    team's configuration, so only a space in this deployment's folder is
    returned.
    """
    wanted = normalized_path(parent_path)
    in_folder = [
        space
        for space in spaces.get(title, [])
        if space_parent_path(client, space) == wanted
    ]
    if len(in_folder) > 1:
        raise ValueError(
            f"Found {len(in_folder)} Genie Agents titled {title!r} in {parent_path}. "
            "Delete the duplicates before deploying."
        )
    return in_folder[0] if in_folder else None


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
    parser.add_argument("--parent-path", required=True)
    args = parser.parse_args()

    manifest = load_manifest(Path(args.manifest))
    client = WorkspaceClient()

    ensure_tags(
        client,
        "dashboards",
        args.dashboard_id,
        manifest["dashboard"]["domain_tags"],
    )

    existing_spaces = spaces_by_title(client)
    for agent in manifest["agents"]:
        space = resolve_space(client, existing_spaces, agent["title"], args.parent_path)
        if space is None:
            raise ValueError(
                f"Genie Agent was not found in {args.parent_path}: {agent['title']}"
            )
        ensure_tags(
            client,
            "geniespaces",
            space.space_id,
            agent["domain_tags"],
        )


if __name__ == "__main__":
    main()
