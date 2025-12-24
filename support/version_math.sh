#!/usr/bin/env bash
set -euo pipefail

# Version math utility for semantic versioning
# Usage: version_math.sh <version> <operation>
# Operations: drop-suffix, bump-major, bump-minor, bump-patch

VERSION=${1:-}
OPERATION=${2:-}

if [ -z "$VERSION" ] || [ -z "$OPERATION" ]; then
  echo "Usage: $0 <version> <operation>"
  echo ""
  echo "Operations:"
  echo "  drop-suffix   - Remove suffix (e.g., 0.1.4-dev → 0.1.4)"
  echo "  bump-major    - Increment major version (e.g., 0.1.4 → 1.0.0)"
  echo "  bump-minor    - Increment minor version (e.g., 0.1.4 → 0.2.0)"
  echo "  bump-patch    - Increment patch version (e.g., 0.1.4 → 0.1.5)"
  echo "  bump-dev      - Bump patch and add -dev (e.g., 0.1.4 → 0.1.5-dev)"
  echo "  drop-dev      - Get last release from -dev (e.g., 0.1.5-dev → 0.1.4)"
  echo ""
  echo "Examples:"
  echo "  $0 0.1.4-dev drop-suffix    # Output: 0.1.4"
  echo "  $0 0.1.4 bump-patch         # Output: 0.1.5"
  echo "  $0 0.1.4 bump-minor         # Output: 0.2.0"
  echo "  $0 0.1.4 bump-major         # Output: 1.0.0"
  echo "  $0 0.1.4 bump-dev           # Output: 0.1.5-dev"
  echo "  $0 0.1.5-dev drop-dev       # Output: 0.1.4"
  exit 1
fi

# Split version and suffix (if exists)
if [[ "$VERSION" =~ ^([0-9]+\.[0-9]+\.[0-9]+)(-.*)?$ ]]; then
  BASE_VERSION="${BASH_REMATCH[1]}"
  SUFFIX="${BASH_REMATCH[2]}"
else
  echo "ERROR: Invalid version format: $VERSION"
  echo "Expected format: major.minor.patch[-suffix]"
  exit 1
fi

# Split base version into components
IFS='.' read -r MAJOR MINOR PATCH <<<"$BASE_VERSION"

# Helper function to error if version has -dev suffix
error_if_dev() {
  if [ "$SUFFIX" = "-dev" ]; then
    echo "ERROR: Cannot $OPERATION on a -dev version: ${BASE_VERSION}${SUFFIX}" >&2
    echo "       Call 'drop-dev' first to get the base version, then bump as needed" >&2
    exit 1
  fi
}

case "$OPERATION" in
drop-suffix)
  echo "$BASE_VERSION"
  ;;

bump-major)
  error_if_dev
  MAJOR=$((MAJOR + 1))
  echo "${MAJOR}.0.0"
  ;;

bump-minor)
  error_if_dev
  MINOR=$((MINOR + 1))
  echo "${MAJOR}.${MINOR}.0"
  ;;

bump-patch)
  error_if_dev
  PATCH=$((PATCH + 1))
  echo "${MAJOR}.${MINOR}.${PATCH}"
  ;;

bump-dev)
  error_if_dev
  PATCH=$((PATCH + 1))
  echo "${MAJOR}.${MINOR}.${PATCH}-dev"
  ;;

drop-dev)
  # Only decrement if version has -dev suffix
  if [ "$SUFFIX" != "-dev" ]; then
    # Not a -dev version, return as-is
    echo "$BASE_VERSION"
  else
    # Has -dev suffix, drop it and decrement patch
    if [ "$PATCH" -eq 0 ]; then
      echo "ERROR: Cannot drop-dev from ${BASE_VERSION}${SUFFIX} (patch is already 0)" >&2
      exit 1
    fi
    PATCH=$((PATCH - 1))
    echo "${MAJOR}.${MINOR}.${PATCH}"
  fi
  ;;

*)
  echo "ERROR: Unknown operation: $OPERATION"
  echo "Valid operations: drop-suffix, bump-major, bump-minor, bump-patch, bump-dev, drop-dev"
  exit 1
  ;;
esac
