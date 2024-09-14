import gspread
from oauth2client.service_account import ServiceAccountCredentials
from colorama import Fore, Style, init
from tabulate import tabulate
from simple_term_menu import TerminalMenu
from datetime import datetime

init(autoreset=True)

def connect_to_google_sheets(my_finance_tracker):
    """
    Connect to google spreadsheet using gspread library
    """
    SCOPE = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive'
        ]

    CREDS = ServiceAccountCredentials.from_json_keyfile_name('creds.json', SCOPE)
    CLIENT = gspread.authorize(CREDS)
    SHEET = CLIENT.open(my_finance_tracker).sheet1
    return SHEET

SHEET = connect_to_google_sheets("my_finance_tracker")

def load_data_from_sheet(SHEET):
    """
    Load data from google sheets,
    """
    data = sheet.get_all_records()
    income = 0
    expenses = []
    for record in data:
        if record['Type'] == 'Income':
            income = record['Amount']
        else:
            expenses.append((record['Description'], record['Amount'], record['Date']))
    return income, expenses

def save_data_to_sheets(SHEET, income, income_date, expenses):
    """
    Function to add all data to google spread sheet,
    Add loaded data to sheet rows.
    """
    SHEET.clear()
    SHEET.append_row(["Type", "Description", "Amount", "Date"])
    SHEET.append_row(["Income", "", income, income_date])
    for desc, amount, date in expenses:
        SHEET.append_row(["Expense", desc, amount, date])

print(Fore.CYAN + "Welcome to My Finance Tracker!\nA program to help you monitor and manage your finances.")
