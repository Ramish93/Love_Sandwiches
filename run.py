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


#def update_sales_worksheet(data):
    """
    updated the google worksheet in last row with provided user data
    """
 #   print('updating sales worksheet')
 #   sales_worksheet = SHEET.worksheet('surplus')
#    sales_worksheet.append_row(data)
#    print('data updated successfully')

def update_worksheet(data, worksheet):
    """
    updated the google worksheet in last row with provided user data
    """
    print(f'updating {worksheet} worksheet')
    update_worksheet = SHEET.worksheet(worksheet)
    update_worksheet.append_row(data)
    print(f'{worksheet} updated successfully')


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

#def update_surplus_worksheet(data):
    #print('updating  surplus worksheet')
    #surplus_worksheet = SHEET.worksheet('surplus')
    #surplus_worksheet.append_row(data)
    #print('data updated successfully')

def get_last_5_sales():
    """
    takes last 5 days of sales and returns the avrage as list of lists.
    """
    sales = SHEET.worksheet('sales')
    columns = []
    for x in range(1 ,7):
        column = sales.col_values(x)
        columns.append(column[-5:])
    return columns

def calculate_stock_data(data):
    """
    calculated avrages of data
    """
    print('calculating stock data...')
    new_stock_data = []

    for column in data:
        int_col = [int(x) for x in column]
        avrage = sum(int_col) / len(int_col)
        stock_num = avrage * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data

def main():
    """
    calls all the functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    new_surplus_data = calsulate_surplus_data(sales_data)
    update_worksheet(sales_data, 'sales')
    update_worksheet(new_surplus_data, 'surplus')
    sales_column = get_last_5_sales()
    stock_data = calculate_stock_data(sales_column)
    update_worksheet(stock_data, 'stock')

print('Welcome to love sandwiches data automation')
main()
