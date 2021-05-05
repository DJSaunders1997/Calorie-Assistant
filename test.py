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

# Create Speaking function
# Updated to be os agnostic
# TODO: See if there are better alternatives, she sounds slow and drunk
def speak(text):
    # Removed buffer so now a tempary file temp.mp3 is created

    print(f'Speaking:: {text}')
    
    tts = gTTS(text=text, lang='en')
    filename = 'temp.mp3'
    tts.save(filename)
    mixer.music.load("temp.mp3")
    mixer.music.play()

speak('Testing Hello')