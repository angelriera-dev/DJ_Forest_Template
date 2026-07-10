#!/usr/bin/env bash
# List files that differ between current HEAD and template/main.
# Use this to choose what to contribute back to the template repo.
# Usage: scripts/template-diff.sh [--stat|--name-only]
set -euo pipefail

MODE="${1:---stat}"
git fetch template --quiet

case "$MODE" in
  --name-only) git diff --name-only "template/main"...HEAD ;;
  --stat)      git diff --stat    "template/main"...HEAD ;;
  *) echo "unknown mode: $MODE" >&2; exit 1 ;;
esac
