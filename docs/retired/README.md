# Retired: browser-automation retrieval

Steve retired the Playwright/Selenium DOM-scraping track on 2026-09-12
(bead dr-4ov). Retrieval is now screen capture of Steve's own Discord
client, transcribed by Gemini: see `discord-reader/`.

The code is gone from the tree but not from history. Tag
`playwright-retired` marks the last commit that carried it:

    git checkout playwright-retired -- src/retrieval tests/retrieval \
        scripts/probe_ax_tree.py scripts/vision_driver.py scripts/run_retrieval.bat

The documents in this folder are kept for what they learned, in
particular `vision-scrape-experiment.md` (vision reads beat DOM reads on
replies and lists), which is the finding the current approach rests on.
