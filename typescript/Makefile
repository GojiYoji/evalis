# region: vars and stuff ------------------------------------------------------
include ../Makefile.common

ts_gen_dir=src/__gen__

# region: PHONY stuff ---------------------------------------------------------
.PHONY: build clean clean_gen lint setup teardown test \
	lint_tsc lint_eslint lint_prettier \
	npm_clean npm_install \
	get_version get_expression_version set_version \
	build_tsc

build: $(ts_gen_dir)/.antlr4.touch $(ts_gen_dir)/grammar.ts build_tsc

clean: clean_gen
	@rm -rf ./node_modules/ ./dist/

clean_gen:
	@rm -rf $(ts_gen_dir)

lint: lint_tsc lint_eslint lint_prettier

setup: npm_install

teardown: npm_clean

test:
	npm test

get_version:
	@npm pkg get version | tr -d '"'

get_expression_version:
	@grep 'EXPRESSION_VERSION' src/constants.ts | cut -d"'" -f2

set_version:
	@echo "Setting TypeScript package version to $${VERSION}"
	@npm version $${VERSION} --no-git-tag-version --allow-same-version

prepack: build LICENSE

# region: typescript specific build -------------------------------------------
build_tsc: $(ts_gen_dir)/grammar.ts
	@npm run build:tsc

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

LICENSE: ../LICENSE
	@cp ../LICENSE LICENSE
