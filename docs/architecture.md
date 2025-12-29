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

## Current Implementations

- **Python** - Reference implementation
- **TypeScript** - JavaScript/Node.js support
