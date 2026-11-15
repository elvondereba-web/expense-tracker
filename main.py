import os
import json
from datetime import datetime

DATA_FILE = "expenses.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

def add_expense(expenses):
    try:
        amount = float(input("Enter amount (KES/USD): "))
        category = input("Enter category (e.g., Food, Transport, Utilities): ").strip().capitalize()
        description = input("Enter description: ").strip()
        
        expense = {
            "date": datetime.today().strftime("%Y-%m-%d"),
            "amount": amount,
            "category": category,
            "description": description
        }
        expenses.append(expense)
        save_data(expenses)
        print("Expense added successfully!\n")
    except ValueError:
        print("Invalid amount entered. Please enter a valid number.\n")

def view_expenses(expenses):
    if not expenses:
        print("No expenses recorded yet.\n")
        return
    
    print("-" * 60)
    print(f"{'Date':<12} | {'Category':<15} | {'Amount':<10} | {'Description'}")
    print("=" * 60)
    
    for expense in expenses:
        print(f"{expense['date']:<12} | {expense['category']:<15} | {expense['amount']:<10.2f} | {expense['description']}")
    
    print("=" * 60 + "\n")

def main():
    expenses = load_data()
    
    while True:
        print("=== Expense Tracker ===")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Exit")
        
        choice = input("Choose an option (1-3): ").strip()
        
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.\n")

if __name__ == "__main__":
    main()