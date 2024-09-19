from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from colorama import Fore, Style, init
from tabulate import tabulate
from simple_term_menu import TerminalMenu


init(autoreset=True)


def date_validation(date_str):
    """
    Function to validate date. The date should be in YYYY-MM-DD format,
    Otherwise print an error message and prompt user to input the correct
    format.
    """
    while True:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            date_str = input(
                f"""
{Fore.RED}
Invalid date format! Please enter the date in YYYY-MM-DD format:
            """
            )


def amount_validation(amount_str):
    """
    Function to validate amount. The amount should be a positive interger,
    Otherwise print an error message and allow user to input s positive int.
    """
    while True:
        try:
            amount = int(amount_str)
            if amount < 0:
                raise ValueError(
                    f"""
{Fore.RED}
The amount cannot be a negative number.
                """
                )
            return amount
        except ValueError:
            amount_str = input(
                f"""
{Fore.RED}
Invalid amount! Please enter a positive integer:
            """
            )


def description_validation(description):
    """
    Function to validate the description.
    The description should be a string and not a number,
    Other wise give error message and prompt user to insert a string.
    """
    while True:
        if description.isdigit():
            description = input(f"""{Fore.RED}
Invalid description! Please enter a valid description that is not a number:
            """)
        else:
            return description


def connect_to_google_sheets(my_finance_tracker):
    """
    Connect to google spreadsheet using gspread library
    """
    SCOPE = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive'
        ]

    CREDS = ServiceAccountCredentials.from_json_keyfile_name(
        'creds.json', SCOPE
    )
    CLIENT = gspread.authorize(CREDS)
    SHEET = CLIENT.open(my_finance_tracker).sheet1
    return SHEET


def load_data_from_sheets(SHEET):
    """
    Load data from google sheets,
    """
    data = SHEET.get_all_records()
    income = 0
    expenses = []
    for record in data:
        if record["Type"] == "Income":
            income = record["Amount"]
        else:
            expenses.append(
                (record["Description"], record["Amount"], record["Date"])
            )
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
    income = amount_validation(input(f"{Fore.YELLOW}Enter your income: "))
    income_date = date_validation(
        input(f"{Fore.YELLOW}Enter the date of this income (YYYY-MM-DD): ")
        or datetime.today().strftime("%Y-%m-%d")
    )
    print(
        f"""{Fore.GREEN}
You have successfully entered an income of €{income} on {income_date}
    """
    )
    return income, income_date


def add_expenses():
    """
    Function to allow user to input expenses in a loop until the input is
    'exit', Enter amount as floating number and uppend expense description and
    amount. Confirm each expense by yes or no.
    """
    expenses = []
    while True:
        description = description_validation(
            input(f"""{Fore.YELLOW}
Enter an expense description (or type 'exit' to go back to the Main Menu.):
            """)
        )
        if description.lower() == 'exit':
            break
        amount = amount_validation(
            input(f"""{Fore.YELLOW}
Enter the expense amount:
            """)
        )
        expense_date = date_validation(
            input("""{Fore.YELLOW}
Enter the date of this expense (YYYY-MM-DD): 
            """) or datetime.today().strftime('%Y-%m-%d')
        )
        confirmation = input(
            f"""
{Fore.GREEN}
Did you mean '{description}' with an amount of {amount} on {expense_date}?
(yes/no):
        """
        ).lower()
        if confirmation == 'yes':
            expenses.append((description, amount, expense_date))
            print(
                f"""
{Fore.GREEN}
Expense '{description}' of {amount} spent on {expense_date} has been added
successfully!
            """
            )
        else:
            print(
                f"""
{Fore.RED}
Expense not added because you did not choose 'yes'.
            """
            )
    return expenses


def show_budget(income, expenses):
    """
    Function to calculate budget by adding total expenses and subtracting
    total expense from income to get savings, Print on terminal the income,
    total expenses and savings. Display expenses in a table
    """
    total_expenses = sum([amt for desc, amt, date in expenses])
    savings = income - total_expenses
    print(
        f"""
Income: {income}
Expenses: {total_expenses}
Savings: {savings}
    """
    )

    expense_table = [[desc, amt, date] for desc, amt, date in expenses]
    print(
        tabulate(
            expense_table,
            headers=["Description", "Amount", "Date"],
            tablefmt="grid",
        )
    )


def main():
    """
    Function for Main Menu with 4 options available to user 1-4,
    Otherwise the option is invalid and user is requested to try again.
    """
    income = 0
    income_date = None
    expenses = []

    SHEET = connect_to_google_sheets("my_finance_tracker")
    income, expenses = load_data_from_sheets(SHEET)

    print(f"""{Fore.CYAN}
Welcome to My Finance Tracker!
A program to help you monitor and manage your finances.
Choose one of the options below to get started.
    """)

    while True:
        options = ["Add Income", "Add Expenses", "Show Current Budget", "Exit"]
        terminal_menu = TerminalMenu(options)
        choice = terminal_menu.show()

        if choice == 0:
            income, income_date = add_income()
        elif choice == 1:
            expenses = add_expenses()
        elif choice == 2:
            show_budget(income, expenses)
        elif choice == 3:
            print(f"""{Fore.CYAN}
Saving data to Google SpreadSheets...\nStandby.
            """)
            save_data_to_sheets(SHEET, income, income_date, expenses)
            print(f"{Fore.CYAN}Exiting program...\nGoodbye!")
            break


if __name__ == "__main__":
    main()
