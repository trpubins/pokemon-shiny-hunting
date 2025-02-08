.PHONY: setup update clean \
		format lint test test-all

####### CONSTANTS #######
PROJ_ROOT_DIR := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
VENV_DIR := $(PROJ_ROOT_DIR)/.venv
PYTHON3 := python3

####### BUILD TARGETS #######

# The setup target creates a virtual env and installs packages as well as pre-commit hooks.
# It depends on the presence of two scripts: $(VENV_DIR)/bin/activate and $(VENV_DIR)/bin/pre-commit.
# If a script doesn't exist, it will trigger the targets below to create the
# virtual env, install packages, and/or install pre-commit hooks.
setup: $(VENV_DIR)/bin/activate

update: setup pip-install

$(VENV_DIR)/bin/activate:
	@$(MAKE) clean
	@echo "Setting up development environment using $(PYTHON3)..."
	$(PYTHON3) -m venv $(VENV_DIR)
	@$(MAKE) pip-install
	@echo "Development environment setup complete."

pip-install:
	@echo "Upgrading pip..."
	$(VENV_DIR)/bin/pip install --upgrade pip
	@echo "Installing required Python packages..."
	@find $(PROJ_ROOT_DIR) \
		-path '*/misc' -prune -o \
		-name 'requirements.txt' -print0 | \
		xargs -0 -I {} sh -c '$(VENV_DIR)/bin/pip install -r "$$1"' _ {}

# Clean target to remove the virtual environment
clean:
	@echo "Removing virtual environment..."
	rm -rf $(VENV_DIR)
	@echo "Clean complete."

# Format code using black, then lint using ruff
format:
	$(VENV_DIR)/bin/black $(PROJ_ROOT_DIR) && \
		$(VENV_DIR)/bin/ruff check $(PROJ_ROOT_DIR) --fix

lint:
	$(VENV_DIR)/bin/ruff check $(PROJ_ROOT_DIR)

# Run all tests
test:
	$(VENV_DIR)/bin/pytest -s -v -c $(PROJ_ROOT_DIR)/tests/pytest.ini -m "not emulator" \
		--cov --cov-report term --cov-report html --cov-report xml --cov-config $(PROJ_ROOT_DIR)/tests/.coveragerc

test-all:
	$(VENV_DIR)/bin/pytest -s -v -c $(PROJ_ROOT_DIR)/tests/pytest.ini \
		--cov --cov-report term --cov-report html --cov-report xml --cov-config $(PROJ_ROOT_DIR)/tests/.coveragerc