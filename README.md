#   Expense Tracker CLI 
A powerful , user-firendly command-line interface tracking application built with python.

## Features 

** Core Feature **
- Add expenses/income with dates, categories and descriptions
- List expenses with filtering (date range, category , type)
- Monthly summaries grouped by categories
- Budget management with alets 
- Search Expenses by description or category 
- Export to CSV
- Dashbaord with key metrics 
- Detailed statistics and trend 

## Beautiful CLI
- color-coded output
- Rich formatted tables
- Progress indicators
- Interactive prompts


## Installation 

1. Install python 3.8+
2. Install dependencies 
```bash
pip install -r requirements.txt
```

3. Run the app 
```bash
python expense_tracker.py --help
```

## Usage  : Commands 

### Add an Expense
```bash
python expense_tracker.py add -a 25.50 -c "Groceries" -d "Weekly Shopping"
python expense_tracker.py add -a 50 -c "Rent" -d "Monthly Rent" --date 2024-02-01
```

### Add Income
```bash
python expense_tracker.py add -a 3000 -c "Salary" -d "Monthly salary" -t income
```

### Vew Expenses
```bash 
# Last 30 days
python expense_tracker.py list 

# Last 7 days
python expense_tracker.py list -d 7

# Specific category 
python expense_tracker.py list -c "Groceries"

# Specific month
python expense_tracker.py list -m 2024-02

# only income 
python expense_tracker.py list -t income 
```

### Monthly Summary
```bash 
# Current month 
python expense_tracker.py summary

# Specific month 
python expense_tracker.py summary -m 2024-02
```

### Budget Management
```bash 
# Set budget for category 
python expense_tracker.py budget -c "Groceries" -l 300 -m 2024-02

# View budget status
python expense_tracker.py budget-status -m 2024-02
```

### Search 
```bash 
python expense_tracker.py search "coffee"
python expense_tracker.py search "amazon" -t expense
```

### Dashboard
```bash
python expense_tracker.py dashboard
```

### Statistics 
```bash 
python expense_tracker.py stats
```

### view Categories
```bash 
python expense_tracker.py categories 
```

### Export Data
```bash 
# Current month
python expense_tracker.py export -o expenses.csv

# Specific month 
python expense_tracker.py export -o feb_expenses.csv -m 2024-02
```

### Delete Expense 
```bash
python expense_tracker.py delete 5
```

## Date Formats Supported 

- `today` - Current date
- `yesterday` - Previous day
- `last 7` - 7 days ago
- `2024-02-15` - ISO format
- `02/15/2024` - US format
- `15/02/2024` - EU format

## Database 

Data is stored in : `~/.expense_tracker/expenses.db` (SQLite)

## Keybaord Shortcuts

when prompted for confirmation, use:
- `y` or `yes` to confirm
- `n` or `no` to cancel 

## Troubleshooting (COMMON PROBLEMS)

** Where is my data stored ? **
A : `~/.expense_tracker/expenses.db`

** Can I delete an expense ? **
A : Yes, use the `delete` command with the expense id (visible in list output)

** can I edit an expense ? **
A : Delete and re-add it for now (havent implemenented a edit feature)

** How do I backup my data ? **
A : Use `export` to create CSV backups, or copy the `.expense_tracker` folder

## License 

MIT 
