#!/usr/bin/env bash
# Integrity gate before opening a PR to the template remote.
# Fails (exit 1) if the diff against template/main contains files that must
# NEVER leave this project: app-specific code, secrets, media, local data.
# Usage: scripts/template-pr-check.sh
set -euo pipefail

git fetch template --quiet

# Forbidden patterns: anything not template-relevant / trust-boundary leakage.
FORBIDDEN=(
  '^src/media/'
  '\.env'
  '\.sqlite3$'
  'secret'
  'credential'
  'node_modules/'
  '__pycache__/'
  '\.venv/'
)

FOUND=0
while IFS= read -r f; do
  [ -z "$f" ] && continue
  for pat in "${FORBIDDEN[@]}"; do
    if printf '%s' "$f" | grep -qiE "$pat"; then
      echo "FORBIDDEN -> $f  (matches: $pat)"
      FOUND=1
    fi
  done
done < <(git diff --name-only "template/main"...HEAD)

if [ "$FOUND" -ne 0 ]; then
  echo
  echo "ABORT: the contribution includes project-private or forbidden files."
  echo "Remove them (git restore --staged <file>) before pushing to template."
  exit 1
fi

echo "OK: diff vs template/main contains only shareable template assets."
git diff --stat "template/main"...HEAD
