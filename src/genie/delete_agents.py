"""Delete the demo Genie Agents, which the bundle does not track."""

from __future__ import annotations

import argparse
from pathlib import Path

from databricks.sdk import WorkspaceClient
from deploy_agents import load_manifest, resolve_space, spaces_by_title


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument(
        "--parent-path",
        help="Folder that holds the agents. Defaults to the bundle default for this user.",
    )
    args = parser.parse_args()

    client = WorkspaceClient()
    parent_path = args.parent_path or (
        f"/Workspace/Users/{client.current_user.me().user_name}"
        "/genie-ontology-transformation-demo"
    )
    manifest = load_manifest(Path(args.manifest))
    existing_spaces = spaces_by_title(client)

    for agent in manifest["agents"]:
        space = resolve_space(client, existing_spaces, agent["title"], parent_path)
        if space is None:
            print(f"Not found in {parent_path}: {agent['title']}")
            continue
        client.genie.trash_space(space.space_id)
        print(f"Deleted Genie Agent: {agent['title']} ({space.space_id})")


if __name__ == "__main__":
    main()
