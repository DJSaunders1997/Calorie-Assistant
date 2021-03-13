# Testing sheets integration

# https://github.com/burnash/gspread
# https://gspread.readthedocs.io/en/latest/

import gspread
import datetime
from gspread_formatting import *

new_calories = 200

gc = gspread.service_account(filename='calorieassistant-SACred.json')


sh = gc.open('CaloriesSheet') # Open spreadsheet
worksheet = sh.get_worksheet(0) # First Worksheet Dave Calories 

data = worksheet.get('A1:B')

most_recent_date_str = data[-1][0] 
most_recent_date_dt = datetime.datetime.strptime(most_recent_date_str, "%Y-%m-%d").date()

today = datetime.date.today()
today_formatted = today.strftime("%Y-%m-%d")

if most_recent_date_dt < today:
    # then today's date isnt in the spreadsheet
    # Add new row
    print('Adding new row to table')
    values = [today_formatted, new_calories]
    # Adding to the first row that's not full
    worksheet.insert_row(values, index=len(data)+1, value_input_option='USER_ENTERED')

elif most_recent_date_dt == today:
    # Get current calories from the existing record
    # Add my new calories to the total
    print('Updating existing row')
    current_calories = int(data[-1][1].replace(',','')) # Last row, calories item, parsed from string to int
    total_calories = current_calories + new_calories
    values = [today_formatted, total_calories]

    # Add new row over the index of last one
    worksheet.delete_rows(len(data))
    worksheet.insert_row(values, index=len(data), value_input_option='RAW')

# Inserting any dates turns type into string, thing this will fix this and allow us set all of that column to string

fmt = cellFormat(
    horizontalAlignment='RIGHT',
    numberFormat=NumberFormat('DATE','yyyy-mm-dd')
    )

# num_fmt = NumberFormat('DATE')


format_cell_range(worksheet, 'A2:A', fmt)    




