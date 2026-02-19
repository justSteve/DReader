@echo off
REM Run DReader retrieval under Windows Python.
REM Prerequisites: pip install pywinauto pyperclip
REM
REM Usage examples:
REM   scripts\run_retrieval.bat --channel general --count 50
REM   scripts\run_retrieval.bat --channel general --count 10 --log-level debug

set REPO_ROOT=%~dp0..
python.exe "%REPO_ROOT%\src\retrieval\run.py" %*
