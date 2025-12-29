#!/usr/bin/env bash

# region: common --------------------------------------------------------------
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# region: get arguments -------------------------------------------------------
SUBDIR=${1:-}

# region: check usages --------------------------------------------------------
if [ -z "$SUBDIR" ]; then
  echo "Usage: $0 <subdir>"
  echo ""
  echo "This script checks both package version and expression version for a subdir."
  echo ""
  echo "To mark a subdir as intentionally behind on grammar version, edit the"
  echo "TODO_EXPRESSION_VERSIONS array in this script with format: \"version#issue\""
  echo ""
  echo "Example: TODO_EXPRESSION_VERSIONS[\"python\"]=\"0.2.0#156\""
  exit 1
fi

# region: TODO expression versions --------------------------------------------
# Hardcoded TODO expression versions for subdirs that are intentionally behind
# Format: "version#issue" (e.g., "0.2.0#42" or "" if none)
declare -A TODO_EXPRESSION_VERSIONS=(
  ["python"]=""
  ["typescript"]=""
)

# region: get versions --------------------------------------------------------
VERSION=$(make -s ${SUBDIR}_get_version)
EXPR_VERSION=$(make -s ${SUBDIR}_get_expression_version)

# region: check package version -----------------------------------------------
${SCRIPT_DIR}/check_readme_version_reference.sh ${SUBDIR} ${VERSION}

# region: check expression version --------------------------------------------
# Check if there's a TODO expression version for this subdir
TODO_ENTRY="${TODO_EXPRESSION_VERSIONS[$SUBDIR]:-}"

if [ -n "$TODO_ENTRY" ]; then
  # Parse version and issue from format "version#issue"
  TODO_VERSION="${TODO_ENTRY%%#*}"
  TODO_ISSUE="${TODO_ENTRY##*#}"

  echo "⚠ Note: ${SUBDIR} has TODO expression version ${TODO_VERSION} (issue #${TODO_ISSUE})"

  # Set TODO_VERSION env var for the check script
  export TODO_VERSION
fi

${SCRIPT_DIR}/check_expression_version_reference.sh ${EXPR_VERSION}
