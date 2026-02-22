from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="YOUR_PASSWORD_here"
        database="expense_tracker_db"
    )

@app.route("/")
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM expenses ORDER BY expense_date DESC")
    expenses = cursor.fetchall()

    cursor.execute("""
        SELECT category, SUM(amount) AS total
        FROM expenses
        GROUP BY category
    """)
    summary = cursor.fetchall()

    cursor.execute("SELECT SUM(amount) AS total_spent FROM expenses")
    total = cursor.fetchone()["total_spent"]

    cursor.close()
    connection.close()

    return render_template("index.html",
                           expenses=expenses,
                           summary=summary,
                           total=total)

@app.route("/add", methods=["POST"])
def add_expense():
    amount = request.form["amount"]
    category = request.form["category"]
    note = request.form["note"]

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

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)