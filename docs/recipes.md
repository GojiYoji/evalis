<!-- vim: set noexpandtab tabstop=4 shiftwidth=4: -->

# Recipes

This document contains step-by-step guides for common tasks when working with Evalis.

## Adding a New Language Implementation

Follow these steps to add support for a new programming language:

### 1. Create Directory Structure

```bash
mkdir -p <language>/src/__gen__
mkdir -p <language>/tests
mkdir -p <language>/support # Optional: this houses language-specific scripts and helpers
```

Replace `<language>` with your target language name (e.g., `go`, `rust`, `java`).

### 2. Create the Makefile

Copy the template Makefile below and customize it for your language:

```makefile
# region: vars and stuff ------------------------------------------------------
# Include common variables shared across all implementations
include ../Makefile.common

# Define the directory where ANTLR will generate code
gen_dir=src/__gen__

# region: PHONY stuff ---------------------------------------------------------
# Declare phony targets (targets that don't represent files)
.PHONY: build clean lint setup teardown test \
	get_version get_expression_version set_version

# build: Compile/build the project
# This target should:
# - Generate ANTLR parser/lexer from grammar
# - Generate language-specific grammar enums
# - Compile/build the source code
build: $(gen_dir)/.antlr4.touch $(gen_dir)/grammar.<ext>
	# Add your build command here
	# Examples:
	#   Go:         go build ./...
	#   Rust:       cargo build
	#   Java:       mvn compile
	#   C#:         dotnet build

# clean: Remove all generated files and build artifacts
clean:
	@rm -rf $(gen_dir) ./build/ ./dist/ ./target/
	# Add language-specific clean commands if needed

# lint: Run all linters and code quality checks
lint:
	# Add your linting commands here
	# Examples:
	#   Go:         golangci-lint run
	#   Rust:       cargo clippy
	#   Java:       mvn checkstyle:check
	#   C#:         dotnet format --verify-no-changes

# setup: Install dependencies and prepare development environment
setup:
	# Add dependency installation commands here
	# Examples:
	#   Go:         go mod download
	#   Rust:       cargo fetch
	#   Java:       mvn install
	#   C#:         dotnet restore

# teardown: Clean up development environment (opposite of setup)
teardown:
	# Add cleanup commands here if needed
	# Usually involves removing dependencies or caches

# test: Run all tests using the shared test oracle
test:
	# Add your test command here
	# Make sure to load and run test-oracle/cases.yml
	# Examples:
	#   Go:         go test ./...
	#   Rust:       cargo test
	#   Java:       mvn test
	#   C#:         dotnet test

# get_version: Print the package version
get_version:
	@# Extract version from package metadata
	# Examples:
	#   Python:     grep '^__version__' src/<language>/constants.py | cut -d'"' -f2
	#   TypeScript: npm pkg get version | tr -d '"'

# get_expression_version: Print the EXPRESSION_VERSION this implementation supports
get_expression_version:
	@# Extract EXPRESSION_VERSION from constants file
	# Examples:
	#   Python:     grep '^EXPRESSION_VERSION' src/<language>/constants.py | cut -d'"' -f2
	#   TypeScript: grep 'EXPRESSION_VERSION' src/constants.ts | cut -d"'" -f2

# set_version: Set the package version (expects VERSION environment variable)
set_version:
	@echo "Setting <language> package version to $${VERSION}"
	@# Update version in package metadata
	# Examples:
	#   Python:     python support/set_version.py $$VERSION
	#   TypeScript: npm version $$VERSION --no-git-tag-version --allow-same-version

# region: code generation -----------------------------------------------------
# Generate language-specific grammar enums (operators, keywords, etc.)
# This uses the generate.py script specific to your language
$(gen_dir)/grammar.<ext>: $(GRAMMAR_FILE) generate.py
	python ../support/generate_source.py support/generate.py $(gen_dir)/grammar.<ext>

# Generate ANTLR parser and lexer for your target language
# The .antlr4.touch file is used as a timestamp to avoid regenerating unnecessarily
$(gen_dir)/.antlr4.touch: $(GRAMMAR_FILE)
	@rm -rf $(gen_dir)
	@mkdir -p $(gen_dir)
	antlr4 -Dlanguage=<Language> -visitor $(GRAMMAR_FILE) -o $(gen_dir)
	@touch $(gen_dir)/.antlr4.touch
```

**Customization Notes:**

- Replace `<language>` with your language name (lowercase)
- Replace `<Language>` with the ANTLR language target (e.g., `Go`, `CSharp`, `Java`)
- Replace `<ext>` with your language's file extension (e.g., `go`, `rs`, `java`, `cs`)
- Customize the `VERSION` and `EXPRESSION_VERSION` extraction commands for your language
  - See `python/Makefile` and `typescript/Makefile` for reference implementations
- Implement the `get_version`, `get_expression_version`, and `set_version` targets
  - `get_version`: Extract package version
  - `get_expression_version`: Extract EXPRESSION_VERSION constant
  - `set_version`: Update package version (expects `VERSION` environment variable)
- Fill in the build, lint, setup, and test commands for your language

### 3. Create Generate Script

Create `<language>/generate.py` to output language-specific code from the grammar.

See `python/generate.py` for a reference implementation.

Example structure:

```python
from typing import Protocol


class LineWriter(Protocol):
    def write(self, line: str): ...


def generate(
    writer: LineWriter,
    reserved_keywords: list[str],
    binary_ops: list[tuple[str, str]],
    unary_ops: list[tuple[str, str]],
):
    # Write code in your target language
    # Generate enums/constants for:
    # - RESERVED_KEYWORDS
    # - BinaryOpType
    # - UnaryOpType
```

### 4. Implement Core Components

Create the following files in `<language>/src/`:

#### a. **types** - AST Node Type Definitions

Define types/classes/structs for:

- `ReferenceNode` - Property/variable access
- `UnaryOpNode` - Single-operand operations
- `BinaryOpNode` - Two-operand operations
- `LiteralNode` - Constants
- `ListComprehensionNode` - List comprehensions
- `EvalisNode` - Union/sum type of all nodes
- `EvaluatorOptions` - Configuration options
- `SyntaxMessage` - Parse error information

See `python/src/evalis/types.py` for reference.

#### b. **ast** - AST Builder (ANTLR Visitor)

Implement a visitor that converts ANTLR parse tree to AST:

- Extend the generated ANTLR visitor
- Implement `visit*` methods for each grammar rule
- Return appropriate AST nodes

See `python/src/evalis/ast.py` for reference.

#### c. **eval** - Expression Evaluator

Implement recursive evaluation of AST nodes:

- Handle all operator types
- Support property/array access
- Implement list comprehensions
- Respect `EvaluatorOptions`

See `python/src/evalis/eval.py` for reference.

#### d. **evalis** - Public API

Implement three main functions:

- `parseAst(expression)` - Parse string to AST
- `evaluateAst(node, context, options)` - Evaluate AST
- `evaluateExpression(expression, context, options)` - One-shot evaluation

See `python/src/evalis/evalis.py` for reference.

### 5. Implement Test Runner

Create `<language>/tests/` with a test runner that:

1. Loads `../test-oracle/cases.yml`
2. Parses the YAML test cases
3. Runs each test case through `evaluateExpression()`
4. Asserts the result matches the expected value

Example test case structure:

```yaml
- expr: "foo.bar + 5"
  context:
    foo:
      bar: 12
  expected: 17
```

See `python/tests/test_cases.py` for reference.

### 6. Register with Build System

Run the auto-discovery script to add your implementation to the root Makefile:

```bash
python support/generate_makefile.py
```

This will automatically detect your new `<language>/Makefile` and add targets like:

- `make <language>_build`
- `make <language>_test`
- `make <language>_lint`
- `make <language>_get_version`
- `make <language>_check_version`

### 7. Verify Implementation

```bash
# Test your implementation
make <language>_test

# Run linters
make <language>_lint

# Build
make <language>_build

# Check version configuration
make <language>_check_version

# Test everything together
make test
```

### 8. Document Your Implementation

Create `<language>/README.md` with:

- Installation instructions
- Usage examples
- API reference
- Development setup

## Need Help?

- Check the Python reference implementation: `python/`
- Read the [Architecture](./architecture.md) document
- Open an issue for questions or guidance
