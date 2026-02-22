import mysql.connector
import json
from datetime import datetime

FILE_NAME = "expenses.json"
BUDGET_FILE = "budget.json"

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Amb@4444",
        database="expense_tracker_db"
    )

def load_expenses():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)
def set_budget():
    budget = float(input("Enter monthly budget: ₹"))
    with open(BUDGET_FILE, "w") as file:
        json.dump({"budget": budget}, file)
    print("✅ Budget saved successfully!")

def get_budget():
    try:
        with open(BUDGET_FILE, "r") as file:
            data = json.load(file)
            return data["budget"]
    except FileNotFoundError:
        return None
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)

def add_expense():
    amount = float(input("Enter amount: "))
    category = input("Enter category: ")
    note = input("Enter note: ")

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO expenses (amount, category, note)
    VALUES (%s, %s, %s)
    """

    cursor.execute(query, (amount, category, note))
    connection.commit()

    cursor.close()
    connection.close()

    print("✅ Expense added to database successfully!")

    # expense = {
    #     "amount": amount,
    #     "category": category,
    #     "note": note,
    #     "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # }

    # expenses = load_expenses()
    # expenses.append(expense)
    # save_expenses(expenses)

    # print("✅ Expense added successfully!")

def view_expenses():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    if not expenses:
        print("No expenses found.")
        return

    total = 0
    category_summary = {}

    for expense in expenses:
        print(f"Amount: ₹{expense['amount']}")
        print(f"Category: {expense['category']}")
        print(f"Note: {expense['note']}")
        print(f"Date: {expense['expense_date']}")
        print("-" * 30)
        total += expense["amount"]
        category = expense["category"]

        if category in category_summary:
            category_summary[category] += expense["amount"]
        else:
             category_summary[category] = expense["amount"]

    print(f"\n💰 Total Spent: {total}")

    budget = get_budget()
    if budget:
        print(f"🎯 Monthly Budget: ₹{budget}")
        if total > budget:
            print("⚠ WARNING: You have exceeded your budget!")
        else:
            remaining = budget - total
            print(f"💵 Remaining Budget: ₹{remaining}")
    

    print("\n📊 Category-wise Summary:")
    for category, amount in category_summary.items():
        print(f"  {category}: ₹{amount}")
    cursor.close()
    connection.close()

def main():
    while True:
        print("\n==== Expense Tracker ====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. set Budget")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            set_budget()
        elif choice == "4":    
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()