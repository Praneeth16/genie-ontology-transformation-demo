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
    existing_by_title = list_spaces(client)

    for agent in manifest["agents"]:
        title = agent["title"]
        definition_path = definition_dir / agent["definition"]
        with definition_path.open(encoding="utf-8") as handle:
            definition = normalize_definition(
                replace_tokens(json.load(handle), replacements)
            )

        serialized = json.dumps(definition, separators=(",", ":"), ensure_ascii=False)
        existing = existing_by_title.get(title)
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
