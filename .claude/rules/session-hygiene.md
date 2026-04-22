# Rule: Session Hygiene

## Session Start

1. **Check DaysActivity.md**
   ```bash
   head -5 /root/projects/COO/DaysActivity.md 2>/dev/null
   ```
   - Read recent entries for context on what was done previously
   - Note any open work items

2. **Review CurrentStatus.md** for operational context

## Session End

1. **Update CurrentStatus.md** if state changed significantly

2. **Run `/handoff`** if substantive work was done
   - Prepends session summary to DaysActivity.md
   - Include files changed, open work

3. **Consider knowledge capture**:
   - Learned anything new? Update LearnedSomethingNewToday.md
   - Made mistakes? Update DontDoThisAgain.md

## DaysActivity.md Contents

Each handoff entry includes:
- **Timestamp**: HH:MM in 24-hour format
- **Summary**: What was accomplished (1-2 sentences)
- **Open Work**: In-progress items
- **Files Changed**: One per line (if any)

## Daily Housekeeping

Run `/daily-housekeeping` at start of day (or it runs automatically):
- Archives yesterday's DaysActivity.md
- Creates fresh file for today
