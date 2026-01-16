#!/usr/bin/env bash
set -euo pipefail
mkdir -p loop

echo "# CI snapshot - $(date -u +'%Y-%m-%dT%H:%M:%SZ')" > loop/ci.md
echo "" >> loop/ci.md

# Detect ecosystem
HAS_NODE=0
HAS_PY=0
[ -f package.json ] && HAS_NODE=1
[ -f pyproject.toml ] || [ -f requirements.txt ] && HAS_PY=1

run_and_capture () {
  local title="$1"; shift
  echo "## $title" >> loop/ci.md
  echo '```' >> loop/ci.md
  ( "$@" ) >> loop/ci.md 2>&1 || true
  echo '```' >> loop/ci.md
  echo "" >> loop/ci.md
}

if [ "$HAS_NODE" -eq 1 ]; then
  run_and_capture "node - npm test" bash -lc "npm test"
  run_and_capture "node - lint (if exists)" bash -lc "npm run -s lint || true"
  run_and_capture "node - typecheck (if exists)" bash -lc "npm run -s typecheck || true"
fi

if [ "$HAS_PY" -eq 1 ]; then
  run_and_capture "python - pytest" bash -lc "pytest -q || true"
  run_and_capture "python - ruff (if exists)" bash -lc "ruff check . || true"
  run_and_capture "python - mypy (if exists)" bash -lc "mypy . || true"
fi
