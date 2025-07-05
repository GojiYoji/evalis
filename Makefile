# region: vars and stuff ------------------------------------------------------
include ./Makefile.common

# region: PHONY stuff ---------------------------------------------------------
.PHONY: \
	build build_python \
	clean clean_python \
	lint lint_python \
	setup setup_python \
	teardown teardown_python \
	test test_python

build: build_python

build_python:
	$(MAKE) -C python lint

clean: clean_python

clean_python:
	$(MAKE) -C python clean

lint: lint_python

lint_python:
	$(MAKE) -C python lint

setup: setup_python

setup_python:
	$(MAKE) -C python setup

teardown: teardown_python

teardown_python:
	$(MAKE) -C python teardown

test: test_python

test_python:
	$(MAKE) -C python test

