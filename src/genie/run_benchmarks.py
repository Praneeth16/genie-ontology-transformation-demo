"""Run the committed benchmark questions for every deployed Genie Agent."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import DatabricksError, NotFound, PermissionDenied
from databricks.sdk.service.dashboards import EvaluationStatusType

TERMINAL_STATES = {
    EvaluationStatusType.DONE,
    EvaluationStatusType.EVALUATION_CANCELLED,
    EvaluationStatusType.EVALUATION_FAILED,
    EvaluationStatusType.EVALUATION_TIMEOUT,
}


def load_manifest(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--parent-path", required=True)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    args = parser.parse_args()

    manifest = load_manifest(Path(args.manifest))
    client = WorkspaceClient()
    existing_spaces = spaces_by_title(client)
    failures: list[str] = []

    for agent in manifest["agents"]:
        title = agent["title"]
        try:
            space = resolve_space(client, existing_spaces, title, args.parent_path)
        except ValueError as exc:
            # Record it and keep going. Every other failure mode reaches the
            # summary at the end, and an aborted loop would hide the agents that
            # were never benchmarked.
            failures.append(f"{title}: {exc}")
            continue
        if space is None:
            failures.append(f"{title}: agent was not found in {args.parent_path}")
            continue

        try:
            run = client.genie.genie_create_eval_run(space.space_id)
        except DatabricksError as exc:
            failures.append(
                f"{title}: could not start a benchmark run: {exc}. Check that this "
                "identity can manage the agent and that Genie benchmarks are enabled."
            )
            continue
        deadline = time.monotonic() + args.timeout_seconds
        while run.eval_run_status not in TERMINAL_STATES:
            if time.monotonic() >= deadline:
                failures.append(f"{title}: benchmark run timed out")
                break
            time.sleep(10)
            run = client.genie.genie_get_eval_run(space.space_id, run.eval_run_id)
        else:
            print(
                f"{title}: {run.num_correct}/{run.num_questions} correct, "
                f"{run.num_needs_review or 0} need review"
            )
            if run.eval_run_status != EvaluationStatusType.DONE:
                failures.append(f"{title}: run ended with {run.eval_run_status}")
            elif run.num_questions is None or run.num_correct is None:
                # Treat missing counts as a failure. Comparing None with None
                # would otherwise report a silent pass for a run that scored
                # nothing.
                failures.append(f"{title}: run reported no benchmark counts")
            elif run.num_correct != run.num_questions or (run.num_needs_review or 0) > 0:
                failures.append(
                    f"{title}: expected every benchmark to pass without manual review"
                )

    if failures:
        raise SystemExit("Benchmark regression failed:\n" + "\n".join(failures))
    print("All Genie Agent benchmark questions passed.")


if __name__ == "__main__":
    main()
