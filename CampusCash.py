# ============================================================
#                     💰 CAMPUSCASH 💰
#              Campus Mini Budget Tracker
#                    GUI VERSION 🎓
# ============================================================
#  UNIVERSITY OF ILORIN
#  FACULTY OF COMMUNICATION AND INFORMATION SCIENCE
#  COURSE CODE: COS 102
#
#  TEAM ASSIGNMENT:
#    Task 1 — Data Storage       : Azuka-Peter Ifeanyi & Giwa Mubarak
#    Task 2 — Calculations       : Aileru Yashkrullah & Abdussalam Sufyaan
#    Task 3 — Delete & Validation: Omotosho Muiz & Nkeonye John
#    Task 4 — GUI Layout         : Muhammed Ahmad & Idris Muh'dsani Modibbo
#    Task 5 — Assembly & Testing : Omipidan Abdulazeez & Adeshina Oluwadarasimi Muiz
#
#  HOW TO RUN:
#    python CampusCash.py
# ============================================================

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


# ════════════════════════════════════════════════════════════
#  TASK 1 — DATA STORAGE
#  👤 Azuka-Peter Ifeanyi  — writes add_income()
#  👤 Giwa Mubarak         — writes add_expense()
# ════════════════════════════════════════════════════════════

income_records  = []
expense_records = []

def add_income():
    _open_entry_popup("Income")

def add_expense():
    _open_entry_popup("Expense")


# ════════════════════════════════════════════════════════════
#  TASK 2 — CALCULATIONS & SUMMARY
#  👤 Aileru Yashkrullah  — writes calculate_totals()
#  👤 Abdussalam Sufyaan  — writes update_summary()
# ════════════════════════════════════════════════════════════

def calculate_totals():
    total_income  = sum(r["amount"] for r in income_records)
    total_expense = sum(r["amount"] for r in expense_records)
    balance       = total_income - total_expense
    return total_income, total_expense, balance

def update_summary():
    total_income, total_expense, balance = calculate_totals()
    income_label.config(text=f"Total Income  : N{total_income:,.2f}")
    expense_label.config(text=f"Total Expenses: N{total_expense:,.2f}")
    balance_label.config(
        text=f"Balance       : N{balance:,.2f}",
        fg="#a6e3a1" if balance >= 0 else "#f38ba8"
    )
    if balance > 0:
        status_label.config(text="Within budget!", fg="#a6e3a1")
    elif balance == 0:
        status_label.config(text="Perfectly balanced.", fg="#f9e2af")
    else:
        status_label.config(text="Over budget!", fg="#f38ba8")


# ════════════════════════════════════════════════════════════
#  TASK 3 — DELETE & VALIDATION
#  👤 Omotosho Muiz  — writes validate_amount()
#  👤 Nkeonye John   — writes delete_selected()
# ════════════════════════════════════════════════════════════

def validate_amount(value):
    try:
        amount = float(value)
        if amount <= 0:
            return False, "Amount must be greater than zero."
        return True, amount
    except ValueError:
        return False, "That is not a valid number. Please try again."

def delete_selected():
    selected = table.selection()
    if not selected:
        messagebox.showinfo("Nothing Selected", "Click a row first, then press Delete.")
        return
    item_id     = selected[0]
    values      = table.item(item_id, "values")
    entry_type  = values[0]
    description = values[1]
    amount      = float(values[2])
    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Delete '{description}' (N{amount:.2f}) from {entry_type}?"
    )
    if not confirm:
        return
    target_list = income_records if entry_type == "Income" else expense_records
    for i, r in enumerate(target_list):
        if r["description"] == description and r["amount"] == amount:
            target_list.pop(i)
            break
    refresh_table()
    update_summary()


# ════════════════════════════════════════════════════════════
#  TASK 4 — GUI LAYOUT & WINDOW DESIGN
#  👤 Muhammed Ahmad          — main window, buttons & table
#  👤 Idris Muh'dsani Modibbo — summary panel & footer
# ════════════════════════════════════════════════════════════

root          = None
table         = None
income_label  = None
expense_label = None
balance_label = None
status_label  = None

def build_gui():
    global root, table, income_label, expense_label, balance_label, status_label

    root = tk.Tk()
    root.title("CampusCash | University of Ilorin | COS 102")
    root.state("zoomed")
    root.resizable(True, True)
    root.configure(bg="#1e1e2e")

    # ── University Banner ──
    banner = tk.Frame(root, bg="#313244", pady=4)
    banner.pack(fill="x")
    tk.Label(banner, text="UNIVERSITY OF ILORIN",
             font=("Courier", 10, "bold"), bg="#313244", fg="#f9e2af").pack()
    tk.Label(banner, text="Faculty of Communication and Information Science  |  COS 102",
             font=("Courier", 8), bg="#313244", fg="#cdd6f4").pack()

    # ── App Title ──
    tk.Label(root, text="CAMPUSCASH",
             font=("Courier", 16, "bold"), bg="#1e1e2e", fg="#f9e2af").pack(pady=(8, 1))
    tk.Label(root, text="Your Campus Budget Tracker",
             font=("Courier", 8), bg="#1e1e2e", fg="#6c7086").pack()

    # ── Buttons ──
    btn_frame = tk.Frame(root, bg="#1e1e2e")
    btn_frame.pack(pady=8)
    tk.Button(btn_frame, text="+ Add Income",
              command=add_income,
              bg="#a6e3a1", fg="#1e1e2e", font=("Courier", 9, "bold"),
              relief="flat", padx=12, pady=5, cursor="hand2").pack(side="left", padx=8)
    tk.Button(btn_frame, text="- Add Expense",
              command=add_expense,
              bg="#f38ba8", fg="#1e1e2e", font=("Courier", 9, "bold"),
              relief="flat", padx=12, pady=5, cursor="hand2").pack(side="left", padx=8)
    tk.Button(btn_frame, text="Delete Selected",
              command=delete_selected,
              bg="#45475a", fg="#cdd6f4", font=("Courier", 9),
              relief="flat", padx=12, pady=5, cursor="hand2").pack(side="left", padx=8)

    # ── Table ──
    table_frame = tk.Frame(root, bg="#1e1e2e")
    table_frame.pack(padx=20, fill="both", expand=True)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="#181825", foreground="#cdd6f4",
                    rowheight=24, fieldbackground="#181825",
                    font=("Courier", 9))
    style.configure("Treeview.Heading",
                    background="#313244", foreground="#f9e2af",
                    font=("Courier", 9, "bold"), relief="flat")
    style.map("Treeview", background=[("selected", "#45475a")])
    table = ttk.Treeview(table_frame,
                         columns=("Type", "Description", "Amount (N)"),
                         show="headings", height=8)
    table.heading("Type",        text="Type")
    table.heading("Description", text="Description")
    table.heading("Amount (N)",  text="Amount (N)")
    table.column("Type",        width=100, anchor="center")
    table.column("Description", width=450, anchor="w")
    table.column("Amount (N)",  width=150, anchor="e")
    table.tag_configure("income",  foreground="#a6e3a1")
    table.tag_configure("expense", foreground="#f38ba8")
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    table.pack(fill="both", expand=True)

    # ── Summary Panel ──
    summary_frame = tk.Frame(root, bg="#181825", padx=16, pady=6)
    summary_frame.pack(fill="x", padx=20, pady=(6, 0))
    income_label  = tk.Label(summary_frame, text="Total Income  : N0.00",
                              font=("Courier", 9), bg="#181825", fg="#a6e3a1")
    expense_label = tk.Label(summary_frame, text="Total Expenses: N0.00",
                              font=("Courier", 9), bg="#181825", fg="#f38ba8")
    balance_label = tk.Label(summary_frame, text="Balance       : N0.00",
                              font=("Courier", 10, "bold"), bg="#181825", fg="#cdd6f4")
    status_label  = tk.Label(summary_frame, text="Add your first entry to begin.",
                              font=("Courier", 8), bg="#181825", fg="#6c7086")
    income_label .pack(anchor="w")
    expense_label.pack(anchor="w")
    balance_label.pack(anchor="w", pady=(2, 0))
    status_label .pack(anchor="w", pady=(1, 0))

    # ── Team Footer (Idris Muh'dsani Modibbo) ──
    footer = tk.Frame(root, bg="#181825", pady=6)
    footer.pack(fill="x", pady=(6, 0))

    # Branding
    tk.Label(footer,
             text="CampusCash  |  University of Ilorin  |  COS 102",
             font=("Courier", 7, "bold"), bg="#181825", fg="#f9e2af").pack()

    # Leader
    tk.Label(footer, text="TEAM LEADER",
             font=("Courier", 7), bg="#181825", fg="#6c7086").pack(pady=(4, 0))
    tk.Label(footer, text="OMIPIDAN ABDULAZEEZ",
             font=("Courier", 9, "bold"), bg="#181825", fg="#f9e2af").pack()

    # Members in a horizontal grid — 3 columns to save vertical space
    tk.Label(footer, text="TEAM MEMBERS",
             font=("Courier", 7), bg="#181825", fg="#6c7086").pack(pady=(4, 2))

    members = [
        "Omotosho Muiz",        "Muhammed Ahmad",          "Nkeonye John",
        "Idris Muh'dsani Modibbo", "Adeshina Oluwadarasimi Muiz", "Azuka-Peter Ifeanyi",
        "Abdussalam Sufyaan",   "Aileru Yashkrullah",      "Giwa Mubarak",
    ]

    grid_frame = tk.Frame(footer, bg="#181825")
    grid_frame.pack()

    for i, name in enumerate(members):
        row = i // 3
        col = i % 3
        tk.Label(grid_frame, text=f"👤 {name}",
                 font=("Courier", 8), bg="#181825", fg="#cdd6f4",
                 width=30, anchor="center").grid(row=row, column=col, padx=10, pady=1)


# ════════════════════════════════════════════════════════════
#  TASK 5 — ASSEMBLY & TESTING
#  👤 Omipidan Abdulazeez        — combines all code & fixes bugs
#  👤 Adeshina Oluwadarasimi Muiz — tests everything & reports errors
# ════════════════════════════════════════════════════════════

def _open_entry_popup(entry_type):
    popup = tk.Toplevel(root)
    popup.title(f"Add {entry_type}")
    popup.geometry("340x200")
    popup.resizable(False, False)
    popup.configure(bg="#1e1e2e")
    popup.grab_set()
    tk.Label(popup, text=f"Add {entry_type}",
             font=("Courier", 13, "bold"), bg="#1e1e2e", fg="#f9e2af").pack(pady=(14, 6))
    frame = tk.Frame(popup, bg="#1e1e2e")
    frame.pack(padx=20, fill="x")
    tk.Label(frame, text="Description:", bg="#1e1e2e", fg="#cdd6f4",
             font=("Courier", 10)).grid(row=0, column=0, sticky="w", pady=4)
    desc_entry = tk.Entry(frame, font=("Courier", 10), bg="#313244",
                          fg="#cdd6f4", insertbackground="white", relief="flat")
    desc_entry.grid(row=0, column=1, sticky="ew", padx=(8, 0))
    tk.Label(frame, text="Amount (N):", bg="#1e1e2e", fg="#cdd6f4",
             font=("Courier", 10)).grid(row=1, column=0, sticky="w", pady=4)
    amt_entry = tk.Entry(frame, font=("Courier", 10), bg="#313244",
                         fg="#cdd6f4", insertbackground="white", relief="flat")
    amt_entry.grid(row=1, column=1, sticky="ew", padx=(8, 0))
    frame.columnconfigure(1, weight=1)

    def save():
        desc = desc_entry.get().strip()
        amt_text = amt_entry.get().strip()
        if not desc:
            messagebox.showwarning("Missing Info", "Please enter a description.", parent=popup)
            return
        is_valid, result = validate_amount(amt_text)
        if not is_valid:
            messagebox.showwarning("Bad Amount", result, parent=popup)
            return
        record = {"description": desc, "amount": result}
        if entry_type == "Income":
            income_records.append(record)
        else:
            expense_records.append(record)
        popup.destroy()
        refresh_table()
        update_summary()

    tk.Button(popup, text="Save", command=save,
              bg="#a6e3a1", fg="#1e1e2e", font=("Courier", 10, "bold"),
              relief="flat", padx=12, pady=4, cursor="hand2").pack(pady=12)


def refresh_table():
    for row in table.get_children():
        table.delete(row)
    for r in income_records:
        table.insert("", "end",
                     values=("Income", r["description"], f"{r['amount']:.2f}"),
                     tags=("income",))
    for r in expense_records:
        table.insert("", "end",
                     values=("Expense", r["description"], f"{r['amount']:.2f}"),
                     tags=("expense",))


if __name__ == "__main__":
    build_gui()
    root.mainloop()
