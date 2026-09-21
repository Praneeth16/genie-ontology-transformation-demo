"""Check the generated metric view definitions without a Databricks workspace.

The build script writes metric view YAML inside SQL. A typo there only surfaces
when the setup job runs, which is a slow and expensive place to find it. This
check stubs out Spark, captures every statement the build script would send, and
asserts the contract that the metric views rely on.
"""

from __future__ import annotations

import contextlib
import io
import re
import sys
import types
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
EXPECTED_METRIC_VIEWS = {
    "mv_value_realization",
    "mv_delivery_health",
    "mv_value_trend",
    "mv_operating_performance",
}


def captured_statements() -> list[str]:
    statements: list[str] = []

    class FakeFrame:
        def count(self) -> int:
            return 0

        def first(self) -> None:
            return None

    class FakeSession:
        def sql(self, statement: str) -> FakeFrame:
            statements.append(statement)
            return FakeFrame()

    class FakeBuilder:
        def getOrCreate(self) -> FakeSession:
            return FakeSession()

    class FakeSparkSession:
        builder = FakeBuilder()

    pyspark = types.ModuleType("pyspark")
    pyspark_sql = types.ModuleType("pyspark.sql")
    pyspark_sql.SparkSession = FakeSparkSession
    sys.modules["pyspark"] = pyspark
    sys.modules["pyspark.sql"] = pyspark_sql
    sys.path.insert(0, str(REPO_ROOT / "src" / "data"))

    import build_demo

    sys.argv = ["build_demo", "--catalog=demo", "--schema=tvo", "--as-of-date=2026-08-31"]
    with contextlib.redirect_stdout(io.StringIO()):
        build_demo.main()
    return statements


def main() -> None:
    statements = captured_statements()
    definitions = [statement for statement in statements if "WITH METRICS" in statement]
    failures: list[str] = []
    seen: set[str] = set()

    for statement in definitions:
        name = re.search(r"CREATE OR REPLACE VIEW (\S+)", statement).group(1)
        short_name = name.split(".")[-1]
        seen.add(short_name)
        body = statement.split("AS $$\n", 1)[1].rsplit("\n$$", 1)[0]

        try:
            document = yaml.safe_load(body)
        except yaml.YAMLError as exc:
            failures.append(f"{short_name}: YAML does not parse: {exc}")
            continue

        if document.get("version") != 1.1:
            failures.append(f"{short_name}: expected version 1.1, got {document.get('version')!r}")
        if "dimensions" in document:
            failures.append(f"{short_name}: use the fields keyword rather than dimensions")

        entries = document.get("fields", []) + document.get("measures", [])
        if not document.get("measures"):
            failures.append(f"{short_name}: defines no measures")
        for entry in entries:
            if not entry.get("comment"):
                failures.append(f"{short_name}: {entry['name']} has no comment")
            if not entry.get("display_name"):
                failures.append(f"{short_name}: {entry['name']} has no display_name")

        declared = {join["name"] for join in document.get("joins", [])}
        for join in document.get("joins", []):
            if not join.get("on") and not join.get("using"):
                failures.append(f"{short_name}: join {join['name']} has neither on nor using")
        referenced: set[str] = set()
        for entry in entries:
            referenced |= set(re.findall(r"\b([a-z][a-z0-9_]*)\.", entry["expr"]))
        referenced -= {"demo"}
        for unknown in sorted(referenced - declared):
            failures.append(f"{short_name}: expression refers to undeclared join {unknown!r}")
        for unused in sorted(declared - referenced):
            failures.append(f"{short_name}: declares join {unused!r} that nothing references")

        # Name resolution is case insensitive, so a join alias that matches a
        # field or measure name is read as that field instead of the join.
        entry_names_lower = {entry["name"].lower() for entry in entries}
        for alias in sorted(declared):
            if alias.lower() in entry_names_lower:
                failures.append(
                    f"{short_name}: join alias {alias!r} collides with a field or measure "
                    "of the same name. Rename the join."
                )

        field_names = {field["name"] for field in document.get("fields", [])}
        for measure in document.get("measures", []):
            for window in measure.get("window", []):
                order = window.get("order")
                if not order:
                    failures.append(f"{short_name}: {measure['name']} window has no order field")
                elif order not in field_names:
                    # The engine rejects a source column here. It requires the
                    # name of a field declared in this metric view.
                    failures.append(
                        f"{short_name}: {measure['name']} window order {order!r} is not a "
                        f"declared field. Use one of: {', '.join(sorted(field_names))}"
                    )
                if not window.get("range"):
                    failures.append(f"{short_name}: {measure['name']} window has no range")
                if window.get("semiadditive") not in {"first", "last"}:
                    failures.append(
                        f"{short_name}: {measure['name']} window semiadditive must be first or last"
                    )

        print(f"PASS {short_name}: {len(document.get('fields', []))} fields, "
              f"{len(document.get('measures', []))} measures, "
              f"{len(declared)} joins")

    missing = EXPECTED_METRIC_VIEWS - seen
    if missing:
        failures.append(f"build script no longer creates: {', '.join(sorted(missing))}")

    if failures:
        raise SystemExit("Metric view checks failed:\n" + "\n".join(f"  {f}" for f in failures))
    print(f"All {len(definitions)} metric view definitions are valid.")


if __name__ == "__main__":
    main()
