@echo off
REM Run DReader retrieval under Windows Python (not WSL).
REM Prerequisites: pip install pywinauto pyperclip  (Windows pip, not WSL pip)
REM
REM Usage examples:
REM   scripts\run_retrieval.bat --channel general --count 50
REM   scripts\run_retrieval.bat --channel general --count 10 --log-level debug
REM
REM From WSL2:
REM   cmd.exe /c scripts\\run_retrieval.bat --channel general --count 50

set REPO_ROOT=%~dp0..
python.exe "%REPO_ROOT%\src\retrieval\run.py" %*
