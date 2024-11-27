#!/usr/bin/env python
import ptpy
from time import sleep
import signal
import sys
import RPi.GPIO as GPIO

BUTTON_GPIO = 23
state = 0

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def button_pressed_callback(channel):
    print(state)
    print("Button pressed!")

if __name__ == '__main__':
    

    if state == 0:
        # GPIO INIT 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=button_pressed_callback, bouncetime=100)

        #  Camera INIT
        # camera = ptpy.PTPy()

        # Cleanup at exit
        signal.signal(signal.SIGINT, signal_handler)
        signal.pause()
        print(state)

        state = 1


    elif state == 1:
        print(state)
        sleep(100)


    # elif state == 10:
    #     with camera.session():
    #         capture = camera.initiate_capture()
    #     sleep(2)



    # camera = ptpy.PTPy()
    # while True:
    #     sleep(2)
    #     with camera.session():
    #         capture = camera.initiate_capture()

def log_event_time(event_time, start_time):
    """Log the event time to a text file."""
    with open(f'shutter_event_log_{start_time}.txt', 'a') as log_file:
        log_file.write(f"{event_time}\n")
