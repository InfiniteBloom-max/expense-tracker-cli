"""
Expense Tracking CLI  A powerful command line expense tracking application 
Created on 2/15/2026
Author Ronith Rashmikara 
"""

# imports section 

import sqlite3 # for saving data
import json 
import csv # to export data to csv
from datetime import datetime , timedelta # for date and time
from pathlib import Path # for file path 
from typing import Optional, List, Tuple 
import click 
from rich.console import Console 
from rich.table import Table 
from rich.panel import Panel 
from rich import print as rprint 
from rich.style import style 
from rich.text import Text 

# Initialize rich console 
console = Console()

# Database setup with the paths 
DB_PATH = Path.home() / ".expense_tracker" / "expenses.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Color scheme for the CLI 

COLOR_INCOME = "green"
COLOR_EXPENSE = "red"
COLOR_NEUTRAL = "cyan"
COLOR_WARNING = "yellow"

# initialize the database connection and the table 

def get_connection():
     """Get database connection with row factory"""
     conn = sqlite3.connect(DB_PATH)
     conn.row_factory = sqlite3.Row
     return conn

def init_db():
    """Initialize the database with required tables """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        date TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        type TEXT DEFAULT 'expense',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP      
        )
""")
    

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budgets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT UNIQUE NOT NULL,
        budget_limit REAL NOT NULL,
        month TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def parse_date(date_str : str) -> str:
    """Parse various date formats and returns in format YYYY-MM-DD"""
    try: 
        # TRY common formats
        for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%m/%d", "%d/%m/%Y", "%d/%m"]:
            try : 
                dt = datetime.strptime(date_str, fmt)
                # Handle Short dates without year
                if fmt in ["%m/%d", "%d/%m"]:
                    dt = dt.replace(year=datetime.now().year)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue

            # Handle relative dates 
            today = datetime.now()
            if date_str.lower() ==  "today":
                return today.strftime("%Y-%m-%d")
            elif date_str.lower() == "yesterday":
                return (today - timedelta(days=1)).strftime("%Y-%m-%d")
            elif date_str.lower().startswith("last"):
                parts = date_str.lower().split()
                if len(parts) >= 2:
                    try: 
                        days = int(parts[1])
                        return (today - timedelta(days=days)).strftime("%Y-%m-%d")
                    except ValueError:
                        pass
            return today.strftime("%Y-%m-%d")
    except Exception:
        return datetime.now().strftime("%Y-%m-%d") 



# CLI AND Database function called 
@click.group 
def cli():
    """ Expense Tracker - Manage your Finances from the terminal """
    init_db()

@cli.command()
# for CLI options 
@click.option("--amount", "-a", type=float, required=True, help="Amount spent")
@click.option("--category", "-c", default="General", help="Expenses category")
@click.option("--description", "-d", help="Description of the expense")
@click.option("--date", default="today", help="Date (YYYY-MM-DD or 'today')")
@click.option("--type", "-t", type=click.Choice(["expense", "income"]), default="expense", help="Type of transation")


def add(amount:float , category:str , description : str, date: str, type : str):
    """Add a new expense or income to the database """
    parsed_date = parse_date(date)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses (date, amount, category, description , type)
        VALUES(?,?,?,?,?)
        """, (parsed_date, amount , category , description , type))
    

    conn.commit()
    conn.close()

    color = COLOR_INCOME if type == "income" else COLOR_EXPENSE
    symbol = "+" if type == "income" else "-"
    console.print(f"[{color}]{symbol}${amount:.2f}[/{color}] added to {category}", style ="bold")

@cli.command()
@click.option("--days" , "-d", type=int , default= 30, help ="Show expenses from last N days")
@click.option("--category", "-c", default=None, help="Filter by category")
@click.option("--month", "-m", default=None, help="Show Specific month (YYYY-MM)")
@click.option("--type", "-t", type=click.Choice(["all", "expense", "income"]), default = "all", help="Filter by type")

# listing the expenses 
def list(days: int , category : Optional[str], month : Optional[str], type : str):
    """List expenses with filters"""
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM expenses WHERE 1=1"
    params = []

    if month : 
        query += " AND date LIKE ?"
        params.append(f"%{month}%")
    else :
         start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
         query += " AND date >= ?"
         params.append(start_date)

    if category :
        query += " AND category = ?"
        params.append(category)
    
    if type != "all":
        query += " AND type = ?"
        params.append(type)

    query += " ORDER BY date DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()


    if not rows:
        console.print("[yellow]No expenses found.[/yellow]")
        return

    table = Table(title=f"Expenses (Last {days} days)" if not month else f"Expenses for {month}")
    table.add_column("Date", style=COLOR_NEUTRAL)
    table.add_column("Category", style="magenta")
    table.add_column("Description", style="white")
    table.add_column("Amount", justify="right")
    table.add_column("Type", justify="right")

    total = 0
    for row in rows:
         color = COLOR_INCOME if row[4] == "income" else COLOR_EXPENSE
         amount_str = f"+${row[2]:.2f}" if row[4] == "income" else f"-${row[2]:.2f}"
         table.add_row(
             row[1],
             row[3],
             row[5] or "-",
             f"[{color}]{amount_str}[/{color}]",
             row[4]
         )
         if row[4] == "expense":
             total += row[2]
         else :
             total -= row[2]
        
    console.print(table)

    net_style = COLOR_INCOME if total < 0 else COLOR_EXPENSE
    console.print(f"\n[bold {net_style}]Total : ${abs(total):.2f}[/bold {net_style}]")


@cli.command()
@click.option("--month", "-m", default = None , help ="Specific month (YYYY-MM) or leave blank for current")

def summary(month: Optional[str]):
    """Show monthly summary by category"""
    if not month:
        month = datetime.now().strftime("%Y-%m")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
         SELECT category, type, SUM(amount) as total
         FROM expenses
         WHERE date LIKE ?
         GROUP BY category, type
         ORDER BY total DESC
         """, (f"{month}%",))
    
    rows = cursor.fetchall()
    conn.close()


    if not rows:
        console.print(f"[yellow]No expenses for {month}[/yellow]")
        return
    
    table = Table(title=f"Monthly Summary - {month}")
    table.add_column("Category", style="magenta")
    table.add_column("Expenses", style=COLOR_EXPENSE , justify="right" )
    table.add_column("Income", style=COLOR_INCOME, justify="right")
    table.add_column("Net", style="cyan", justify="right")

    categories = {}
     for row in rows:
         if row[0] not in categories: 
             categories[row[0]] = {"expense": 0, "income": 0}
         categories[row[0]][row[1]] = row[2]


    
    total_expense = 0
    total_income = 0

    for category in sorted(categories.keys()):
        expense = categories[category]["expense"]
        income = categories[category]["income"]
        net = income - expense

        total_expense += expense
        total_income += income

        table.add_row(
            category, 
            f"${expense:.2f}" if expense > 0 else "-",
            f"${income:.2f}" if income > 0 else "-",
            f"[cyan]${net:.2f}[/cyan]" if net != 0 else "-"
        )

        console.print(table)


        net_total = total_income - total_expense
        console.print(f"\n[bold]Month Total:[/bold]")
        console.print(f" [green]Income: ${total_income:.2f}[/green]")
        console.print(f" [cyan]Net : ${net_total:.2f}[/cyan]")
        

@cli.command()
@click.option("--category", "-c", required=True, help="Category name")
@click.option("--limit", "-l", type=float, required=True, help="Budget limit")
@click.option("--month", "-m", default=None, help="Month (YYYY-MM) or current month")

def set_budget(category: str , limit : float, month : Optional[str]):
    """Setting a budget limit for a category"""
    if not month:
        month = datetime.now().strftime("%Y-%m")

    conn = get_connection()
    cursur = conn.cursor()

    cursur.execute("""
        INSERT OR REPLACE INTO budgets (category, budget_limit, month)
        VALUES (?,?,?)
    """, (category, month, limit))

    conn.commit()
    conn.close()

    console.print(f"[cyan]Budget set:[/cyan] {category} - ${limit:.2f} for {month}")

@cli.command()
@click.option("--month", "-m", default=None, help="Specific month (YYYY-MM)")

def budget_status(month: Optional[str]):
    """Show budget status for all categories"""
    if not month:
        month = datetime.now().strftime("%Y-%m")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT category , budget_limit FROM budgets WHERE month =?", (month,))
    budgets = cursor.fetchall()

    if not budgets:
        console.print(f"[yellow]No budgets set for this month[/yellow]")
        conn.close()
        return 
    
    table = Table(title=f"Budget Status - {month}")
    table.add_column("Category", style="magenta")
    table.add_column("Budget", style="cyan", justify="right")
    table.add_column("Spent", style=COLOR_EXPENSE, justify="right")
    table.add_column("Remaining", justify="right")

    for budget in budgets:
        category = budget["category"]
        limit = budget["budget_limit"]

        cursor.execute("""
            SELECT SUM(amount) as total FROM expenses
            where category = ? AND date LIKE ? AND type = 'expense'
        """, (category, f"{month}%"))

        result = cursor.fetchone()
        spent = result["total"] if result["total"] else 0
        remaining = limit - spent
        percent = (spent / limit * 100) if limit > 0 else 0
        

        remaining_color = COLOR_WARNING if percent >= 80 else "green" if percent < 50 else "yellow"
        status_color = "red" if remaining < 0 else remaining_color

        table.add_row(
            category,
            f"${limit:.2f}",
            f"${spent:.2f}",
            f"[{status_color}]${remaining:.2f}[/{status_color}]",
            f"[{status_color}]{percent:.1f}%[/{status_color}]"
        )

        if remaining < 0 :
            console.print(f"[red] {category} budget exceeded by ${abs(remaining):.2f}[/red]")
    
    console.print(table)
    conn.close()


@cli.command()
@click.argument("query")
@click.option("--type", "-t", type=click.Choice(["all","expense","income"]),default="all")

def search(query: str, type: str):
    """ Search expenses by description or category"""
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT * FROM expenses
        WHERE (description LIKE ? OR category LIKE ?)
    """

    params = [f"%{query}%", f"%{query}%"]

    if type != "all":
        sql += " AND type = ?"
        params.append(type)

    sql += " ORDER BY date DESC"

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()

    if not rows :
        console.print(f"[yellow]No results for '{query}'[/yellow]")
        return 

    table = Table(title=f"Search Results for '{query}'")
    table.add_column("Date", style=COLOR_NEUTRAL)
    table.add_column("Category", style="magenta")
    table.add_column("Description", style="white")
    table.add_column("Amount", justify="right")

    for row in rows: 
        color = COLOR_INCOME if row["type"] == "income" else COLOR_EXPENSE
        amount_str =  f"+${row['amount']:.2f}" if row["type"] == "income" else f"-${row['amount']:.2f}"
        table.add_row(
            row["date"],
            row["category"],
            row["description"] or "-",
            f"[{color}]{amount_str}[/{color}]"
        )

    console.print(table)


@cli.command()
@click.option("--output", "-o", type=click.Path(), default="expenses.csv", help="Output file path")
@click.option("--month", "-m", default=None, help="Export specific month (YYYY-MM)")

def export(output: str, month: Optional[str]):
    """"Export expenses to CSV"""
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM expenses WHERE 1=1"
    params = []


    if month : 
        query += " AND date LIKE ?"
        params.append(f"{month}%")

    query += " ORDER by date DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        console.print("[yellow]No data to export[/yellow]")
        return 
    
    with open(output, "w", newline="") as csvfile:
        fieldnames = ["Date", "Amount", "Category", "Description", "Type"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in rows:
             writer.writerow({
                 "Date" : row[1],
                 "Amount" : f"{row[2]:.2f}",
                 "Category" : row[3],
                 "Description" : row[5] or "-",
                 "Type" : row[4]
             })

    console.print(f"[green]Exported {len(rows)} transactions to {output}[/green]")

@cli.command()

# dashboard function 
def dashboard():
    """Show a dashbaord with key metrics"""
    conn = get_connection()
    cursor = conn.cursor()

    current_month = datetime.now().strftime("%Y-%m")

    # This month stats
    cursor.execute("""
            SELECT type , SUM(amount) as total FROM expenses    
            WHERE date LIKE ?
            GROUP BY type    
            """, (f"{current_month}%"))
    
    month_stats = {row[0]: row[1] for row in cursor.fetchall()}

    # Last 7 days
    last_7_days = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    cursor.execute("""
         SELECT SUM(amount) as total FROM expenses
         WHERE date >= ? AND type = "expense"
     """, (last_7_days,))

     week_expense = cursor.fetchone()[0] or 0

    # Categories breakdown 
    cursor.execute("""
        SELECT category, SUM(amount) as total FROM expenses
        WHERE date LIKE ? AND type = "expense"
        GROUP BY category
        ORDER BY total DESC
        LIMIT 5
    """, (f"{current_month}%",))

    top_categories = cursor.fetchall()
    conn.close()

    # Create dashboard 
    month_expense = month_stats.get("expense", 0)
    month_income = month_stats.get("income", 0)
    net = month_income - month_expense

    console.print("\n")

    # Top row - key metric 
    metrics = Table(show_header=False, box=None)
    metrics.add_row(
        Panel(f"[red]${month_expense:.2f}[/red]", title="This Month Spent", expand=False),
        Panel(f"[green]${month_income:.2f}[/green]", title="This Month Income", expand=False),
        Panel(f"[cyan]${net:.2f}[/cyan]", title="Net", expand=False)
    )

    console.print(metrics)

    # Weekly Spending
    console.print(Panel(f"[yellow]${week_expense:.2f}[/yellow]", title="Last 7 days Spending"))

    # Top categories 
    if top_categories:
        cat_table = Table(title="Top Spending Categories This Month")
        cat_table.add_column("Category", style="magenta")
        cat_table.add_column("Amount", style =COLOR_EXPENSE)

        for cat in top_categories:
            cat_table.add_row(cat[0], f"${cat[1]:.2f}")

        console.print(cat_table)

    console.print()

@cli.command()
@click.argument("expense_id", type=int)

# delete function 
def delete(expense_id : int):
    """Delete an expense by ID"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
    expense = cursor.fetchone()

    if not expense:
        console.print("[red]Expense not found[/red]")
        conn.close()
        return 

    if click.confirm(f"Delete '{expense['description']}' (${expense['amount']:.2f})?"):
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        console.print("[green]Expense deleted[/green]")
    
    conn.close()

@cli.command()

def categories():
    """Show all categories used"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT category, COUNT(*) as count
        FROM expenses
        GROUP BY category
        ORDER BY count DESC
    """)


    rows = cursor.fetchall()
    conn.close()

    if not rows:
        console.print("[yellow]No categories yet[/yellow]")
        return


    table = Table(title="ALL categories")
    table.add_column("Category", style="magenta")
    table.add_column("Count", style="cyan")

    for row in rows:
        table.add_row(row[0], str(row[1]))

    console.print(table)

@cli.command()

# statistics function 
def stats():
    """Show detailed statistics"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT type, COUNT(*) as count, SUM(amount) as total
    FROM expenses
    GROUP BY type             
    """)

    stats_data = {}
    for row in cursor.fetchall():
        stats_data[row[0]] = {"count": row[1], "total": row[2] or 0}

    # Last 3 month comparison 
    cursor.execute("""
       SELECT 
          strftime('%Y-%m', date ) as month,
          type,
          SUM(amount) as total
        FROM expenses 
        WHERE date >= date('now', '-3 months')
        GROUP BY month , type
        ORDER BY month DESC  
    """)

    monthly_stats = cursor.fetchall()
    conn.close()

    # Display all-time stats
    console.print("\n[bold cyan]ALL-Time Statistics [/bold cyan]")
    all_table = Table()
    all_table.add_column("Type", style="magenta")
    all_table.add_column("Count", style="cyan", justify="right")
    all_table.add_column("Total", justify="right")

    for exp_type in ["expense", "income"]:
        if exp_type in stats_data: 
            data = stats_data[exp_type]
            color = COLOR_EXPENSE if exp_type == "expense" else COLOR_INCOME
            all_table.add_row(
                exp_type.capitalize(),
                str(data["count"]),
                f"[{color}]${data['total']:.2f}[/{color}]"
            )

    console.print(all_table)

    # monthly breakdown 
    if monthly_stats:
        console.print("\n[bold cyan]Last 3 Months [/bold cyan]")
        monthly_table = Table()
        monthly_table.add_column("Month", style=COLOR_NEUTRAL)
        monthly_table.add_column("Expense", style=COLOR_EXPENSE)
        monthly_table.add_column("Income", style=COLOR_INCOME)

        months_dict = {}
        for row in monthly_stats:
            month = row[0]
            if month not in months_dict:
                months_dict[month] = {"expense": 0, "income": 0}
            months_dict[month][row[1]] = row[2]

        for month in sorted(months_dict.keys(), reverse=True):
            monthly_table.add_row(
                month,
                f"${months_dict[month]['expense']:.2f}",
                f"${months_dict[month]['income']:.2f}"
            )

        console.print(monthly_table)
        console.print()
    
if __name__ == "__main__":
    cli()