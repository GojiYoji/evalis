# region: vars and stuff ------------------------------------------------------
include ../Makefile.common

ifdef CI
pip_install_target := pip_install_ci
else
pip_install_target := pip_install
endif

requirements_file=requirements.lock.txt
python_gen_dir=src/evalis/__gen__

# region: PHONY stuff ---------------------------------------------------------
.PHONY: build clean lint setup teardown test \
	lint_pyright \
	pip_clean pip_install pip_install_ci pip_lock \
	get_version get_expression_version set_version \
	pack

build: $(python_gen_dir)/.antlr4.touch $(python_gen_dir)/grammar.py

clean:
	@rm -rf $(python_gen_dir) ./__pycache__/ ./.pytest_cache/ ./dist/

lint: lint_pyright lint_black lint_flake8

setup: $(pip_install_target)

teardown: pip_clean

test:
	pytest $(ARGS)

get_version:
	@support/get_version.sh

get_expression_version:
	@support/get_expression_version.sh

set_version:
	@echo "Setting python package version to $${VERSION}"
	@support/set_version.py $$VERSION

prepack: build LICENSE

# region: packaging -----------------------------------------------------------
pack: prepack
	@rm -rf ./dist/
	python -m build --sdist
	@echo "Tarball created:"
	@ls -1 ./dist/*.tar.gz

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
$(python_gen_dir)/grammar.py: $(GRAMMAR_FILE) support/generate.py
	python ../support/generate_source.py support/generate.py $(python_gen_dir)/grammar.py

$(python_gen_dir)/.antlr4.touch: $(GRAMMAR_FILE) $(requirements_file)
	@rm -rf $(python_gen_dir)
	@mkdir -p $(python_gen_dir)
	antlr4 -Dlanguage=Python3 -visitor $(GRAMMAR_FILE) -o $(python_gen_dir)
	@touch $(python_gen_dir)/.antlr4.touch

LICENSE: ../LICENSE
	@cp ../LICENSE LICENSE
