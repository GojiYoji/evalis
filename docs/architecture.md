# Architecture

Evalis is designed as a **polyglot expression evaluator** with a focus on
consistency, security, and maintainability across multiple programming
languages.

## Core Principles

### 1. Single Source of Truth

**Grammar Definition** (`grammar/Evalis.g4`)

- ANTLR4 grammar defines the expression language syntax
- Shared across all language implementations
- Changes to the grammar automatically propagate to all implementations

**Test Oracle** (`test-oracle/cases.yml`)

- Single YAML file containing all test cases
- Each implementation runs the same tests
- Ensures behavioral consistency across languages
- Easy to add new test cases that benefit all implementations

### 2. Language-Specific Implementations

Each language implementation follows the same architecture:

```
language/
├── src/
│   ├── __gen__/          # ANTLR-generated parser/lexer
│   ├── types.*           # AST node type definitions
│   ├── ast.*             # AST builder (ANTLR visitor)
│   ├── eval.*            # Expression evaluator
│   └── evalis.*          # Public API
├── tests/                # Test runner for shared test cases
├── generate.py           # Code generator for grammar enums
└── Makefile              # Build automation
```

## Data Flow

```
Expression String
    ↓
[ANTLR Lexer] → Tokens
    ↓
[ANTLR Parser] → Parse Tree
    ↓
[AST Builder Visitor] → Abstract Syntax Tree
    ↓
[Evaluator] → Result
```

## AST Node Types

All implementations support these node types:

- **LiteralNode** - Constants (numbers, strings, booleans, null)
- **ReferenceNode** - Variable and property access (`foo.bar`, `items[0]`)
- **BinaryOpNode** - Two-operand operations (`+`, `-`, `*`, `/`, `<`, `>`, `==`, `and`, `or`, `in`)
- **UnaryOpNode** - Single-operand operations (`not`)
- **ListComprehensionNode** - List transformations (`[x * 2 for x in numbers]`)

## Expression Features

### Operators

- **Arithmetic**: `+`, `-`, `*`, `/`
- **Comparison**: `<`, `<=`, `>`, `>=`, `==`, `!=`
- **Logical**: `and`, `or`, `not`
- **Membership**: `in`

### Data Access

- **Property access**: `foo.bar.baz`
- **Array indexing**: `items[0]`
- **Dynamic access**: `data[key]`

### List Comprehensions

- **Mapping**: `[x * 2 for x in numbers]`
- **Nested properties**: `[user.name for user in users]`
- **Context variables**: `[x + offset for x in values]`

## Security Model

Evalis provides **sandboxed expression evaluation**:

1. **No arbitrary code execution** - Unlike `eval()` in most languages
2. **Formal grammar validation** - All input is validated before evaluation
3. **Controlled operations** - Only allowed operators and functions
4. **Safe property access** - Optional null-coalescing with `shouldNullOnBadAccess`

## Build System

- **Root Makefile** - Orchestrates all language implementations
- **Language Makefiles** - Language-specific build, test, lint
- **Auto-discovery** - `generate_makefile.py` finds all implementations
- **Consistent targets** - All implementations support the same Make targets

## Versioning

Evalis uses a multi-layered versioning strategy to manage the grammar specification and language-specific implementations independently.

### Pre-1.0 Status

**Current Status:** Pre-stable (0.x.x versions)

While we don't expect the API or expression syntax to change significantly, we're not yet declaring these versions officially stable. The 0.1.0 API is reasonably stable, but use at your own discretion until we reach 1.0.0.

**Stable Release:** Version `1.0.0` will signify the first officially stable release.

### Expression Syntax Version

The Evalis expression language has its own semantic version, independent of implementation versions. This version is defined in `grammar/Evalis.g4` as a comment at the top of the file.

**Versioning Rules:**
- **Major bump** (e.g., `1.2.0` → `2.0.0`): Breaking changes to existing syntax
- **Minor bump** (e.g., `1.2.0` → `1.3.0`): Backwards-compatible feature additions

**Important:** Adding support for previously invalid syntax is NOT a breaking change. For example, adding the modulo operator (`%`) would be a minor version bump because existing expressions continue to work.

**Version Discovery:**

Each language implementation exports an `EXPRESSION_VERSION` constant indicating which grammar version it supports:

```python
# Python
from evalis import EXPRESSION_VERSION
print(f"Supports grammar v{EXPRESSION_VERSION}")  # "0.1.0"
```

```typescript
// TypeScript
import { EXPRESSION_VERSION } from 'evalis';
console.log(`Supports grammar v${EXPRESSION_VERSION}`);  // "0.1.0"
```

### Language-Specific Package Versions

Each language implementation maintains its own version, following semantic versioning:

**Versioning Rules:**
- **Major bump** (e.g., `3.2.1` → `4.0.0`): Breaking changes to the API or adoption of a breaking grammar version
- **Minor bump** (e.g., `3.2.1` → `3.3.0`): New features or adoption of a new (non-breaking) grammar version
- **Patch bump** (e.g., `3.2.1` → `3.2.2`): Bug fixes and internal improvements

**Examples:**
- If the grammar adds list comprehensions (minor), Python package goes from `1.2.0` → `1.3.0`
- If the grammar breaks `and` operator behavior (major), Python package goes from `1.2.0` → `2.0.0`
- If Python fixes a bug in property access, package goes from `1.2.0` → `1.2.1`

This allows implementations to evolve independently while tracking grammar compatibility.

## Current Implementations

- **Python** - Reference implementation
- **TypeScript** - JavaScript/Node.js support
