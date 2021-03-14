# Using this article as a reference
# https://www.techwithtim.net/tutorials/voice-assistant/wake-keyword/

#import libraries

import speech_recognition as sr
import re # Regular Expressions
from win32com.client import Dispatch
# Google sheets integration imports
import gspread
import datetime
from gspread_formatting import *

# Connecting to googlesheets
gc = gspread.service_account(filename='calorieassistant-SACred.json')
sh = gc.open('CaloriesSheet') # Open spreadsheet
worksheet = sh.get_worksheet(0) # First Worksheet Dave Calories 

# Seeing what microphones we have available
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"Microphone with name \"{name}\" found for `Microphone(device_index={index})`".format(index, name))

# Create Speaking function
# This is windows only at the moment, will have to change if I deploy on pi
def speak(text):
    print(f'Speaking:: {text}')
    Dispatch("SAPI.SpVoice").Speak(text)

speak("Testing mike is working") # test

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print(f"Exception {str(e)}: All I heard was {said}" )

    return said.lower()


# Adding calories logic

def add_calories(new_calories):
    '''
    This function is used to add rows to the attached google sheets workbook.
    It will update the spreadsheet if there is already a record with todays date there.
    Otherwise it will create a new record with today's date
    '''

    # First need to get data as it could have changed inside of the loop
    data = worksheet.get('A1:B')    # Get all data ignoring the headers

    most_recent_date_str = data[-1][0] # Get lasts item from list / most recent record. First index which is date 
    most_recent_date_dt = datetime.datetime.strptime(most_recent_date_str, "%Y-%m-%d").date()

    today = datetime.date.today()
    today_formatted = today.strftime("%Y-%m-%d")

    if most_recent_date_dt < today:
        # then today's date isnt in the spreadsheet
        # Add new row
        print('Adding new row to table')
        total_calories = new_calories
        values = [today_formatted, total_calories]
        # Adding to the first row that's not full
        worksheet.insert_row(values, index=len(data)+1, value_input_option='USER_ENTERED')

    elif most_recent_date_dt == today:
        # Get current calories from the existing record
        # Add my new calories to the total
        print('Updating existing row')
        current_calories = int(data[-1][1].replace(',','')) # Last row, calories item, parsed from string to int
        total_calories = current_calories + new_calories
        values = [today_formatted, total_calories]
        # Delete existing and add new row over
        worksheet.delete_rows(len(data))
        worksheet.insert_row(values, index=len(data), value_input_option='RAW')

    # Inserting any dates turns type into string, thing this will fix this and allow us set all of that column to string
    fmt = cellFormat(
        horizontalAlignment='RIGHT',
        numberFormat=NumberFormat('DATE','yyyy-mm-dd')
        )
    format_cell_range(worksheet, 'A2:A', fmt)    

    return(total_calories)    ## Return this so Barry can say how many calories I have left

def calorie_events(text, total_calories):
    if 'add' in text:
        print('Adding calories')

        reg_ex = re.search(r'\d+', text) # search for any digits

        # If digits were found
        if reg_ex:
            calorie_amount = reg_ex.group(0) # If there are multiple numbers then add the first one
            
            speak(f'Adding {calorie_amount} to your daily total')
            total_calories = total_calories + int(calorie_amount)
            speak(f'Total calorie consumed is now {total_calories}')

            # Adding Cloud integration
            cloudCalories = add_calories(int(calorie_amount))
            speak(f'On Google Sheets you have {cloudCalories} calories logged')

        # If no digits were found
        else:
            speak('No numbers were said, so I cant add anything sorry!')
    
    # Reducing calories function
    elif ('minus' in text) or ('take away' in text) or ('reduce' in text):
        print('Reducing calories')

        reg_ex = re.search(r'\d+', text) # search for any digits

        # If digits were found
        if reg_ex:
            calorie_amount = reg_ex.group(0) # If there are multiple numbers then add the first one
            
            speak(f'Taking away {calorie_amount} from your daily total')
            total_calories = total_calories - int(calorie_amount)
            speak(f'Total calorie consumed is now {total_calories}')

            #TODO function to remove calories from sheets

        # If no digits were found
        else:
            speak('No numbers were said, so I cant add anything sorry!')    
    
    #TODO: Implement a asking how many calories you have + how many calories remaining.


    else:
        speak('Please specify what calorie action you would like to perform')

    return total_calories   # Need to return so next runthough will be able to know calories



wake_word = 'barry' # name needs to lowercase!!


# initilise calories outside of loop so it should increase
total_calories = 0


while True:
    print("Listening")
    background_speech = get_audio()

    #print(f'I just heard {text}') # for debugging only

    # Wake word detection
    # TODO: See if I can bypass the 'Yo watup' and add calores straight away if calories keyword is detected
    # Add more logic for Adding based on names such as meg or dave
    if wake_word in background_speech:
        print("Wakeword heard")
        speak("Yo watup")
        text = get_audio()

        if 'calories' in text:
            total_calories = calorie_events(text, total_calories)
            
        else:
            speak('You didnt say any phrases I can respond to yet. Sorry!')

    






