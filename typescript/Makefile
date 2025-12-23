# region: vars and stuff ------------------------------------------------------
include ../Makefile.common

ts_gen_dir=src/__gen__
VERSION := $(shell grep '"version":' package.json | head -1 | cut -d'"' -f4)
EXPRESSION_VERSION := $(shell grep 'EXPRESSION_VERSION' src/constants.ts | cut -d"'" -f2)

# region: PHONY stuff ---------------------------------------------------------
.PHONY: build clean clean_gen lint setup teardown test \
	lint_tsc lint_eslint lint_prettier \
	npm_clean npm_install \
	check_version

build: $(ts_gen_dir)/.antlr4.touch $(ts_gen_dir)/grammar.ts
	npm run build

clean: clean_gen
	@rm -rf ./node_modules/ ./dist/

clean_gen:
	@rm -rf $(ts_gen_dir)

lint: lint_tsc lint_eslint lint_prettier

setup: npm_install

teardown: npm_clean

test:
	npm test

check_version:
	@echo "[check_version] --------------------"
	@$(ROOT_DIR)/support/check_readme_version_reference.sh JavaScript/TypeScript $(VERSION)
	@echo "[check_version:OK] -----------------"
	@echo "[check_expression_version] ---------"
	@$(ROOT_DIR)/support/check_expression_version_reference.sh $(EXPRESSION_VERSION)
	@echo "[check_expression_version:OK] ------"

# region: typescript specific linters -----------------------------------------
lint_tsc:
	@echo "[tsc] ----------------------"
	@npx tsc --noEmit
	@echo "[tsc:OK] -------------------"

lint_eslint:
	@echo "[eslint] -------------------"
	@npm run lint
	@echo "[eslint:OK] ----------------"

lint_prettier:
	@echo "[prettier] -----------------"
	@npm run format:check
	@echo "[prettier:OK] --------------"

# region: npm stuff -----------------------------------------------------------
npm_clean:
	rm -rf node_modules package-lock.json

npm_install:
	npm install

# region: real stuff ----------------------------------------------------------
$(ts_gen_dir)/grammar.ts: $(GRAMMAR_FILE) generate.py
	python ../support/generate_source.py generate.py $(ts_gen_dir)/grammar.ts

$(ts_gen_dir)/.antlr4.touch: $(GRAMMAR_FILE)
	@rm -rf $(ts_gen_dir)
	@mkdir -p $(ts_gen_dir)
	antlr4 -Dlanguage=TypeScript -visitor $(GRAMMAR_FILE) -o $(ts_gen_dir)
	@touch $(ts_gen_dir)/.antlr4.touch
