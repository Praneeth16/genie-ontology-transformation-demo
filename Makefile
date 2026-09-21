PROFILE ?= DEFAULT
TARGET ?= dev
CATALOG ?= CHANGE_ME_CATALOG
SCHEMA ?= transformation_value_office
WAREHOUSE_ID ?= CHANGE_ME_WAREHOUSE_ID

BUNDLE_ENV = BUNDLE_VAR_catalog="$(CATALOG)" BUNDLE_VAR_schema="$(SCHEMA)" BUNDLE_VAR_warehouse_id="$(WAREHOUSE_ID)"

.PHONY: check check-config validate deploy setup benchmark

check:
	uv run ruff check src tests
	uv run python -m compileall -q src tests
	uv run python tests/check_metric_views.py
	find src/genie -maxdepth 1 -name '*.json' -print0 | xargs -0 -n1 jq empty
	jq empty src/dashboards/transformation_value_office.lvdash.json

check-config:
	@if [ "$(CATALOG)" = "CHANGE_ME_CATALOG" ] || [ "$(WAREHOUSE_ID)" = "CHANGE_ME_WAREHOUSE_ID" ]; then \
		echo "Set CATALOG and WAREHOUSE_ID before running a workspace command."; \
		exit 1; \
	fi

validate: check check-config
	$(BUNDLE_ENV) databricks bundle validate -t $(TARGET) --profile $(PROFILE)

deploy: validate
	$(BUNDLE_ENV) databricks bundle deploy -t $(TARGET) --profile $(PROFILE)
	$(BUNDLE_ENV) databricks bundle run setup_transformation_value_office -t $(TARGET) --profile $(PROFILE)

setup: check-config
	$(BUNDLE_ENV) databricks bundle run setup_transformation_value_office -t $(TARGET) --profile $(PROFILE)

benchmark: check-config
	$(BUNDLE_ENV) databricks bundle run regression_test_genie_agents -t $(TARGET) --profile $(PROFILE)
