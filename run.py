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
    Load data from google sheets, Income in row 1, colum 2 and expenses from row 2.
    Then check if expense desription exists, return income, expenses.
    """
    data = sheet.get_all_records()
    income = 0
    expenses = []
    for record in data:
        if record['Type'] == 'Income':
            income = record['Amount']
        else:
            expenses.append((record['Description'], record['Amount'], record['Date']))
    print(income, expenses)

def save_data_to_sheet(SHEET, income, expenses):
    """
    Save all data to google spreadsheet that is income and expenses.
    """
    SHEET.update_cell(1, 1, "Income")
    SHEET.update_cell(1, 2, income)
    SHEET.resize(2)
    for i, (description, amount) in enumerate(expenses, start=3):
        SHEET.update_cell(i, 1, description)
        SHEET.update_cell(i, 2, amount)

print(Fore.CYAN + "Welcome to My Finance Tracker!\nA program to help you monitor and manage your finances.")
