#!/usr/bin/env bash
# shutdown-filter.sh — UserPromptSubmit hook
# Detects --shutdown in user prompt and injects mini-handoff instructions.
#
# When triggered, the original prompt still reaches Claude, but a systemMessage
# is appended instructing Claude to perform a mini-handoff before responding.

set -euo pipefail

INPUT=$(cat)
if [[ -z "$INPUT" ]]; then
    exit 0
fi

USER_PROMPT=$(echo "$INPUT" | jq -r '.user_prompt // empty')
if [[ -z "$USER_PROMPT" ]]; then
    exit 0
fi

# Check if the prompt contains --shutdown (case-insensitive)
if echo "$USER_PROMPT" | grep -qi -- '--shutdown'; then
    # Strip --shutdown from the prompt so Claude sees clean text
    # Return systemMessage with mini-handoff instructions
    TIMESTAMP=$(date +%H:%M)
    TODAY=$(date +%Y-%m-%d)

    # Log session end (symmetric with session-start.sh)
    SESSION_LOG="/var/moo/logs/sessions.jsonl"
    SESSION_ID="${CLAUDE_SESSION_ID:-unknown}"
    ZGENT_NAME=$(basename "${CLAUDE_PROJECT_DIR:-$(pwd)}")
    jq -n -c \
        --arg ts "$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)" \
        --arg sid "$SESSION_ID" \
        --arg zgent "$ZGENT_NAME" \
        --arg event "session_end" \
        --arg trigger "shutdown_signal" \
        '{ts:$ts, session_id:$sid, zgent:$zgent, event:$event, trigger:$trigger}' \
        >> "$SESSION_LOG" 2>/dev/null || true

    jq -n -c \
        --arg ts "$TIMESTAMP" \
        --arg today "$TODAY" \
        '{systemMessage: ("[shutdown-filter] The user has signaled session shutdown via --shutdown. Before responding to anything else in their message, you MUST perform a mini-handoff:\n\n1. Summarize what was accomplished this session (1-2 sentences)\n2. List any open/in-progress work\n3. Prepend a handoff entry to DaysActivity.md using the /handoff skill format:\n   ## " + $ts + " - Session Handoff [Brief Topic]\n   **Summary**: ...\n   **Open Work**: ...\n   **Files Changed**: ...\n   ---\n4. After the handoff entry is written, respond to the user with a brief goodbye confirming the handoff is done.\n\nTimestamp: " + $ts + " | Date: " + $today + "\nThis is the LAST thing you do in this session. Keep it concise.")}'
    exit 0
fi

# No --shutdown detected — pass through silently
exit 0
