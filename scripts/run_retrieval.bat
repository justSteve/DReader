@echo off
REM Run DReader retrieval using venv Python.
REM Prerequisites: .venv created with pywinauto and pyperclip
REM
REM Usage examples:
REM   scripts\run_retrieval.bat --channel general --count 50
REM   scripts\run_retrieval.bat --channel general --count 10 --log-level debug

set REPO_ROOT=%~dp0..
"%REPO_ROOT%\.venv\Scripts\python.exe" "%REPO_ROOT%\src\retrieval\run.py" %*
