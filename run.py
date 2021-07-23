import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    gets sales data in input
    """
    while True:      
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input('enter your data here:')
        sales_data = data_str.split(',')

        if validate_data(sales_data):
            print('valid data.')
            break
    return sales_data

def validate_data(values):
    """
    validated the input data
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(f'6 values needed you added {len(values)}')      
    except ValueError as e:
        print(f'invalid data {e}, please try again.\n')
        return False
    return True


def update_sales_worksheet(data):
    """
    updated the google worksheet in last row with provided user data
    """
    print('updating worksheet')
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print('data updated successfully')


def calsulate_surplus_data(sales_row):
    """
    calculated the extra sandwiches made or thrown away.
    """
    print('calculating surplus data')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock,sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data


def main():
    """
    calls all the functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    new_surplus_data = calsulate_surplus_data(sales_data)
    update_sales_worksheet(sales_data)

print('Welcome to love sandwiches data automation')
main()