import gspread
from oauth2client.service_account import ServiceAccountCredentials
from colorama import Fore, Style, init
from tabulate import tabulate
from simple_term_menu import TerminalMenu

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