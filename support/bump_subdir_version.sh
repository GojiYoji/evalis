#!/usr/bin/env bash

# region: common --------------------------------------------------------------
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# region: parse arguments -----------------------------------------------------
SUBDIR=""
COMMAND=""
FORCE=false
NO_COMMIT=false

while [[ $# -gt 0 ]]; do
	case $1 in
		--force)
			FORCE=true
			shift
			;;
		--no-commit)
			NO_COMMIT=true
			shift
			;;
		*)
			if [ -z "$SUBDIR" ]; then
				SUBDIR="$1"
			elif [ -z "$COMMAND" ]; then
				COMMAND="$1"
			else
				echo "ERROR: Unknown argument: $1"
				exit 1
			fi
			shift
			;;
	esac
done

# region: check usage ---------------------------------------------------------
if [ -z "$SUBDIR" ] || [ -z "$COMMAND" ]; then
	echo "Usage: $0 <subdir> <command> [--force] [--no-commit]"
	echo ""
	echo "Example:"
	echo "  $0 python dev"
	echo "  $0 typescript minor --no-commit"
	echo ""
	echo "Commands:"
	echo "  major   - bumps to the next major version"
	echo "  minor   - bumps to the next minor version"
	echo "  patch   - bumps to the next patch version"
	echo "  dev     - bumps to the next dev version"
	echo ""
	echo "Options:"
	echo "  --force      - allow bumping even with uncommitted changes"
	echo "  --no-commit  - skip auto-commit after bumping version"
	echo ""
	echo "IMPORTANT: If this script is bumping major, minor, or patch versions, it"
	echo "will drop the -dev version if needed."
	exit 1
fi

# region: check for uncommitted changes ---------------------------------------
if ! git diff-index --quiet HEAD --; then
	HAD_CHANGES=true
	if [ "$FORCE" != "true" ]; then
		echo "ERROR: You have uncommitted changes. Commit or stash them first."
		echo "       Or use --force to proceed anyway (auto-commit will be skipped)."
		git status --short
		exit 1
	fi
	echo "⚠️  WARNING: Proceeding with uncommitted changes (--force specified)"
	echo "             Auto-commit will be skipped."
else
	HAD_CHANGES=false
fi

# region: bump version --------------------------------------------------------
CURR_VERSION=$(make -s ${SUBDIR}_get_version)
echo "Found current version for ${SUBDIR}: ${CURR_VERSION}"

BASE_VERSION=$(${SCRIPT_DIR}/version_math.sh ${CURR_VERSION} drop-dev)
NEXT_VERSION=$(${SCRIPT_DIR}/version_math.sh ${BASE_VERSION} bump-${COMMAND})

VERSION=${NEXT_VERSION} make -s ${SUBDIR}_set_version

echo "✅ Bumped ${SUBDIR} version: ${CURR_VERSION} → ${NEXT_VERSION}"

# region: auto-commit ---------------------------------------------------------
if [ "$HAD_CHANGES" = "false" ] && [ "$NO_COMMIT" != "true" ]; then
	echo "Creating commit..."
	git add "${SUBDIR}/"
	git commit -m "chore(${SUBDIR}): bump version to ${NEXT_VERSION}"
	echo "✅ Committed version bump"
	echo ""
	echo "Next steps:"
	echo "  1. Push your branch and create a PR"
	echo "  2. After PR is merged, run the 'Tag Version' workflow to create the release tag"
else
	if [ "$HAD_CHANGES" = "true" ]; then
		echo "⚠️  Skipped auto-commit (had uncommitted changes before bump)"
	else
		echo "⚠️  Skipped auto-commit (--no-commit specified)"
	fi
	echo ""
	echo "Version files updated but not committed. Remember to:"
	echo "  1. Review changes: git diff"
	echo "  2. Commit manually: git add ${SUBDIR}/ && git commit -m 'chore(${SUBDIR}): bump version to ${NEXT_VERSION}'"
fi
