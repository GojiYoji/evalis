#!/usr/bin/env bash
set -euo pipefail

# Make sure there are no unstaged changes before generating
if ! git diff --quiet; then
  echo "Error: You have unstaged changes. Please commit or stash them before running this script."
  git status --short
  exit 1
fi

# Run the makefile generator script
python3 support/generate_makefile.py

# Check if there are unstaged changes after generation
if ! git diff --quiet; then
  echo "Error: The generated Makefile has unstaged changes after running the generator."
  echo "Please review and commit the changes."
  git diff --stat Makefile.gen
  exit 1
fi

echo "No changes detected after generating Makefile. All good!"
