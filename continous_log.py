import signal
import sys
import RPi.GPIO as GPIO
from datetime import datetime


# BUTTON_GPIO = 23
BUTTON_GPIO = 23

start_time = datetime.now().strftime('%y%m%d_%H%M%S')

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def button_pressed_callback(channel):
    event_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    with open(f'shutter_event_log_{start_time}.txt', 'a') as log_file:
        log_file.write(f"{event_time}\n")

if __name__ == '__main__':
    
    try: 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=button_pressed_callback, bouncetime=100)
        signal.signal(signal.SIGINT, signal_handler)
        signal.pause()
    
    except KeyboardInterrupt:
        print("keboard int")
    
    finally:
        GPIO.cleanup()
