#!/usr/bin/sudo /usr/bin/python3

# Using this article as a reference
# https://www.techwithtim.net/tutorials/voice-assistant/wake-keyword/

#import libraries

import speech_recognition as sr
import re # Regular Expressions

# Platform agnostic TTS using googles library
from gtts import gTTS
from pygame import mixer
mixer.init() # Needs to be initilised only once

# Adding library's for RESPEAKER colours
# The local libaries were originally found on GitHub here:
# They have been modified to use the APA102_pi library instead of a local file https://github.com/tinue/apa102-pi#use-the-apa102-project-as-a-library
import time
from pixels import Pixels, pixels   # Local library needs files in repo
from google_home_led_pattern import GoogleHomeLedPattern # Local library needs files in repo

pixels.pattern = GoogleHomeLedPattern(show=pixels.show) # Initilise patern to be googles

# Google sheets integration imports
import gspread
import datetime
from gspread_formatting import *

# Connecting to googlesheets
gc = gspread.service_account(filename='/home/pi/Calorie-Assistant/calorieassistant-SACred.json')
sh = gc.open('CaloriesSheet') # Open spreadsheet
worksheet = sh.get_worksheet(0) # First Worksheet Dave Calories 

# Seeing what microphones we have available
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print(f"Microphone with name \"{name}\" found for `Microphone(device_index={index})`".format(index, name))

# Create Speaking function
# Updated to be os agnostic
# TODO: See if there are better alternatives, she sounds slow and drunk
def speak(text):
    # Removed buffer so now a tempary file temp.mp3 is created

    # Wrap in try except so it might still work on windows?
    try:
        pixels.speak()
    except:
        print('Pixels Error')

    print(f'Speaking:: {text}')
    
    tts = gTTS(text=text, lang='en')
    filename = 'temp.mp3'
    tts.save(filename)
    mixer.music.load("temp.mp3")
    mixer.music.play()

    # Loops while sound is playing
    while mixer.music.get_busy() == True:
        continue

    # See what it looks like without turning off pixels
    # try:
    #     pixels.off()
    # except:
    #     print('Pixels Error')

try:
    pixels.wakeup()
except:
    print("Pixels error")

speak("Initilising") # test

try:
    pixels.wakeup()
except:
    print("Pixels error")

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

def remove_calories(minus_calories):
    '''
    This function will reduce the total calories stored on sheets if the row exists.
    It will update the spreadsheet if there is already a record with todays date there.
    If the row doesn't exist then create it with negative calories.
    '''

    minus_calories = -minus_calories # Convert positive into negative

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
        total_calories = minus_calories
        values = [today_formatted, total_calories]
        # Adding to the first row that's not full
        worksheet.insert_row(values, index=len(data)+1, value_input_option='USER_ENTERED')

    elif most_recent_date_dt == today:
        # Get current calories from the existing record
        # Add my new calories to the total
        print('Updating existing row')
        current_calories = int(data[-1][1].replace(',','')) # Last row, calories item, parsed from string to int
        total_calories = current_calories + minus_calories
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

def query_calories():
    '''
    #TODO: change add calories logic
    This function will return the the calories stored on sheets if the row exists.
    It will return the number if there is already a record with today's date there.
    If the row doesn't exist then create it with 0 calories.
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
        total_calories = 0
        values = [today_formatted, total_calories]
        # Adding to the first row that's not full
        worksheet.insert_row(values, index=len(data)+1, value_input_option='USER_ENTERED')

    elif most_recent_date_dt == today:
        # Get current calories from the existing record
        print('Reading from existing row')
        current_calories = int(data[-1][1].replace(',','')) # Last row, calories item, parsed from string to int
 
        total_calories=current_calories

    # Inserting any dates turns type into string, thing this will fix this and allow us set all of that column to string
    fmt = cellFormat(
        horizontalAlignment='RIGHT',
        numberFormat=NumberFormat('DATE','yyyy-mm-dd')
        )
    format_cell_range(worksheet, 'A2:A', fmt)    

    return(total_calories)    ## Return this so Barry can say how many calories I have left


def calorie_events(text):
    """
    Function is called when the assistant detects the word 'Calories' in the command.
    """
    if 'add' in text:
        print('Adding calories')
        reg_ex = re.search(r'\d+', text) # search for any digits

        # If digits were found
        if reg_ex:
            calorie_amount = reg_ex.group(0) # If there are multiple numbers then add the first one            
            speak(f'Adding {calorie_amount} calories')            

            # Adding Cloud integration
            cloudCalories = add_calories(int(calorie_amount))
            speak(f'You have {cloudCalories} calories logged')

        # If no digits were found
        else:
            speak('No numbers were said.')
    
    # Reducing calories function
    elif ('minus' in text) or ('take away' in text) or ('takeaway' in text) or ('reduce' in text) or ('remove' in text):
        print('Reducing calories')

        reg_ex = re.search(r'\d+', text) # search for any digits

        # If digits were found
        if reg_ex:
            calorie_amount = reg_ex.group(0) # If there are multiple numbers then add the first one            
            speak(f'Taking away {calorie_amount} calories')

            # Cloud integration
            cloudCalories = remove_calories(int(calorie_amount))
            speak(f'You have {cloudCalories} calories logged')

        # If no digits were found
        else:
            speak('No numbers were said.')    
    
    #TODO: Implement a path asking how many calories you have + how many calories remaining.
    elif ('how many' in text) or ('how much' in text):
        print('Querying how many calories have been stored')
        total_calories = query_calories()
        speak(f'You have {total_calories} calories logged')

    #IDEA: Maybe I should have a feature asking how many more calories you can consume in a day?
    # For example if you have consummed 1800 calories then you have 200 left.

    else:
        speak('Please specify what calorie action you would like to perform')


wake_word = 'barry' # name needs to lowercase!!

while True:
    print("Listening")
    background_speech = get_audio()

    #print(f'I just heard {text}') # for debugging only

    # Wake word detection
    # TODO: See if I can bypass the 'Yo watup' and add calores straight away if calories keyword is detected
    # Add more logic for Adding based on names such as meg or dave
    if wake_word in background_speech:

        try:
            pixels.think()
        except:
            print('Pixels Error')

        print("Wakeword heard")
        speak("Yo watup")
        text = get_audio()

        if 'calorie' in text: # Changed from calories as sometimes the s isnt understood
            calorie_events(text)
            
        else:
            speak("Sorry I didn't catch that")

    try:
        pixels.off()
    except:
        print('Pixels Error')
