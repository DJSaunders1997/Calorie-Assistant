# Calorie-Assistant
Voice assistant to help track calories throughout the day


## All Packages and Programs used:


- Respeaker 4mic hat for raspberry pi: https://wiki.seeedstudio.com/ReSpeaker_4_Mic_Array_for_Raspberry_Pi/
 Used their repo to light up hat, but used all seperate code for speech recognition and speech.
 https://github.com/respeaker/4mics_hat
 There code was also modified to use the APA201-pi library rather than relying on local files.

- Text to voice on Windows used TTS engine (Espeak)
   https://www.instructables.com/Make-your-Raspberry-Pi-speak/

- Text to voice on raspberry pi used win32com.client import Dispatch

- Google sheets with Python integration to store calories over time.
  Link to speadsheet https://docs.google.com/spreadsheets/d/1bQCi2DsnIFFSZZ9wHnXBtvhaKgvmp9mG3t918Gwz39o/edit#gid=0 .
  Linked using the gspread library # https://github.com/burnash/gspread , https://gspread.readthedocs.io/en/latest/

- If there are PyAudio issues on Pi then follow this forum for fixes https://www.raspberrypi.org/forums/viewtopic.php?p=1242333 

Name Ideas:

KoolKcal
CalCounter
kcalKounter

CalTrackR
