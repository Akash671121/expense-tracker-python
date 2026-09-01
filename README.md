# Expense Tracker

## Overview

Expense Tracker is a desktop application developed using Python, CustomTkinter, and SQLite.

The application allows users to record income and expenses, view transactions, delete selected transactions, and calculate the current balance.

## Features

- Add income and expense transactions
- Select transaction type: Income or Expense
- Add transaction categories
- Enter transaction amounts
- Automatic date recording
- View transactions in a table
- Delete selected transactions
- Automatic balance calculation
- Input validation for categories and amounts
- Dark-themed graphical user interface

## Technologies Used

- Python
- CustomTkinter
- Tkinter
- SQLite
- DateTime

## How It Works

1. The user selects either Income or Expense.
2. The user enters a category and amount.
3. The application validates the entered information.
4. The transaction is stored in the SQLite database.
5. Transactions are displayed in the application table.
6. The current balance is calculated as:

```text
Balance = Total Income - Total Expenses
```
The application also allows the user to delete a selected transaction.

## Database

The application uses SQLite to store transaction data.

The database contains a `transactions` table with:

- ID
- Type
- Category
- Amount
- Date

The database file is created automatically when the application runs.

## Project Structure
```text
expense-tracker-python/
│
├── expense_tracker.py
├── requirements.txt
├── README.md
└── .gitignore
```
## Installation

### 1. Clone the repository
```bash
git clone https://github.com/Akash671121/expense-tracker-python.git
```
### 2. Install the required package
```bash
pip install -r requirements.txt
```
### 3. Run the application
```bash
python expense_tracker.py
```
The SQLite database will be created automatically when the application starts.

## Validation

The application validates:

- Category input to allow alphabetic characters
- Amount input to allow numeric values
- Empty fields are not accepted

## Future Improvements

- Add monthly and yearly expense reports
- Add expense category charts
- Add search and filtering
- Add transaction editing
- Export transactions to CSV
- Add budget management

## Author

**Akash K**
