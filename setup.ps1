# Expense Tracker - Setup Script for Windows 

Write-Host "Expense Tracker - Setup" -Foreground Cyan
Write-Host "=======================" -Foreground Cyan
Write-Host ""

# Check if Python is installed 
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0){
    Write-Host "ERROR : Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org" -ForegroundColor Yellow
    exit 1
}

Write-Host "Found : $pythonVersion" -ForegroundColor Green
Write-Host ""

# Install dependencies 
Write-Host "Installing dependencies..." -ForegroundColor Yellow 
pip install click rich pandas 
if($LASTEXITCODE -ne 0){
    Write-Host "ERROR : Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org" -ForegroundColor Yellow
    exit 1
}

Write-Host "Found : $pythonVersion" - ForegroundColor Green 
Write-Host ""

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install click rich pandas
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR : Failed to install dependencies" - ForegroundColor Red
    exit 1 
}

Write-Host ""
Write-Host "Setup completed!" -ForegroundColor Green
Write-Host ""

# Test the app
Write-Host "Testing application..." -ForegroundColor Yellow
python expense_tracker.py  --help | Out-Null
if($LASTEXITCODE -ne 0){
    Write-Host "ERROR : Application test failed" -ForegroundColor Red
    exit 1
}

Write-Host "Test Passed!" -ForegroundColor Green
Write-Host ""


# Create Shortcut suggestion
Write-Host "Optional : Create a shortcut for easy access" -ForegroundColor Cyan
$shortcutPath = Read-Host "Enter shortcut path Enter to skip (e.g., c:\expense.cmd)"

if ($shortcutPath){
    $scriptPath = (Get-Item "expense_tracker.py").FullName
    $pythonPath = (python -c "import sys; print(sys.executable)")
    $content = "@echo off `npython ` `"$scriptPath`" %*`npause"
    Set-Content -Path $shortcutPath -Value $content
    Write-Host "Shortcut created at: $shortcutPath" -ForegroundColor Green
}

Write-Host ""
Write-Host "Ready to go!" -ForegroundColor Green
Write-Host ""
Write-Host "Quick start"  -ForegroundColor Cyan
Write-Host " python expense_tracker.py add -a 50 -c 'Groceries' -d 'Shopping'"
Write-Host " python expense_traker.py list"
Write-Host " python expense_tracker.py dashboard"
Write-Host ""
Write-Host "For more help:" -ForegroundColor Cyan
Write-Host "  - Check QUICKSTART.md for common commands"
Write-Host "  - Run: python expense_tracker.py --help"
Write-Host ""
