# DReader Windows Setup Script
# Run in PowerShell as Administrator

$ErrorActionPreference = "Stop"

Write-Host "=== DReader Windows Setup ===" -ForegroundColor Cyan

# 1. Check/Install Bun
Write-Host "`n[1/5] Checking Bun installation..." -ForegroundColor Yellow
if (Get-Command bun -ErrorAction SilentlyContinue) {
    $bunVersion = bun --version
    Write-Host "  Bun $bunVersion already installed" -ForegroundColor Green
} else {
    Write-Host "  Installing Bun..." -ForegroundColor Yellow
    powershell -c "irm bun.sh/install.ps1 | iex"
    # Refresh PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    Write-Host "  Bun installed" -ForegroundColor Green
}

# 2. Create bridge directory
Write-Host "`n[2/5] Creating chrome-bridge directory..." -ForegroundColor Yellow
$bridgeDir = "C:\temp\chrome-bridge"
if (-not (Test-Path $bridgeDir)) {
    New-Item -ItemType Directory -Path $bridgeDir -Force | Out-Null
    Write-Host "  Created $bridgeDir" -ForegroundColor Green
} else {
    Write-Host "  $bridgeDir already exists" -ForegroundColor Green
}

# 3. Install dependencies
Write-Host "`n[3/5] Installing dependencies..." -ForegroundColor Yellow
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $scriptDir
try {
    bun install
    Write-Host "  Dependencies installed" -ForegroundColor Green
} finally {
    Pop-Location
}

# 4. Run tests
Write-Host "`n[4/5] Running tests..." -ForegroundColor Yellow
Push-Location $scriptDir
try {
    bun test
    Write-Host "  Tests passed" -ForegroundColor Green
} catch {
    Write-Host "  Some tests may have failed (check output above)" -ForegroundColor Yellow
} finally {
    Pop-Location
}

# 5. Create run script
Write-Host "`n[5/5] Creating run script..." -ForegroundColor Yellow
$runScript = @"
@echo off
cd /d "%~dp0"
echo Starting DReader server...
echo Bridge directory: C:\temp\chrome-bridge
echo.
set CHROME_BRIDGE_DIR=C:\temp\chrome-bridge
bun run dev
"@
$runScriptPath = Join-Path $scriptDir "run-server.bat"
$runScript | Out-File -FilePath $runScriptPath -Encoding ASCII
Write-Host "  Created run-server.bat" -ForegroundColor Green

# Done
Write-Host "`n=== Setup Complete ===" -ForegroundColor Cyan
Write-Host @"

Next steps:
  1. Start Chrome with debugging:
     chrome.exe --remote-debugging-port=9222

  2. Run the server:
     .\run-server.bat

  3. Start Claude Code with Chrome (in another terminal):
     claude --chrome

  4. Trigger a scrape:
     curl -X POST http://localhost:3001/api/scrape/start \
       -H "Content-Type: application/json" \
       -d '{"channel_id": "YOUR_CHANNEL_ID", "scrape_type": "initialization"}'

Bridge directory: C:\temp\chrome-bridge
Server URL: http://localhost:3001

"@ -ForegroundColor White
