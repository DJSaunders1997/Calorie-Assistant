# https://www.kdnuggets.com/2019/09/build-your-first-voice-assistant.html

print("Started script")
global global_calories
global_calories = 200
print('global_calories ', global_calories)
# Imports
import speech_recognition as sr
import os
import sys
import re

# Speech test
from win32com.client import Dispatch
speak = Dispatch("SAPI.SpVoice").Speak

# Method to convert text to speech 
def response(audio):
    print(audio)
    speak(audio)

#For our voice-assistant to perform all the above-discussed features, we have to code the logic of each of them in one method.
#So our first step is to create the method which will interpret user voice response.
def myCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        speak('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....')
        command = myCommand()
    return command



#Now create a loop to continue executing multiple commands. Inside the method assistant() passing user command(myCommand()) as parameters.

def assistant(command):
    "if statements for executing commands"

    if 'exit' in command:
        response('I will now byebye')
        sys.exit()#open website
    
    #Add calories
    elif '' in command:
        reg_ex = re.search(r'\d+', command)

        if reg_ex:
            calories = reg_ex.group(0)
            print('TODO: add calories to global counter')
            #global_calories = global_calories + calories
            #response(f'I have added {calories} calories to your daily amount. You now have had {global_calories} total')
    return global_calories



while True:
    assistant(myCommand())
    #print(global_calories)



# text =f'You just said: {myCommand()}' 
# speak(text)

