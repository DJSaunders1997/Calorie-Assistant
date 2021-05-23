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

# New using for wakeword detection.
# https://pimylifeup.com/raspberry-pi-porcupine/

import struct
import pyaudio
import pvporcupine

porcupine = None
pa = None
audio_stream = None

porcupine = pvporcupine.create(keywords=["picovoice", "blueberry"])

pa = pyaudio.PyAudio()

audio_stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length)

# Replace GoogleSheets imports with Custom MongoDB Module
# Current date from datetime module needed when using module 
import DBConModule
import datetime


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
    try:
        pixels.off()
    except:
        print('Pixels Error')

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

def calorie_events(text):
    """
    Function is called when the assistant detects the word 'Calories' in the command.
    Looks whether to add calories for Megan, but will add calories to Dave by default.
    """

    # Update datetime so that it will still be up to date for multiple days without restarting script
    today = datetime.datetime.today()

    if ('megan' in text) or ('meg' in text):
        person = 'Meg'
    else:
        person = 'Dave'

    if ('how many' in text) or ('how much' in text):
        print('Querying how many calories have been stored')
        total_calories = DBConModule.get_daily_total(person, today)
        speak(f'{person} has {total_calories} calories logged')

    elif ('add' in text) or ('ad' in text) or ('at' in text):
        print('Adding calories')

        reg_ex = re.search(r'\d+', text) # search for any digits

        # If digits were found
        if reg_ex:
            calorie_amount = reg_ex.group(0) # If there are multiple numbers then add the first one            
            speak(f'Adding {calorie_amount} calories')            

            # Cloud integration
            DBConModule.add_calories(person, today, int(calorie_amount))
            total_calories = DBConModule.get_daily_total(person, today)

            speak(f'{person} has {total_calories} calories logged')

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

            # Adding Cloud integration
            DBConModule.add_calories(person, today, -int(calorie_amount))
            total_calories = DBConModule.get_daily_total(person, today)

            speak(f'{person} has {total_calories} calories logged')

        # If no digits were found
        else:
            speak('No numbers were said.')    
    

    #IDEA: Maybe I should have a feature asking how many more calories you can consume in a day?
    # For example if you have consummed 1800 calories then you have 200 left.

    else:
        speak('Please specify what calorie action you would like to perform')


wake_word = 'barry' # name needs to lowercase!!

print("About to enter main loop")
speak("Listening")

while True:
    #print("Listening")
    pcm = audio_stream.read(porcupine.frame_length)
    pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

    keyword_index = porcupine.process(pcm)

    if keyword_index >= 0:
        print("Hotword Detected")

        try:
            pixels.think()
        except:
            print('Pixels Error')

        # text = get_audio()

        # print("text is", text)

        # #try again if text is nothing
        # if text == '':
        #     speak("Yo")
        #     text = get_audio()

        speak("Yo")
        text = get_audio()

        calorie_events(text)

        try:
            pixels.off()
        except:
            print('Pixels Error')
