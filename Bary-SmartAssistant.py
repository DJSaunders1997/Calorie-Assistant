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

speak("Testing mic is working") # test

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

        # If no digits were found
        else:
            speak('No numbers were said, so I cant add anything sorry!')    
    
    
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

    






