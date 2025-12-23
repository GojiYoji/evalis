# region: vars and stuff ------------------------------------------------------
include ../Makefile.common

ifdef CI
pip_install_target := pip_install_ci
else
pip_install_target := pip_install
endif

requirements_file=requirements.lock.txt
python_gen_dir=src/evalis/__gen__

VERSION := $(shell grep '^__version__' src/evalis/constants.py | cut -d'"' -f2)
EXPRESSION_VERSION := $(shell grep '^EXPRESSION_VERSION' src/evalis/constants.py | cut -d'"' -f2)

# region: PHONY stuff ---------------------------------------------------------
.PHONY: build clean lint setup teardown test \
	lint_pyright \
	pip_clean pip_install pip_install_ci pip_lock \
	check_version

build: $(python_gen_dir)/.antlr4.touch $(python_gen_dir)/grammar.py

clean:
	@rm -rf $(python_gen_dir) ./__pycache__/ ./.pytest_cache/

lint: lint_pyright lint_black lint_flake8

setup: $(pip_install_target)

teardown: pip_clean

test:
	pytest

check_version:
	@echo "[check_version] --------------------"
	@$(ROOT_DIR)/support/check_readme_version_reference.sh Python $(VERSION)
	@echo "[check_version:OK] -----------------"
	@echo "[check_expression_version] ---------"
	@$(ROOT_DIR)/support/check_expression_version_reference.sh $(EXPRESSION_VERSION)
	@echo "[check_expression_version:OK] ------"

# region: python specific linters ---------------------------------------------
lint_pyright:
	@echo "[pyright] ------------------"
	@pyright
	@echo "[pyright:OK] ---------------"

lint_black:
	@echo "[black] --------------------"
	@black --check src/ tests/
	@echo "[black:OK] -----------------"

lint_flake8:
	@echo "[flake8] -------------------"
	@flake8 src/ tests/
	@echo "[flake8:OK] ----------------"

# region: python pip stuff ----------------------------------------------------
pip_clean:
	mise uninstall python
	rm -rf ../.venv
	mise install

pip_install_ci:
	python -m pip install --upgrade pip
	pip install --no-deps -e .
	pip install --require-hashes -r requirements.lock.txt
	pip check

pip_install:
	pip install --require-hashes -r requirements.lock.txt
	pip install -e .[dev]
	pip check

pip_lock:
	pip install pip-tools
	pip-compile --generate-hashes --extra dev -o requirements.lock.txt pyproject.toml

# region: real stuff ----------------------------------------------------------
$(python_gen_dir)/grammar.py: $(GRAMMAR_FILE) generate.py
	python ../support/generate_source.py generate.py $(python_gen_dir)/grammar.py

$(python_gen_dir)/.antlr4.touch: $(GRAMMAR_FILE) $(requirements_file)
	@rm -rf $(python_gen_dir)
	@mkdir -p $(python_gen_dir)
	antlr4 -Dlanguage=Python3 -visitor $(GRAMMAR_FILE) -o $(python_gen_dir)
	@touch $(python_gen_dir)/.antlr4.touch
