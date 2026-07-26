#!/usr/bin/env bash
# find_previous.sh — deterministic previous-report lookup for vibe-coding-review.
#
# Matches reports by frontmatter `source_repo` (NOT by the project name in the
# filename, which breaks when a project is renamed).
#
# Usage:
#   find_previous.sh <review_dir> <source_repo> [count]     # list recent reports
#   find_previous.sh <review_dir> <source_repo> --tags      # aggregate issue tags
#
# Output (list mode), newest first:
#   === <filename>
#   created: ... | review_type: ...
#   scores: project_clarity=9 architecture_understanding=9 ...
#   review_issue_tags: tag-a, tag-b
#
# Exit codes: 0 ok (even if zero matches), 1 usage error, 2 dir missing.

set -euo pipefail

if [ $# -lt 2 ]; then
  echo "usage: $0 <review_dir> <source_repo> [count|--tags]" >&2
  exit 1
fi

REVIEW_DIR=$1
SOURCE_REPO=$2
MODE=${3:-5}

if [ ! -d "$REVIEW_DIR" ]; then
  echo "error: review_dir not found: $REVIEW_DIR" >&2
  exit 2
fi

SCORE_KEYS="project_clarity architecture_understanding ai_direction_quality product_judgment_quality validation_awareness compounding_quality"

# Collect matching files (frontmatter source_repo equals the given repo path).
# Real frontmatter blocks run up to ~50 lines; keep a margin.
matches=()
while IFS= read -r -d '' f; do
  if head -n 60 "$f" | grep -q "^source_repo: ${SOURCE_REPO}$"; then
    matches+=("$f")
  fi
done < <(find "$REVIEW_DIR" -maxdepth 1 -name '*.md' -print0 | sort -rz)

if [ "$MODE" = "--tags" ]; then
  echo "# issue-tag frequency across ${#matches[@]} matching reports (reuse-first)"
  for f in "${matches[@]+"${matches[@]}"}"; do
    awk '/^review_issue_tags:/{flag=1;next} flag&&/^[a-zA-Z_]+:/{flag=0} flag&&/^  - /{print $2}' "$f"
  done | grep -v '^tag-or-none$' | sort | uniq -c | sort -rn
  exit 0
fi

COUNT=$MODE
echo "# ${#matches[@]} report(s) match source_repo: ${SOURCE_REPO}"
echo "# showing newest ${COUNT}:"
shown=0
for f in "${matches[@]+"${matches[@]}"}"; do
  [ "$shown" -ge "$COUNT" ] && break
  shown=$((shown + 1))
  echo "=== $(basename "$f")"
  head -n 60 "$f" | grep -E '^(created|review_type):' | tr '\n' ' ' | sed 's/ $//'
  echo
  scores=""
  for k in $SCORE_KEYS; do
    v=$(head -n 80 "$f" | grep -E "^  ${k}:" | head -n1 | awk '{print $2}')
    scores="${scores}${k}=${v:-?} "
  done
  echo "scores: ${scores}"
  tags=$(awk '/^review_issue_tags:/{flag=1;next} flag&&/^[a-zA-Z_]+:/{flag=0} flag&&/^  - /{print $2}' "$f" | tr '\n' ',' | sed 's/,$//; s/,/, /g')
  echo "review_issue_tags: ${tags:-none}"
done
if [ "${#matches[@]}" -eq 0 ]; then
  echo "# NO matching previous report. Only after seeing this zero-match output may a report claim '暂无上一份可比较报告'."
fi
