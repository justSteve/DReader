---
name: tap-in
description: Initialize session with context briefing for PaneWarden
context: fork
allowed-tools: Bash, Read, Glob, Write
---

# Tap In — Session Initialization (PaneWarden)

Read recent activity and current state to get oriented at session start.

## Workflow

### 1. Get current date

```bash
date +%Y-%m-%d
```

---

### 2. Check if daily housekeeping is needed

```bash
head -1 /root/projects/PaneWarden/DaysActivity.md 2>/dev/null
```

- If date doesn't match today: run `/daily-housekeeping` first, then resume tap-in.

---

### 3. Read recent activity

Last 2–3 entries from `DaysActivity.md` — note open work, state, continuity threads:

```bash
head -80 /root/projects/PaneWarden/DaysActivity.md
```

---

### 4. Read inception context (first session after clone)

If you've never seen this repo before, the founding docs live in `inception/`:

```bash
ls /root/projects/PaneWarden/inception/
cat /root/projects/PaneWarden/inception/steve-directives.md 2>/dev/null | head -50
```

- `plan.html` — Pane Warden design plan (originated in COO meeting 2026-04-19)
- `meeting-notes.md` — open-questions meeting doc; decisions that shaped the zgent
- `steve-directives.md` — the three operating directives (shared-executable-space, fork doctrine, aspirational-vs-active)

Read these on first boot. Don't re-read every session — they're not current-state docs.

---

### 5. Read inherited enterprise context

Per `CLAUDE.md` §Inherited Enterprise Context, the canonical sources live under COO:

- `/root/projects/COO/docs/enterprise-integration-narrative-2026-04-18.md`
- `/root/projects/COO/conventions/`
- `/root/projects/COO/.claude/rules/`

Read targeted sections as relevant; don't bulk-read.

---

### 6. Check open beads

```bash
bd ready
bd list --status in_progress
```

---

### 7. Check tmux state (PaneWarden's domain)

```bash
tmux list-sessions 2>/dev/null
tmux list-sockets 2>/dev/null
```

Note which sessions are live — that's the shared executable space this zgent stewards.

---

### 8. Output session briefing

Write to `/root/projects/PaneWarden/session-briefing.md`:

```markdown
## Session Briefing — YYYY-MM-DD HH:MM

### Recent Activity

**Last handoff**: [timestamp] — [brief summary]

**Open work (carried forward)**:
- [item]

---

### Tmux state

**Live sessions**:
- [name] ([windows])

---

### Open beads

| Bead | Status | Title |
|------|--------|-------|
| pw-xxx | open | ... |

---

### Resumption guidance

1. [specific next step]
2. [specific next step]

---

### Ready status

[Ready to proceed | Issues require attention]
```

---

## Pairs with

- `/handoff` — session end (prepends to DaysActivity.md)

## Re-run anytime

```
/tap-in
```
