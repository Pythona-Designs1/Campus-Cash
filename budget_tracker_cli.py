# ============================================================
#         CAMPUS MINI BUDGET TRACKER - CLI VERSION
# ============================================================
# How to run:
#   Open your terminal and type:
#   python budget_tracker_cli.py
# ============================================================

# We store all records in two lists (Python's way of holding
# multiple items in one variable)
income_records = []
expense_records = []


# ── HELPER FUNCTIONS ────────────────────────────────────────

def add_income():
    """Ask the user for an income entry and save it."""
    print("\n── Add Income ──")
    description = input("Description (e.g. Part-time job): ").strip()
    amount = get_positive_number("Amount (GHS): ")
    income_records.append({"description": description, "amount": amount})
    print(f"✔  Income of GHS {amount:.2f} added!")


def add_expense():
    """Ask the user for an expense entry and save it."""
    print("\n── Add Expense ──")
    description = input("Description (e.g. Textbooks): ").strip()
    amount = get_positive_number("Amount (GHS): ")
    expense_records.append({"description": description, "amount": amount})
    print(f"✔  Expense of GHS {amount:.2f} added!")


def view_summary():
    """Display all records and the balance."""
    print("\n" + "=" * 42)
    print("         BUDGET SUMMARY")
    print("=" * 42)

    # ── Income ──
    print("\n  INCOME")
    print("  " + "-" * 30)
    if income_records:
        for i, record in enumerate(income_records, start=1):
            print(f"  {i}. {record['description']:<20} GHS {record['amount']:>8.2f}")
    else:
        print("  No income recorded yet.")

    # ── Expenses ──
    print("\n  EXPENSES")
    print("  " + "-" * 30)
    if expense_records:
        for i, record in enumerate(expense_records, start=1):
            print(f"  {i}. {record['description']:<20} GHS {record['amount']:>8.2f}")
    else:
        print("  No expenses recorded yet.")

    # ── Totals ──
    total_income  = sum(r["amount"] for r in income_records)
    total_expense = sum(r["amount"] for r in expense_records)
    balance       = total_income - total_expense

    print("\n" + "=" * 42)
    print(f"  Total Income  : GHS {total_income:>10.2f}")
    print(f"  Total Expenses: GHS {total_expense:>10.2f}")
    print(f"  Balance       : GHS {balance:>10.2f}")

    if balance > 0:
        print("\n  Status: ✅  You are within budget!")
    elif balance == 0:
        print("\n  Status: ⚠️   Budget is exactly balanced.")
    else:
        print("\n  Status: ❌  You are over budget!")

    print("=" * 42)


def delete_record():
    """Let the user delete one income or expense record."""
    print("\n── Delete a Record ──")
    print("  1. Delete an Income record")
    print("  2. Delete an Expense record")
    choice = input("Choice: ").strip()

    if choice == "1":
        records = income_records
        label   = "Income"
    elif choice == "2":
        records = expense_records
        label   = "Expense"
    else:
        print("Invalid choice.")
        return

    if not records:
        print(f"No {label} records to delete.")
        return

    # Show numbered list so user can pick one
    for i, r in enumerate(records, start=1):
        print(f"  {i}. {r['description']}  — GHS {r['amount']:.2f}")

    try:
        index = int(input("Enter record number to delete: ")) - 1
        if 0 <= index < len(records):
            removed = records.pop(index)
            print(f"✔  Deleted: {removed['description']}")
        else:
            print("Invalid number.")
    except ValueError:
        print("Please enter a valid number.")


def get_positive_number(prompt):
    """Keep asking until the user gives a valid positive number."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("  ⚠  Please enter a number greater than zero.")
            else:
                return value
        except ValueError:
            print("  ⚠  That doesn't look like a number. Try again.")


# ── MAIN MENU LOOP ───────────────────────────────────────────

def main():
    print("\n" + "=" * 42)
    print("   🎓 CAMPUS MINI BUDGET TRACKER 🎓")
    print("=" * 42)

    while True:
        print("\n  MENU")
        print("  1. Add Income")
        print("  2. Add Expense")
        print("  3. View Summary")
        print("  4. Delete a Record")
        print("  5. Exit")
        print()

        choice = input("  Choose an option (1-5): ").strip()

        if choice == "1":
            add_income()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            view_summary()
        elif choice == "4":
            delete_record()
        elif choice == "5":
            print("\n  Goodbye! Stay on budget! 👋\n")
            break
        else:
            print("  ⚠  Invalid option. Please choose 1 to 5.")


# This line means: only run main() when this file is executed
# directly (not when it is imported by another file).
if __name__ == "__main__":
    main()
