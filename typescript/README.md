# Evalis

A secure, user-friendly expression evaluator for TypeScript and JavaScript.

> **Early Release**: This is an early release with core functionality. More features are in active development. Check the [main project](https://github.com/GojiYoji/evalis) for roadmap and updates.

## Installation

```bash
npm install evalis
```

## Quick Start

```typescript
import { evaluateExpression } from 'evalis';

const context = { a: { b: 5 } };
const value = evaluateExpression('a.b + 2', context);

console.log(value); // 7
```

## Features

- **Safe evaluation** - No `eval()`. No access to global namespace.
- **Simple syntax** - Familiar expressions with property access, operators, and comprehensions.
- **Type-safe** - Full TypeScript support with type definitions included.

## Supported Operations

- **Arithmetic**: `+`, `-`, `*`, `/`
- **Comparison**: `==`, `!=`, `<`, `<=`, `>`, `>=`
- **Logical**: `and`, `or`, `not`
- **Property access**: `obj.property`, `obj['key']`
- **Array access**: `arr[0]`
- **List comprehensions**: `[x * 2 for x in numbers]`
- **Membership**: `x in collection`

## More Information

This is the TypeScript/JavaScript implementation of Evalis. For more details about the project:

- [Main Project](https://github.com/GojiYoji/evalis)
- [Architecture](https://github.com/GojiYoji/evalis/blob/main/docs/architecture.md)
- [Python Implementation](https://github.com/GojiYoji/evalis/tree/main/python)

## License

MIT
