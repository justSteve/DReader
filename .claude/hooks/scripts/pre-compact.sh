#!/usr/bin/env bash
# pre-compact.sh — PreCompact hook
# Preserves critical context before Claude Code compacts the conversation.
#
# Bead: gt-enforce

set -euo pipefail

COO_DIR="${CLAUDE_PROJECT_DIR:-/root/projects/COO}"

# --- Git state ----------------------------------------------------------------
BRANCH=$(git -C "$COO_DIR" branch --show-current 2>/dev/null || echo "unknown")
DIRTY=$(git -C "$COO_DIR" status --short 2>/dev/null | wc -l || echo "0")
MODIFIED=$(git -C "$COO_DIR" status --short 2>/dev/null | head -10 | tr '\n' ', ' || echo "none")

# --- Active beads -------------------------------------------------------------
BEADS="none"
BEADS_FILE="$COO_DIR/.beads/issues.jsonl"
if [[ -f "$BEADS_FILE" ]]; then
    BEADS=$(grep '"status":"open"' "$BEADS_FILE" 2>/dev/null | jq -r '.id' 2>/dev/null | tr '\n' ', ' || echo "none")
    BEADS="${BEADS%,}"
    [[ -z "$BEADS" ]] && BEADS="none"
fi

# --- Recent enforcement actions -----------------------------------------------
RECENT_ENFORCEMENT="none"
ENF_LOG="/var/moo/audit/enforcement.jsonl"
if [[ -f "$ENF_LOG" ]]; then
    RECENT_ENFORCEMENT=$(tail -3 "$ENF_LOG" 2>/dev/null | jq -r '[.hook, .action, .detail] | join(": ")' 2>/dev/null | tr '\n' '; ' || echo "none")
    [[ -z "$RECENT_ENFORCEMENT" ]] && RECENT_ENFORCEMENT="none"
fi

# --- Last DaysActivity entry --------------------------------------------------
LAST_ACTIVITY="none"
DA_FILE="$COO_DIR/DaysActivity.md"
if [[ -f "$DA_FILE" ]]; then
    LAST_ACTIVITY=$(head -5 "$DA_FILE" 2>/dev/null | tr '\n' ' ' || echo "none")
fi

# --- Emit preserved context ---------------------------------------------------
MSG="Pre-compact context preserved:
- Branch: ${BRANCH}, ${DIRTY} dirty files
- Modified: ${MODIFIED}
- Active beads: [${BEADS}]
- CWD: ${COO_DIR}
- Recent enforcement: ${RECENT_ENFORCEMENT}
- Last activity: ${LAST_ACTIVITY}"

MSG_ESCAPED=$(echo "$MSG" | jq -Rs '.')

echo "{\"systemMessage\":${MSG_ESCAPED}}"
exit 0
