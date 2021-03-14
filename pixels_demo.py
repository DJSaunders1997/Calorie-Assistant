import time
from pixels import Pixels, pixels
from alexa_led_pattern import AlexaLedPattern
from google_home_led_pattern import GoogleHomeLedPattern

if __name__ == '__main__':

    pixels.pattern = GoogleHomeLedPattern(show=pixels.show)

    while True:

        try:
            print('Wakekup')
            pixels.wakeup()
            time.sleep(3)
            print('think')
            pixels.think()
            time.sleep(3)
            print('speak')
            pixels.speak()
            time.sleep(6)
            print('off')
            pixels.off()
            time.sleep(3)
        except KeyboardInterrupt:
            break


    pixels.off()
    time.sleep(1)
