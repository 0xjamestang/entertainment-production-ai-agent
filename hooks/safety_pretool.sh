#!/usr/bin/env bash
set -euo pipefail

# Read hook event JSON from stdin
EVENT="$(cat)"

# Basic denylist for shell tool
# (Keep it simple: block destructive ops and credential exfil patterns)
if echo "$EVENT" | grep -Eiq '"tool_name"\s*:\s*"shell"'; then
  if echo "$EVENT" | grep -Eiq 'rm\s+-rf\s+/( |"|$)|:\(\)\s*\{|\bcurl\b.*\b(token|secret|apikey)\b|\bwget\b.*\b(token|secret|apikey)\b|\baws\s+configure\b|\bssh\b|\bscp\b'; then
    echo "Blocked potentially dangerous shell command. Use a safer alternative or ask for approval." 1>&2
    exit 2
  fi
fi

exit 0
