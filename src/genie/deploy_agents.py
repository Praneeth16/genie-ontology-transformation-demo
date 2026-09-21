"""Create or update the Genie Agents defined in the repository."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from databricks.sdk import WorkspaceClient


def replace_tokens(value: Any, replacements: dict[str, str]) -> Any:
    if isinstance(value, str):
        for token, replacement in replacements.items():
            value = value.replace(token, replacement)
        return value
    if isinstance(value, list):
        return [replace_tokens(item, replacements) for item in value]
    if isinstance(value, dict):
        return {key: replace_tokens(item, replacements) for key, item in value.items()}
    return value


def load_manifest(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        manifest = json.load(handle)
    agents = manifest.get("agents")
    if not isinstance(agents, list) or not agents:
        raise ValueError("Manifest must contain a non-empty agents list")
    return manifest


def normalize_definition(definition: dict[str, Any]) -> dict[str, Any]:
    data_sources = definition.get("data_sources", {})
    tables = data_sources.get("tables", [])
    for table in tables:
        column_configs = table.get("column_configs")
        if column_configs:
            column_configs.sort(key=lambda item: item["column_name"])
    tables.sort(key=lambda item: item["identifier"])
    return definition


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
    except Exception as exc:  # noqa: BLE001  # A space may be readable only by its owner.
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--warehouse-id", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--definition-dir", required=True)
    parser.add_argument("--parent-path", required=True)
    args = parser.parse_args()

    manifest = load_manifest(Path(args.manifest))
    definition_dir = Path(args.definition_dir)
    replacements = {
        "${catalog}": args.catalog,
        "${schema}": args.schema,
    }

    client = WorkspaceClient()
    client.workspace.mkdirs(args.parent_path)
    existing_spaces = spaces_by_title(client)

    for agent in manifest["agents"]:
        title = agent["title"]
        definition_path = definition_dir / agent["definition"]
        with definition_path.open(encoding="utf-8") as handle:
            definition = normalize_definition(
                replace_tokens(json.load(handle), replacements)
            )

        serialized = json.dumps(definition, separators=(",", ":"), ensure_ascii=False)
        existing = resolve_space(client, existing_spaces, title, args.parent_path)
        if existing:
            updated = client.genie.update_space(
                existing.space_id,
                title=title,
                description=agent["description"],
                warehouse_id=args.warehouse_id,
                parent_path=args.parent_path,
                serialized_space=serialized,
            )
            print(f"Updated Genie Agent: {title} ({updated.space_id})")
        else:
            created = client.genie.create_space(
                args.warehouse_id,
                serialized,
                title=title,
                description=agent["description"],
                parent_path=args.parent_path,
            )
            print(f"Created Genie Agent: {title} ({created.space_id})")


if __name__ == "__main__":
    main()
