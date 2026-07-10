#!/usr/bin/env bash
# Create a clean branch from template/main and stage selected files from the
# current commit, so the resulting PR contains only the chosen diff (no origin
# history). The source commit is captured BEFORE switching branches.
#
# Usage:
#   scripts/template-contribute.sh <branch-name> [file ...]
#
# Examples:
#   scripts/template-contribute.sh theming-partial src/templates/components/cdns.html
#   scripts/template-contribute.sh theming-partial   # just create the branch
set -euo pipefail

BRANCH="${1:-contribute-to-template}"
shift || true

SRC="$(git rev-parse HEAD)"   # capture source commit before switching

git fetch template --quiet
git checkout -b "$BRANCH" "template/main"

if [ "$#" -gt 0 ]; then
  git checkout "$SRC" -- "$@"
  git add "$@"
  git status --short
  echo
  echo "Staged $# file(s) from $SRC onto '$BRANCH' (based on template/main)."
  echo "Review, then: git commit -m 'feat(template): ...' && git push template $BRANCH"
else
  echo "Branch '$BRANCH' created from template/main."
  echo "Now select files from $SRC:"
  echo "  git checkout $SRC -- path/to/file        # whole file"
  echo "  git restore --source=$SRC --patch -- path/to/file   # hunks"
  echo "  git add path/to/file && git commit -m 'feat(template): ...'"
  echo "  git push template $BRANCH"
fi
