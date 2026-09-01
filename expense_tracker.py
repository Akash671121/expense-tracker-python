import customtkinter as ctk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# ---------------- DATABASE ---------------- #


conn = sqlite3.connect("expense_tracker.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    category TEXT,
    amount REAL,
    date TEXT
)
""")
conn.commit()

# ---------------- APP ---------------- #

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Expense Tracker") 
app.geometry("1000x650")
app.minsize(900, 600)

# ---------------- IN-APP ALERT ---------------- #

alert_label = ctk.CTkLabel(app, text="", font=("Segoe UI", 14, "bold"))
alert_label.pack(pady=5)

def show_alert(message, color="red"):
    alert_label.configure(text=message, text_color=color)
    alert_label.after(2000, lambda: alert_label.configure(text=""))

# ---------------- VALIDATION ---------------- #

def is_valid_category(text):
    return text.strip() != "" and text.replace(" ", "").isalpha()

def is_valid_amount(text):
    if text.count(".") > 1 or text.strip() == "":
        return False
    return text.replace(".", "", 1).isdigit()

# ---------------- FUNCTIONS ---------------- #

def add_transaction():
    t_type = type_var.get()
    category = category_entry.get().strip()
    amount = amount_entry.get().strip()

    if not category or not amount:
        show_alert("Please fill all fields ❌", "red")
        return

    if not is_valid_category(category):
        show_alert("⚠ Only Alphabets Allowed!", "red")
        category_entry.focus()
        return

    if not is_valid_amount(amount):
        show_alert("⚠ Only Numbers Allowed!", "red")
        amount_entry.focus()
        return

    amount = float(amount)
    date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(
        "INSERT INTO transactions(type, category, amount, date) VALUES (?, ?, ?, ?)",
        (t_type, category, amount, date)
    )
    conn.commit()

    category_entry.delete(0, "end")
    amount_entry.delete(0, "end")

    load_data()
    update_balance()

    show_alert("Transaction Added ✔", "green")

def load_data():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM transactions ORDER BY id ASC")
    records = cursor.fetchall()

    for index, record in enumerate(records, start=1):
        tree.insert("", "end", values=(
            index,        # UI serial number
            record[0],    # REAL database ID
            record[1],    # type
            record[2],    # category
            record[3],    # amount
            record[4]     # date
        ))

def delete_transaction():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select a row first")
        return

    item = tree.item(selected[0])
    real_id = item["values"][1]   # DB ID (not serial number)

    cursor.execute("DELETE FROM transactions WHERE id=?", (real_id,))
    conn.commit()

    load_data()
    update_balance()

    show_alert("Transaction Deleted 🗑", "orange")
def update_balance():
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Income'")
    income = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Expense'")
    expense = cursor.fetchone()[0] or 0

    balance = income - expense

    balance_label.configure(text=f"Current Balance : ₹{balance:,.2f}")

# ---------------- FIXED LIVE ALERT (NO SPAM) ---------------- #

def live_category_alert(event):
    text = category_entry.get()

    if text and not is_valid_category(text):
        category_entry.configure(border_color="red")

        if not hasattr(live_category_alert, "shown"):
            live_category_alert.shown = False

        if not live_category_alert.shown:
            show_alert("⚠ Only Alphabets Allowed!", "red")
            live_category_alert.shown = True
    else:
        category_entry.configure(border_color="green")
        live_category_alert.shown = False


def live_amount_alert(event):
    text = amount_entry.get()

    if text and not is_valid_amount(text):
        amount_entry.configure(border_color="red")

        if not hasattr(live_amount_alert, "shown"):
            live_amount_alert.shown = False

        if not live_amount_alert.shown:
            show_alert("⚠ Only Numbers Allowed!", "red")
            live_amount_alert.shown = True
    else:
        amount_entry.configure(border_color="green")
        live_amount_alert.shown = False

# ---------------- UI ---------------- #

title = ctk.CTkLabel(app, text="💰 Expense Tracker", font=("Segoe UI", 28, "bold"))
title.pack(pady=20)

# INPUT CARD
card = ctk.CTkFrame(app, corner_radius=15)
card.pack(fill="x", padx=20, pady=10)

type_var = ctk.StringVar(value="Expense")

type_menu = ctk.CTkComboBox(card, values=["Income", "Expense"], variable=type_var, width=200)
type_menu.pack(pady=10)

category_entry = ctk.CTkEntry(card, placeholder_text="Enter Category (Only Alphabets)", width=300)
category_entry.pack(pady=10)

amount_entry = ctk.CTkEntry(card, placeholder_text="Enter Amount (Only Numbers)", width=300)
amount_entry.pack(pady=10)

# LIVE BINDING
category_entry.bind("<KeyRelease>", live_category_alert)
amount_entry.bind("<KeyRelease>", live_amount_alert)

add_btn = ctk.CTkButton(
    card,
    text="➕ Add Transaction",
    fg_color="#22C55E",
    hover_color="#16A34A",
    command=add_transaction
)
add_btn.pack(pady=15)

# BALANCE
balance_frame = ctk.CTkFrame(app, corner_radius=15)
balance_frame.pack(fill="x", padx=20, pady=10)

balance_label = ctk.CTkLabel(
    balance_frame,
    text="Current Balance : ₹0",
    font=("Segoe UI", 20, "bold"),
    text_color="#38BDF8"
)
balance_label.pack(pady=15)

# TABLE
table_frame = ctk.CTkFrame(app)
table_frame.pack(fill="both", expand=True, padx=20, pady=10)

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background="#1E293B",
    foreground="white",
    fieldbackground="#1E293B",
    rowheight=28
)

style.configure(
    "Treeview.Heading",
    background="#38BDF8",
    foreground="black",
    font=("Segoe UI", 10, "bold")
)

columns = ("ID", "Type", "Category", "Amount", "Date")

tree = ttk.Treeview(table_frame, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(fill="both", expand=True)

# DELETE BUTTON
delete_btn = ctk.CTkButton(
    app,
    text="🗑 Delete Selected",
    fg_color="#EF4444",
    hover_color="#DC2626",
    command=delete_transaction
)
delete_btn.pack(pady=15)

# START
load_data()
update_balance()

app.mainloop()

conn.close()