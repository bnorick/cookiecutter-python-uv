PACKAGE := {{ cookiecutter.package_name }}
PACKAGE_DIR := src/${PACKAGE}
MODULES := $(wildcard $(PACKAGE_DIR)/*.py)

# For additional vebosity, execute these in your shell before make
# export RUST_LOG=trace

export UV_PREVIEW=1

# MAIN TASKS ##################################################################

.PHONY: all
all: doctor format check test ## Run all tasks that determine CI status

.PHONY: dev
dev: install  ## Continuously run all CI tasks when files chanage
	uv run ptw

.PHONY: ipython
ipython: install
	uv run ipython --ipython-dir=notebooks --profile-dir=notebooks/.ipython_profile

.PHONY: demo
demo: install
	uv run nbstripout notebooks/demos/*.ipynb 2>/dev/null || true
	uv run jupyter notebook --ServerApp.root_dir=notebooks --ServerApp.preferred_dir=notebooks/demos --allow-root --ip 0.0.0.0 --port 8888

.PHONY: notebook
notebook: install
	uv run jupyter notebook --ServerApp.root_dir=notebooks --allow-root --ip 0.0.0.0 --port 8888

# SYSTEM DEPENDENCIES #########################################################

.PHONY: doctor
doctor: ## Confirm system dependencies are available
	bin/verchew

# PROJECT DEPENDENCIES ########################################################

VIRTUAL_ENV ?= .venv
DEPENDENCIES := $(VIRTUAL_ENV)/.deps-$(shell bin/checksum pyproject.toml requirements.lock requirements-dev.lock)

.PHONY: install
install: $(DEPENDENCIES) .cache ## Install project dependencies

$(DEPENDENCIES): uv.lock
	@ rm -rf $(VIRTUAL_ENV)/.deps-*
	uv sync --extra test
	@ touch $@

uv.lock: pyproject.toml
	uv lock
	@ touch $@

.cache:
	@ mkdir -p .cache

# CHECKS ######################################################################

.PHONY: format
format: install
	@ echo
	@ echo '#### RUFF'
	uv run ruff check ${PACKAGE_DIR} tests
	@ echo
	@ echo '#### BLACK'
	uv run black $(PACKAGE_DIR) tests
	@ echo

.PHONY: check
check: install  ## Run formaters, linters, and static analysis
	@ echo
	@ echo '#### MYPY'
	uv run mypy ${PACKAGE_DIR}
	@ echo
	@ echo '#### DEPTRY'
	uv run deptry --config pyproject.toml ${PACKAGE_DIR} tests
	@ echo
	@ echo '#### RUFF'
	uv run ruff check --output-format=full --no-fix
	@ echo
	@ echo '#### BLACK'
	uv run black $(PACKAGE_DIR) tests --diff

# TESTS #######################################################################

.PHONY: test
test: install  ## Run unit and integration tests
	uv run pytest --random --doctest-modules

.PHONY: test-repeat
test-repeat: install
	uv run pytest --count=5 --random --doctest-modules --exitfirst

# RELEASE #####################################################################

# DIST_FILES := dist/*.tar.gz dist/*.whl

# .PHONY: dist
# dist: install $(DIST_FILES)
# $(DIST_FILES): $(MODULES) pyproject.toml
# 	rm -f $(DIST_FILES)
# 	poetry build

# .PHONY: upload
# upload: dist  ## Upload the current version to PyPI
# 	git diff --name-only --exit-code
# 	poetry publish
# 	bin/open https://pypi.org/project/$(PACKAGE)

# CLEANUP #####################################################################

.PHONY: clean
clean:  ## Delete all generated and temporary files
	rm -rf .venv

# HELP ########################################################################

.PHONY: help
help: install
	@ grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help