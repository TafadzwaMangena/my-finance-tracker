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

def add_income():
    """
    Function to allow user to add income as a floating number,
    Print f string to user with the income entered.
    """
    income = float(input(f"{Fore.YELLOW}Enter your income: "))
    income_date = input(f"{Fore.YELLOW}Enter the date of this income (YYYY-MM-DD): ") or datetime.today().strftime('%Y-%m-%d')
    print(Fore.GREEN + f"You have successfully entered an income of €{income} on {income_date}")
    return income, income_date

def main():
    """
    Function for Main Menu with 4 options available to user 1-4, 
    Otherwise the option is invalid and user is requested to try again.
    """
    print(Fore.CYAN + "Welcome to My Finance Tracker!\nA program to help you monitor and manage your finances.")
    print("1. Add Income")
    print("2. Add Expenses")
    print("3. Show Current Budget")
    print("4. Exit")
    
    choice = input("Select one of the options, 1, 2, 3 or 4: ")
    if choice == "1":
        income = add_income()
    elif choice == "2":
        print("Add Expenses selected.")
    elif choice == "3":
        print("Show Current Budget selected.")
    elif choice == "4":
        print("Exiting program...\nGoodbye!")
    else:
        print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()