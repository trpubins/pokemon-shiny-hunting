.PHONY: setup update clean \
		format lint test test-all

####### CONSTANTS #######
PROJ_ROOT_DIR := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
VENV_DIR := $(PROJ_ROOT_DIR)/.venv
PYTHON3 := python3

# OS-specific path handling
ifeq ($(OS),Windows_NT)
    VENV_EXE_DIR := $(VENV_DIR)/Scripts
else
    VENV_EXE_DIR := $(VENV_DIR)/bin
endif

####### BUILD TARGETS #######

# The setup target creates a virtual env and installs packages as well as pre-commit hooks.
# It depends on the presence of one script: $(VENV_EXE_DIR)/activate.
# If the script doesn't exist, it will trigger the targets below to create the
# virtual env and/or install packages.
setup: $(VENV_EXE_DIR)/activate

update: setup pip-install

$(VENV_EXE_DIR)/activate:
	@$(MAKE) clean
	@echo "Setting up development environment using $(PYTHON3)..."
	$(PYTHON3) -m venv $(VENV_DIR)
	@$(MAKE) pip-install
	@echo "Development environment setup complete."

pip-install:
	@echo "Upgrading pip..."
	$(VENV_EXE_DIR)/pip install --upgrade pip
	@echo "Installing required Python packages..."
	@find $(PROJ_ROOT_DIR) \
		-path '*/misc' -prune -o \
		-name 'requirements.txt' -print0 | \
		xargs -0 -I {} sh -c '$(VENV_EXE_DIR)/pip install -r "$$1"' _ {}

# Clean target to remove the virtual environment
clean:
	@echo "Removing virtual environment..."
	rm -rf $(VENV_DIR)
	@echo "Clean complete."

# Format code using black, then lint using ruff
format:
	$(VENV_EXE_DIR)/black $(PROJ_ROOT_DIR) && \
		$(VENV_EXE_DIR)/ruff check $(PROJ_ROOT_DIR) --fix

lint:
	$(VENV_EXE_DIR)/ruff check $(PROJ_ROOT_DIR)

# Run all tests
test:
	$(VENV_EXE_DIR)/pytest -s -v -c $(PROJ_ROOT_DIR)/tests/pytest.ini -m "not emulator" \
		--cov --cov-report term --cov-report html --cov-report xml --cov-config $(PROJ_ROOT_DIR)/tests/.coveragerc

test-all:
	$(VENV_EXE_DIR)/pytest -s -v -c $(PROJ_ROOT_DIR)/tests/pytest.ini \
		--cov --cov-report term --cov-report html --cov-report xml --cov-config $(PROJ_ROOT_DIR)/tests/.coveragerc