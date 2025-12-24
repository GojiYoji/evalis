# Versioning

Evalis uses a multi-layered versioning strategy to manage the grammar specification and language-specific implementations independently.

## Pre-1.0 Status

**Current Status:** Pre-stable (0.x.x versions)

While we don't expect the API or expression syntax to change significantly, we're not yet declaring these versions officially stable. The 0.1.0 API is reasonably stable, but use at your own discretion until we reach 1.0.0.

**Stable Release:** Version `1.0.0` will signify the first officially stable release.

## Expression Syntax Version

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
import { EXPRESSION_VERSION } from "evalis";
console.log(`Supports grammar v${EXPRESSION_VERSION}`); // "0.1.0"
```

## Language-Specific Package Versions

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

## Development Versions

The `main` branch uses `-dev` suffix versions to distinguish unreleased code from published releases.

**Workflow:**

1. **After a release** (e.g., `0.1.3`), immediately commit a new `-dev` version (e.g., `0.1.4-dev`)
2. **During development**, all commits on `main` use the `-dev` version
3. **Before the next release**, evaluate what changed since the last release
4. **Determine version bump** based on the nature of changes (see versioning rules above)
5. **Release with appropriate version** - the final version may differ from the `-dev` number

**Important:** Don't simply drop the `-dev` suffix when releasing. Always evaluate whether the changes warrant a major, minor, or patch bump.

**Example:**

```
0.1.3       (released)
0.1.4-dev   (development on main - bug fixes accumulating)
0.1.4       (release - patch bump appropriate)
0.1.5-dev   (new development cycle begins)
```

If during the `0.1.4-dev` cycle a breaking change was introduced, the release would be `0.2.0` (not `0.1.4`), followed by `0.2.1-dev`.
