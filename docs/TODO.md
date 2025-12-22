# Next Steps

This document outlines the roadmap, priorities, and future enhancements for Evalis.

## High Priority

### New Language Implementations

- [ ] **Go**
- [ ] **Rust**
- [ ] **Java**
- [ ] **C#**
- [ ] **Ruby**
- [ ] **PHP**

### Publishing & Distribution

- [ ] **Publish Python package to PyPI**
  - Set up package metadata
  - Configure build system (setuptools/poetry)
  - Add installation instructions
  - Version management strategy

- [ ] **Publish TypeScript package to npm**
  - Configure package.json for publishing
  - Bundle types and source
  - Add installation instructions
  - Version management strategy

### Documentation

- [ ] **Language-specific README files**
  - Python README with usage examples
  - TypeScript README with usage examples
  - API documentation

- [ ] **Usage examples repository**
  - Real-world use cases
  - Integration patterns
  - Best practices

## Expression Features

### List Comprehensions

- [ ] **Flat mapping with multiple `for` clauses**
  - Syntax: `[x.name for group in groups for x in group.items]`
  - Flattens nested iterations into a single list
  - Requires grammar extension and evaluator updates

- [ ] **Filtering with `if` clause**
  - Syntax: `[x for x in items if x.active]`
  - Conditional filtering during iteration
  - Optional clause in comprehensions

### New Operators

- [ ] **Modulo operator** (`%`)
- [ ] **Exponentiation** (`**` or `^`)
- [ ] **String concatenation** (explicit operator or implicit)
- [ ] **Ternary conditional** (`x if condition else y`)

### Built-in Functions

- [ ] **Type conversion functions**
  - `int()`, `float()`, `str()`, `bool()`

- [ ] **String functions**
  - `len()`, `upper()`, `lower()`, `substring()`

- [ ] **List functions**
  - `len()`, `sum()`, `min()`, `max()`, `filter()`, `map()`

- [ ] **Math functions**
  - `abs()`, `round()`, `floor()`, `ceil()`

### Advanced Features

- [ ] **Null-coalescing operator** (`??`)
- [ ] **Optional chaining** (`?.`)
- [ ] **Object/array literals**
  - `{key: value}` for objects
  - `[1, 2, 3]` for arrays

- [ ] **Regex support**
  - Pattern matching
  - String replacement

## Developer Experience

### Build & Tooling

- [ ] **CI/CD pipeline**
  - Version bumping and releases

### Performance

- [ ] **Benchmarking suite**
  - Cross-language performance comparison
  - Optimization targets

- [ ] **AST caching**
  - Reuse parsed ASTs for repeated expressions
  - Performance improvement for high-frequency evaluation

### Testing & Quality

- [ ] **Expand test coverage**
  - Edge cases for all operators
  - Error handling scenarios

- [ ] **Error messages**
  - Better syntax error reporting
  - Helpful suggestions for common mistakes
  - Line/column information in errors

### Ecosystem

- [ ] **Web playground**
  - Interactive expression tester

---

**Want to contribute?** Pick an item from this list and open an issue to discuss the implementation approach!
