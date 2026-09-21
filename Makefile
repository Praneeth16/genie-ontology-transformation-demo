PROFILE ?= fe-vm-lakebase-praneeth
TARGET ?= praneeth

.PHONY: check validate deploy setup benchmark

check:
	uv run ruff check src
	uv run python -m compileall -q src
	find src/genie -maxdepth 1 -name '*.json' -print0 | xargs -0 -n1 jq empty
	jq empty src/dashboards/transformation_value_office.lvdash.json

validate: check
	databricks bundle validate -t $(TARGET) --profile $(PROFILE)

deploy: validate
	databricks bundle deploy -t $(TARGET) --profile $(PROFILE)
	databricks bundle run setup_transformation_value_office -t $(TARGET) --profile $(PROFILE)

setup:
	databricks bundle run setup_transformation_value_office -t $(TARGET) --profile $(PROFILE)

benchmark:
	databricks bundle run regression_test_genie_agents -t $(TARGET) --profile $(PROFILE)
