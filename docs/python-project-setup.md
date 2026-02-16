# Python Project Setup Guide

Reference configuration for Python 3.12+ projects.

## Directory Structure

```
project/
├── .env                 # Secrets (gitignored)
├── .venv/               # Virtual environment (gitignored)
├── pyproject.toml       # Project config and dependencies
├── src/
│   └── *.py
└── .gitignore
```

## 1. .gitignore Entries

Add to existing `.gitignore`:

```gitignore
# Python
.venv/
__pycache__/
*.pyc
.env
```

## 2. pyproject.toml Template

```toml
[project]
name = "project-name"
version = "0.1.0"
description = "Project description"
requires-python = ">=3.12"
dependencies = [
    # Add runtime dependencies here
]

[project.optional-dependencies]
dev = [
    "ruff>=0.4.0",
    "mypy>=1.10.0",
]

[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]

[tool.mypy]
python_version = "3.12"
strict = true
```

## 3. Environment Variables

Create `.env` for secrets:

```bash
# .env
API_KEY=your-secret-here
```

Load in Python:

```python
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY environment variable not set")
```

Add `python-dotenv>=1.0.0` to dependencies.

## 4. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows
```

## 5. Install Dependencies

```bash
pip install -e .               # Install project + dependencies
pip install -e ".[dev]"        # Include dev tools
```

## Verification

```bash
python -m py_compile src/your_module.py   # Syntax check
ruff check src/                            # Lint
mypy src/                                  # Type check
```

## 6. VS Code Configuration

Create `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.terminal.activateEnvironment": true,

  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit"
    }
  },

  "python.analysis.typeCheckingMode": "basic",
  "python.analysis.autoImportCompletions": true,
  "python.analysis.diagnosticMode": "workspace"
}
```

Create `.vscode/extensions.json`:

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "charliermarsh.ruff"
  ]
}
```

## Checklist

- [ ] `.gitignore` includes `.venv/`, `__pycache__/`, `*.pyc`, `.env`
- [ ] `pyproject.toml` exists with `requires-python = ">=3.12"`
- [ ] Secrets in `.env`, not in source code
- [ ] `.venv/` created with `python3 -m venv .venv`
- [ ] Dependencies installed via `pip install -e .`
- [ ] `.vscode/settings.json` configured for Pylance + Ruff
- [ ] `.vscode/extensions.json` recommends Python tooling
