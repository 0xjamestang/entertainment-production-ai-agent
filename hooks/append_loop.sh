#!/usr/bin/env bash
set -euo pipefail
mkdir -p loop
touch loop/state.md loop/last_output.md loop/ci.md loop/corrections.md

{
  echo ""
  echo "---"
  echo "## Iteration $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
  echo ""
  echo "### Agent Output"
  echo ""
  cat loop/last_output.md
  echo ""
  echo "### CI"
  echo ""
  cat loop/ci.md
  echo ""
} >> loop/state.md

# prevent unbounded growth
tail -n 5000 loop/state.md > loop/state.md.tmp && mv loop/state.md.tmp loop/state.md
