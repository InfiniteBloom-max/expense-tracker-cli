# Expense Tracker - Troubleshooting Guide

## Installation Issues

### Python Not Found 
**Error** : `python: command not found` or `python is not recognized`

**soulution** :
1. Install Python 3.8+ from https://www.python.org
2. On Windows : Make sure to check "Add Python to PATH" during installation
3. On Mac/Linux : Install via Homebrew
  ```bash
  brew install python
  ```

### Dependecies Not Installing 
**Error** : `pip command not found` or `ModuleNotFoundError`

**Solution** :
```bash
# Check available commands 
python expense_tracker.py --help

# Use exact command name (note use hyphen not underscores !)
python expense_tracker.py set-budget # correct
python expense_tracker.py set_budget # incorrect
```

### Missing Required Options
**Error** : `Error : Missing option '-a' / '--amount'`

**Solution** :
```bash 
# These formats work : 
python expense_tracker.py add --date "2026-02-15" # ISO format
python expense_tracker.py add --date "02/15/2026" # US format
python expense_tracker.py add --date "15/02/2026" # EU format
python expense_tracker.py add --date "today"      # Today
python expense_tracker.py add --date "yersterday" # Yesterday
python expense_tracker.py add --date "last 7"     # 7 days ago
```


## Data Issue 
**Error** : All Transactions disappered


**Solution** : 
1. Check database location : `~/.expense_tracker/expenses.db`
2. If file exists but empty, database was reset
3. Recover from backup:
```bash
# Copy backup file to database location
cp expenses.db.bak ~/.expense_tracker/expenses.db
```