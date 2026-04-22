#!/usr/bin/env bash
# failure-logger.sh — PostToolUseFailure observer hook
# Logs every tool failure to JSONL for diagnosis.
# Pure observer: always exits 0.
#
# Bead: gt-enforce

set -euo pipefail

LOG_FILE="/var/moo/logs/tool-failures.jsonl"
mkdir -p "$(dirname "$LOG_FILE")" 2>/dev/null || true

INPUT=$(cat 2>/dev/null) || true
[[ -z "$INPUT" ]] && exit 0

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // "unknown"' 2>/dev/null || echo "unknown")
ERROR=$(echo "$INPUT" | jq -r '.error // .stderr // "no details"' 2>/dev/null | head -c 500)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null || echo "unknown")
CWD=$(echo "$INPUT" | jq -r '.cwd // ""' 2>/dev/null || echo "")
ZGENT_NAME=$(basename "${CLAUDE_PROJECT_DIR:-${CWD:-unknown}}")

# Auto-rotate at 1MB
if [[ -f "$LOG_FILE" ]]; then
    file_size=$(stat -c%s "$LOG_FILE" 2>/dev/null || echo "0")
    if [[ "$file_size" -gt 1048576 ]]; then
        mv "$LOG_FILE" "${LOG_FILE}.old" 2>/dev/null || true
    fi
fi

jq -n -c \
    --arg ts "$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)" \
    --arg sid "$SESSION_ID" \
    --arg zgent "$ZGENT_NAME" \
    --arg tool "$TOOL_NAME" \
    --arg error "$ERROR" \
    '{ts:$ts,session_id:$sid,zgent:$zgent,tool:$tool,error:$error}' \
    >> "$LOG_FILE" 2>/dev/null || true

exit 0
