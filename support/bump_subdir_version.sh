#!/usr/bin/env bash

# region: common --------------------------------------------------------------
set -xeuo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# region: get arguments -------------------------------------------------------
SUBDIR=${1:-}
COMMAND=${2:-}

# region: check usages --------------------------------------------------------
if [ -z "$SUBDIR" ] || [ -z "$COMMAND" ]; then
	echo "Usage: $0 <subdir> <command>"
	echo ""
	echo "Example:"
	echo "  $0 python dev"
	echo ""
	echo "Commands:"
	echo "  major   - bumps to the next major version"
	echo "  minor   - bumps to the next minor version"
	echo "  patch   - bumps to the next patch version"
	echo "  dev     - bumps to the next dev version"
	echo ""
	echo "IMPORTANT: If this script is bumping major, minor, or patch versions, it"
	echo "will drop the -dev version if needed."
	exit 1
fi

CURR_VERSION=$(make -s ${SUBDIR}_get_version)
echo "Found current version for ${SUBDIR}: ${CURR_VERSION}"

BASE_VERSION=$(${SCRIPT_DIR}/version_math.sh ${CURR_VERSION} drop-dev)
NEXT_VERSION=$(${SCRIPT_DIR}/version_math.sh ${BASE_VERSION} bump-${COMMAND})

VERSION=${NEXT_VERSION} make -s ${SUBDIR}_set_version
