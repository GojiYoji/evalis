#!/usr/bin/env bash
set -euo pipefail

VERSION=${1:-}
TODO_VERSION=${TODO_VERSION:-}

# If version is blank, show usage
if [ -z "$VERSION" ]; then
    echo "Usage: $0 <version>"
    echo "       TODO_VERSION=<version> $0 <version>"
    echo ""
    echo "Arguments:"
    echo "  version       - The expression version your implementation supports"
    echo ""
    echo "Environment Variables:"
    echo "  TODO_VERSION  - Optional. A known grammar version you're intentionally skipping"
    echo ""
    echo "Examples:"
    echo "  $0 0.1.0                              # Check that grammar is 0.1.0"
    echo "  TODO_VERSION=0.2.0 $0 0.1.0           # Grammar should be 0.1.0 or 0.2.0 (TODO)"
    echo ""
    echo "This script verifies that the grammar version matches your implementation's"
    echo "EXPRESSION_VERSION, or matches a known TODO version you're planning to support."
    exit 1
fi

# Find the grammar file
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
GRAMMAR_FILE="$ROOT_DIR/grammar/Evalis.g4"

# Check if grammar file exists
if [ ! -f "$GRAMMAR_FILE" ]; then
    echo "ERROR: Grammar file not found at $GRAMMAR_FILE"
    exit 1
fi

# Extract version from grammar file
# Looking for: // VERSION: x.y.z
GRAMMAR_VERSION=$(grep -E '^\s*//\s*VERSION:' "$GRAMMAR_FILE" | awk '{print $3}')

if [ -z "$GRAMMAR_VERSION" ]; then
    echo "ERROR: Could not find VERSION in $GRAMMAR_FILE"
    echo "Expected format: // VERSION: x.y.z"
    exit 1
fi

# Check if grammar version matches the implementation version
if [ "$GRAMMAR_VERSION" = "$VERSION" ]; then
    echo "✓ Grammar version $GRAMMAR_VERSION matches implementation version $VERSION"
    exit 0
fi

# Check if grammar version matches the TODO version (if provided)
if [ -n "$TODO_VERSION" ] && [ "$GRAMMAR_VERSION" = "$TODO_VERSION" ]; then
    echo "⚠ Grammar version $GRAMMAR_VERSION matches TODO version $TODO_VERSION"
    echo "  Implementation is on version $VERSION (intentionally behind)"
    exit 0
fi

# Version mismatch - provide helpful error message
echo "✗ ERROR: Version mismatch!"
echo ""
echo "  Grammar version:         $GRAMMAR_VERSION"
echo "  Implementation version:  $VERSION"
if [ -n "$TODO_VERSION" ]; then
    echo "  TODO version:            $TODO_VERSION"
fi
echo ""
echo "To fix this, you need to either:"
echo "  1. Update your implementation's EXPRESSION_VERSION to '$GRAMMAR_VERSION'"
echo "  2. OR set TODO_VERSION='$GRAMMAR_VERSION' to acknowledge you're skipping it"
echo ""
echo "Example:"
echo "  TODO_VERSION=$GRAMMAR_VERSION $0 $VERSION"
echo ""
exit 1
