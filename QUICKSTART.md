# Expense Tracker - Quickstart Guide

## Installation (30 seconds)

```bash
pip install click rich pandas
```


## Your First Expense (2 minutes)

```bash 
# Add a expense
python expenses_tracker.py add -a 25 -c "Groceries" -d "weekly shopping"

# Add income 
python expense_tracker.py add -a 3000 -c "Salary" -d "Monthly salary" -t income 

# View all expenses
python expense_tracker.py list
```

## Set Budgets 

```bash
python expenses_tracker.py budget -c "Groceries" -b 100

# View all budgets
python expenses_tracker.py budget list
```

## View Your Spending 
```bash 
# See this month's summary by category
python expense_tracker.py summary

# Check your financial dashboard 
python expense_tracker.py dashbaord

# View detailed statistics
python  expense_tracker.py stats
```

## Common Commands

| Task | Command |
|------|---------|
|Add expense     |  `python expense_tracker.py add -a 50 -c "Food" -d "Pizza"`       |
|View last 7 days  | `python expense_tracker.py list -d 7`  |

