# Python Retrieval Subsystem - Technical Findings

## Summary

The Python keyboard-driven retrieval approach (`src/retrieval/`) is **architecturally blocked** by Discord's rendering model and cannot extract message content.

## Investigation (2026-02-24)

### Attempted Approaches

1. **Keyboard navigation + Clipboard** (original design)
   - Send arrow keys to navigate messages
   - Send Ctrl+C to copy message text
   - **Result**: Failed - Discord doesn't copy messages with Ctrl+C alone

2. **Keyboard navigation + UIA fallback**
   - Navigate with arrow keys
   - Read message text from UIA properties on focused element
   - **Result**: Failed - keyboard focus never enters message list, remains on channel header

3. **UIA tree enumeration** (pywinauto)
   - Walk Windows UI Automation tree to find message elements
   - **Result**: Failed - Discord uses Chromium GPU rendering, not Windows controls

### Root Cause: Chromium Rendering Architecture

Discord (Electron/Chromium app) renders content using GPU/DirectX:

```
Discord Window Structure (via pywinauto):
└─ Chrome_WidgetWin_1 (top window)
   ├─ Chrome_RenderWidgetHostHWND (render surface) - 0 children
   └─ Intermediate D3D Window (GPU rendering)
```

The Windows UI Automation tree **does not contain message elements**. Message content is rendered pixels on a DirectX surface, not accessible as Windows controls.

### Verification

```powershell
python test_uia_enum.py
# Output shows only 2 elements: window container and render surface
# No message elements in tree despite messages being visible on screen
```

## Alternative Approaches

### 1. TypeScript + Claude Chrome Extension ✅ VIABLE
**Status**: Already implemented in `src/domain/scrape-engine/`

- Uses Claude Code's `--chrome` flag for browser control
- Accesses Discord via DOM/JavaScript (real web content)
- Can extract messages, metadata, threads
- **Limitation**: User reported `claude --chrome` was buggy

**Recommendation**: Debug and fix Claude Chrome integration rather than abandon it.

### 2. Computer Vision / OCR ❌ NOT VIABLE
- Screenshot Discord window
- OCR to extract text
- **Problems**: Slow, unreliable, loses metadata (author, timestamp, threads)

### 3. Chrome DevTools Protocol ❌ BLOCKED
- Control Discord via CDP (chrome debugging protocol)
- **Problem**: Discord detects and blocks CDP connections

### 4. Discord API ❌ BLOCKED
- Official Discord bot API
- **Problem**: Self-bots banned, official bots can't read message history retroactively

## Conclusion

**Python pywinauto approach is fundamentally incompatible with Discord's architecture.**

The TypeScript + Claude Chrome approach (already implemented) remains the only viable path for DReader's mission.

## Files Affected

- `src/retrieval/` - Python subsystem (non-functional for Discord)
- `test_uia_enum.py` - Investigation script
- Bead `dr-zc5` - Closed as "won't fix"

## Next Steps

1. Focus on TypeScript scraper (`src/domain/scrape-engine/`)
2. Debug Claude Chrome integration issues
3. Consider deprecating Python retrieval subsystem
4. Update README to clarify supported approaches
