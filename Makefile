# region: vars and stuff ------------------------------------------------------
grammar_file=grammar/Fablex.g4
requirements_file=python/requirements.lock.txt

python_gen_dir=python/src/fablex/__gen__/

# region: PHONY stuff ---------------------------------------------------------
.PHONY: \
	build build_python \
	clean clean_python_gen \
	pip_clean pip_install pip_install_ci pip_lock

build: build_python

build_python: $(python_gen_dir)

clean: clean_python_gen

clean_python_gen:
	@rm -rf $(python_gen_dir)

pip_clean:
	mise uninstall python
	rm -rf .venv
	mise install

pip_install_ci:
	python -m pip install --upgrade pip
	cd python && pip install --no-deps -e .
	cd python && pip install -r requirements.lock.txt
	cd python && pip check

pip_install:
	cd python && pip install -r requirements.lock.txt
	cd python && pip install -e .[dev]
	cd python && pip check

pip_lock:
	cd python && pip install -e .[dev]
	cd python && pip freeze --exclude-editable > requirements.lock.txt

# region: real stuff ----------------------------------------------------------
$(python_gen_dir): $(grammar_file) $(requirements_file)
	@rm -rf $(python_gen_dir)
	@mkdir -p $(python_gen_dir)
	antlr4 -Dlanguage=Python3 -visitor $(grammar_file) -o $(python_gen_dir)
	@touch $(python_gen_dir)
