# Evalis

A polyglot, secure, user-friendly expression evaluator.

## Early Development

This project is in early development. Feel free to adopt and use at your discretion, or contribute to make it better! :)

## Documentation

- **[Architecture](./docs/architecture.md)** - Learn about the polyglot design, shared grammar, and test suite architecture
- **[Recipes](./docs/recipes.md)** - Step-by-step guides for common tasks (e.g., adding a new language)
- **[Next Steps](./docs/TODO.md)** - View the roadmap, TODOs, and priorities

## How to Use?

Evalis has implementations in multiple languages. Check out the language-specific documentation:

- **[Python](./python/README.md)** - Python implementation
- **[TypeScript](./typescript/README.md)** - TypeScript/JavaScript implementation

## How to Contribute?

### Prerequisites

1. Install [`mise`](https://mise.jdx.dev/) - This manages the development environment and tool versions.

### Setup

Once `mise` is installed, run the following from the project root:

```shell
# Install all required tools (Python, Node.js, etc.)
mise install

# Setup all language implementations
make setup
```

This will set up the development environment for all language implementations (Python, TypeScript, etc.).

### Building and Testing

```shell
# Build all implementations
make build

# Run all tests
make test

# Run all linters
make lint
```

For language-specific commands, see the individual language directories.

## Latest Release Versions

| Package    | Release Version |
| ---------- | --------------- |
| python     | 0.2.0           |
| typescript | 0.2.0           |
