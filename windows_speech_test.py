# Speech test

from win32com.client import Dispatch

speak = Dispatch("SAPI.SpVoice").Speak

speak("Boo lets go for a walk")