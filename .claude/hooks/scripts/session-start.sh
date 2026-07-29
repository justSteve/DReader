#!/usr/bin/env bash
# Session start hook — session logging only. DReader is a SERVICE.
#
# This hook used to declare "Session Ritual — MANDATORY: You MUST run /tap-in
# before responding", and DReader carried tap-in and handoff skills to satisfy
# it. Steve ruled 2026-07-29 (decision co-4a47x, executed under co-b4j6u):
# DReader stays a service and the ritual is stripped.
#
# The skills and their permission grants are gone, so this directive had to go
# with them. A hook commanding a skill that no longer exists breaks every
# session start — that is the three-layer alignment rule (gate / rule /
# enforcement) failing in the other direction. Remove one layer, remove all
# three.
#
# What a service gets at session start instead: Claude Code loads CLAUDE.md and
# .claude/rules/ as normal, and `bd prime` reloads the beads protocol on demand.
# A responder does not need cross-session ritual continuity — that is the whole
# distinction in conventions/roster-taxonomy.md. If DReader is ever reclassified
# a zgent, restore all three layers together rather than just this one.

set -euo pipefail

ZGENT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
ZGENT_NAME=$(basename "$ZGENT_DIR")
SESSION_LOG="/var/moo/logs/sessions.jsonl"
SESSION_ID="${CLAUDE_SESSION_ID:-unknown}"

# Detect warm vs cold start
START_TYPE="cold"
if [ -f "$ZGENT_DIR/.claude/state/snapshot.json" ]; then
    START_TYPE="warm"
fi

# Log session start. Kept deliberately — the /var/moo/logs/sessions.jsonl audit
# trail is enterprise observability, not part of the ritual being removed.
jq -n -c \
    --arg ts "$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)" \
    --arg sid "$SESSION_ID" \
    --arg zgent "$ZGENT_NAME" \
    --arg event "session_start" \
    --arg start_type "$START_TYPE" \
    --arg class "service" \
    '{ts:$ts, session_id:$sid, zgent:$zgent, event:$event, start_type:$start_type, class:$class}' \
    >> "$SESSION_LOG" 2>/dev/null || true

cat <<EOF
# DReader — Discord Intelligence Service

Class: **service** (responder architecture; no session ritual by design —
see conventions/roster-taxonomy.md, decision co-4a47x).

There is no /tap-in or /handoff here and that absence is correct. Run
\`bd prime\` if you need the beads protocol reloaded.

Start type: ${START_TYPE}
EOF
