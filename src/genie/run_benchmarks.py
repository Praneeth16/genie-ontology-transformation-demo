"""Run the committed benchmark questions for every deployed Genie Agent."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from databricks.sdk import WorkspaceClient
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
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    args = parser.parse_args()

    manifest = load_manifest(Path(args.manifest))
    client = WorkspaceClient()
    spaces = list_spaces(client)
    failures: list[str] = []

    for agent in manifest["agents"]:
        title = agent["title"]
        space = spaces.get(title)
        if space is None:
            failures.append(f"{title}: agent was not found")
            continue

        run = client.genie.genie_create_eval_run(space.space_id)
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
            elif run.num_correct != run.num_questions or (run.num_needs_review or 0) > 0:
                failures.append(
                    f"{title}: expected every benchmark to pass without manual review"
                )

    if failures:
        raise SystemExit("Benchmark regression failed:\n" + "\n".join(failures))
    print("All Genie Agent benchmark questions passed.")


if __name__ == "__main__":
    main()
