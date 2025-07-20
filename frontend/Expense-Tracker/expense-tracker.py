import argparse
import json
import os
import datetime

EXPENSES_FILE = "expenses.json"
BUDGET_FILE = "budget.json"

# Load existing expenses from a file
def load_expenses():
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, "r") as f:
            return json.load(f)
    return []

# Save expenses to a file
def save_expenses(expenses):
    with open(EXPENSES_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

# Load budget from file
def load_budget():
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, "r") as f:
            return json.load(f)
    return None

# Save budget to file
def save_budget(budget):
    with open(BUDGET_FILE, "w") as f:
        json.dump({"budget": budget}, f, indent=4)

# Delete expense
def delete_expense(expenses, id):
    for i, expense in enumerate(expenses):
        if expense["id"] == id:
            expenses.pop(i)
            return f"Item '{expense['description']}' of ID {id} deleted successfully."
    return f"ID {id} not found"

# Load data
expenses = load_expenses()
budget = load_budget()

# Get next ID
id = expenses[-1]["id"] + 1 if expenses else 1

parser = argparse.ArgumentParser(
    prog="Expense Tracker",
    description="Track your expenses with add, delete, and list features.",
    epilog="Expense tracking made simple."
)

subparsers = parser.add_subparsers(dest="command", required=True)

# Add command
add = subparsers.add_parser("add", help="Add a new expense.")
add.add_argument("-d", "--description", required=True, type=str, help="Name of your expense.")
add.add_argument("-a", "--amount", required=True, type=float, help="The cost of your expense.")

# Delete command
delete = subparsers.add_parser("delete", help="Delete an expense using its ID")
delete.add_argument("-id", required=True, type=int, help="Provide the ID to delete")

# List command
list_parser = subparsers.add_parser("list", help="Show all expenses with optional filtering")
list_parser.add_argument("-y", "--year", type=int, help="Filter expenses by year")
list_parser.add_argument("-m", "--month", type=int, help="Filter expenses by month")

# Budget command
budget_parser = subparsers.add_parser("budget", help="Set a budget for tracking")
budget_parser.add_argument("-b", "--budget", required=True, type=float, help="Set your budget")

# Update Command
update = subparsers.add_parser("update", help="Update an expense by ID.")
update.add_argument("-id", required=True, type=int, help="ID of the expense to update.")
update.add_argument("-d", "--description", type=str, help="New description (optional).")
update.add_argument("-a", "--amount", type=float, help="New amount (optional).")

args = parser.parse_args()

if args.command == "add":
    date = str(datetime.date.today())

    expense = {"description": args.description, "amount": args.amount, "id": id, "date": date}
    expenses.append(expense)

    save_expenses(expenses)
    print(f"Added expense '{args.description}' of ${args.amount:.2f}.")

elif args.command == "list":
    if not expenses:
        print("No expenses recorded.")
    else:
        filter_year = args.year if args.year else datetime.date.today().year
        filter_month = args.month

        filtered_expenses = [
            e for e in expenses
            if (str(filter_year) in e["date"]) and (not filter_month or e["date"][5:7] == f"{filter_month:02d}")
        ]

        filtered_expenses.sort(key=lambda e: e["date"])

        print(f"{'ID':<5} {'Description':<20} {'Amount':<10} {'Date'}")
        print("-" * 50)
        for i, expense in enumerate(filtered_expenses, 1):
            print(f"{i:<5} {expense['description']:<20} ${expense['amount']:<10.2f} {expense['date']}")
        print("-" * 50)

        total_spent = sum(e["amount"] for e in filtered_expenses)
        print(f"Total expenses: ${total_spent:.2f}")

        # Check budget
        if budget is not None:
            remaining_budget = budget["budget"] - total_spent
            if remaining_budget < 0:
                print(f"Oh no! You're ${-remaining_budget:.2f} beyond the budget!")
            else:
                print(f"You're within budget with ${remaining_budget:.2f} left.")

elif args.command == "delete":
    print(delete_expense(expenses, args.id))
    save_expenses(expenses)

elif args.command == "budget":
    save_budget(args.budget)
    print(f"Budget set to ${args.budget:.2f}.")

elif args.command == "update":
    date_u = str(datetime.date.today())
    updated = False  # Track whether any changes were made

    for expense in expenses:
        if expense["id"] == args.id:
            if args.description:
                expense["description"] = args.description
                updated = True 
            if args.amount:
                expense["amount"] = args.amount
                updated = True  
            if updated:
                expense["date"] = date_u  # Only update the date if something changed
                save_expenses(expenses)
                print(f"Expense ID {args.id} updated successfully.")
            else:
                print("No changes provided. Expense remains the same.")
            break
    else:
        print(f"Expense with ID {args.id} not found.")
