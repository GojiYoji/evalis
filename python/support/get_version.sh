#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="$(dirname "${SCRIPT_DIR}")"

echo $(grep '^__version__' ${PACKAGE_DIR}/src/evalis/constants.py | cut -d'"' -f2)
