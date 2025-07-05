# region: vars and stuff ------------------------------------------------------
include ../Makefile.common

requirements_file=requirements.lock.txt
python_gen_dir=src/fablex/__gen__/

# region: PHONY stuff ---------------------------------------------------------
.PHONY: build clean lint setup teardown test \
	lint_pyright \
	pip_clean pip_install pip_lock \

build: $(python_gen_dir)

clean:
	@rm -rf $(python_gen_dir)

lint: lint_pyright lint_black lint_flake8

setup: pip_install

teardown: pip_clean

test:
	pytest

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

pip_install:
	pip install -r requirements.lock.txt
	# note: We need to run this from top directory so that we are next to `.venv`
	pip install -e .[dev]
	pip check

pip_lock:
	# note: We need to run this from top directory so that we are next to `.venv`
	pip install -e .[dev]
	pip freeze --exclude-editable > requirements.lock.txt

# region: real stuff ----------------------------------------------------------
$(python_gen_dir): $(GRAMMAR_FILE) $(requirements_file)
	@rm -rf $(python_gen_dir)
	@mkdir -p $(python_gen_dir)
	antlr4 -Dlanguage=Python3 -visitor $(GRAMMAR_FILE) -o $(python_gen_dir)
	@touch $(python_gen_dir)
