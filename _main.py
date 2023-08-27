import sqlite3
import datetime
import os

conn = sqlite3.connect("expenses.db")
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS expenses 
(id INTEGER PRIMARY KEY,
Date DATE,
description TEXT,
category TEXT,
price REAL)""")

conn.commit()


while True:
    os.system("cls")
    print("Select an option:")
    print("1. Add an expense")
    print("2. View expenses")
    print("3. Delete an expense")
    print("4. Edit an expense")

    choice = int(input("Enter your choice: "))
    if choice == 1:
        date = input("Enter the date (YYYY-MM-DD): ")
        description = input("Enter a description: ")

        cur.execute("SELECT DISTINCT category FROM expenses")

        categories = cur.fetchall()
        
        print("Select a category (by number):")
        for i, category in enumerate(categories):
            print(f"{i+1}. {categories[i][0]}")
        print(f"{len(categories)+1}. Add a new category")

        category_choice = int(input("Enter your choice: "))
        if category_choice == len(categories) +1:
            category = input("Enter a new category: ")
        else:
            category = categories[category_choice-1][0]
            
        price = float(input("Enter the price: "))

        cur.execute("INSERT INTO expenses (Date, description, category, price) VALUES(?,?,?,?)", (date, description, category, price))

        conn.commit()
    elif choice == 2:
        print("Select an option:")
        print("1. View all expenses")
        print("2. View monthly expenses")
        print("3. View expenses by category")
        
        view_choice = int(input("Enter your choice: "))
        if view_choice == 1:
            cur.execute("SELECT * FROM expenses")
            expenses = cur.fetchall()
            for expense in expenses:
                print(expense)
        elif view_choice == 2:
            month = input("Enter the month (MM): ")
            year = input("Enter the year (YYYY): ")
            cur.execute("SELECT category, SUM(price) FROM expenses WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ? GROUP BY category", (month, year))
            expenses = cur.fetchall()
            for expense in expenses:
                print(f"Category: {expense[0]}, Total: {expense[1]}")
        elif view_choice == 3:
            print("Select a category:")
            cur.execute("SELECT DISTINCT category FROM expenses")
            categories = cur.fetchall()
            for i, category in enumerate(categories):
                print(f"{i+1}. {categories[i][0]}")
            category_choice = int(input("Enter your choice: "))
            category = categories[category_choice-1][0]
            cur.execute("SELECT * FROM expenses WHERE category = ?", (category,))
            expenses = cur.fetchall()
            for expense in expenses:
                print(expense)    
        else:
            exit()

    elif choice == 3:
        print("Select an expense to delete:")
        cur.execute("SELECT * FROM expenses")

        expenses = cur.fetchall()

        for expense in expenses:
            print(expense)

        expense_id = int(input("Enter the ID of the expense to delete: "))

        cur.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()

    elif choice == 4:

        print("Select an expense to edit:")
        cur.execute("SELECT * FROM expenses")
        expenses = cur.fetchall()

        for expense in expenses:
            print(expense)

        expense_id = int(input("Enter the ID of the expense to edit: "))
        cur.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
        expense = cur.fetchone()
        print(expense)

        date = input(f"Enter the new date ({expense[1]}): ")
        description = input(f"Enter the new description ({expense[2]}): ")
        category = input(f"Enter the new category ({expense[3]}): ")
        price = input(f"Enter the new price ({expense[4]}): ")

        cur.execute("UPDATE expenses SET Date = ?, description = ?, category = ?, price = ? WHERE id = ?", (date, description, category, price, expense_id))
        conn.commit()
        
    else:
        exit()

    repeat = input("Would you like to continue? (y/n):\n")
    if repeat.lower() != "y":
        break

conn.close()
