# Calorie-Assistant
Voice assistant to help track calories throughout the day.


## All Packages and Programs used:


- Respeaker 4mic hat for raspberry pi: https://wiki.seeedstudio.com/ReSpeaker_4_Mic_Array_for_Raspberry_Pi/ .
  Remember to follow the setup steps when first running to set up microphone.
  
- Used this repo to light up hat, but used all seperate code for speech recognition and speech:
  https://github.com/respeaker/4mics_hat
  There code was also modified to use the APA201-pi library rather than relying on local files.

- Text to voice on Windows used TTS engine (Espeak)
   https://www.instructables.com/Make-your-Raspberry-Pi-speak/

- Text to voice on raspberry pi used win32com.client import Dispatch

- Backend Database used is now MongoDB for experience. MongoDB Atlas has a free tier with up to 500MB of storage. Will never fill that so feels like a good solution.

- If there are PyAudio issues on Pi then follow this forum for fixes https://www.raspberrypi.org/forums/viewtopic.php?p=1242333 

Calories from the Pi are also displayed on the related Calorie Website https://github.com/DJSaunders1997/Calorie-Website

Name Ideas:

KoolKcal
CalCounter
kcalKounter

CalTrackR
