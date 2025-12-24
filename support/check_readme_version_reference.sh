#!/usr/bin/env bash
set -euo pipefail

PACKAGE_NAME=${1:-}
VERSION_ARG=${2:-}

# If the package_name is blank or version is blank, show usage
if [ -z "$PACKAGE_NAME" ] || [ -z "$VERSION_ARG" ]; then
  echo "Usage: $0 <package_name> <version>"
  echo ""
  echo "Example:"
  echo "  $0 python 0.1.0"
  echo ""
  echo "This script checks if the README.md contains a reference to the"
  echo "specified package name and version in table format."
  exit 1
fi

# Find the README.md (assume it's in the parent directory of support/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
README_PATH="$ROOT_DIR/README.md"

# Drop the "-dev" from the given version
VERSION=$(${SCRIPT_DIR}/version_math.sh ${VERSION_ARG} drop-dev)

# Check if README.md exists
if [ ! -f "$README_PATH" ]; then
  echo "ERROR: README.md not found at $README_PATH"
  exit 1
fi

# Look for pattern: | package_name | version |
# This handles markdown table format with flexible whitespace
PATTERN="^\s*\|\s*${PACKAGE_NAME}\s*\|\s*${VERSION}\s*\|"

if grep -qE "$PATTERN" "$README_PATH"; then
  echo "✓ Found ${PACKAGE_NAME} ${VERSION} in README.md"
  exit 0
else
  echo "✗ ERROR: ${PACKAGE_NAME} ${VERSION} not found in README.md"
  echo ""
  echo "Expected pattern: | ${PACKAGE_NAME} | ${VERSION} |"
  echo ""
  echo "Please update README.md to include this version reference."
  exit 1
fi
