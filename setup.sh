#!/bin/bash

echo "Expense Tracker - Setup"
echo "======================="
echo ""

# Check if python is installed 
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then 
    echo "ERROR : Python3 is not installed"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "Found: $PYTHON_VERSION"
echo ""

# Check pip 
echo "Checking pip..."
if ! command -v pip3 &> /dev/null; then
    echo "ERROR : pip3 is not installed"
    exit 1
fi

echo ""
echo "Installing dependencies..."
pip3 install click rich requests

if [$? -ne 0]; then
    echo "ERROR : Failed to install dependencies"
    exit 1
fi

echo ""
echo "Testing application..."
python3 expense_tracker.py --help > /dev/null

if [$? -ne 0]; then 
    echo "ERROR : Failed to test application"
    exit 1
fi

echo "Test passed !"
echo ""
echo "Setup complete !"
echo ""
echo "Quick start:"
echo " python3 expense_tracker.py add -a 50 -c 'Groceries' -d 'shopping'"
echo " python3 expense_tracker.py list"
echo " python3 expense_tracker.py dashboard"
echo ""
echo "Create an alias for easier access (optional):"
echo " Add this to ~/.bashrc or ~/.zshrc:"
echo " alias expense='python3 $(pwd)/expense_tracker.py'"
echo ""
echo "For more help:"
echo " - Run: python3 expense_tracker.py --help"
echo ""