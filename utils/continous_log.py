import signal
import sys
import RPi.GPIO as GPIO
import csv
from datetime import datetime
import argparse


parser = argparse.ArgumentParser(
                    prog='EventLog',
                    description='Continously log the computertime of all the camera event pulses',
                    epilog='---')

parser.add_argument('output_dir', type=str)
args = parser.parse_args()
event_filename = args.output_dir

BUTTON_GPIO = 23

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def button_pressed_callback(channel):
    global event_filename
    event_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    with open(event_filename, 'a', newline='') as log_file:
        writer = csv.writer(log_file)
        writer.writerow([event_time])

if __name__ == '__main__':
    
    try: 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=button_pressed_callback, bouncetime=100)
        signal.signal(signal.SIGINT, signal_handler)
        signal.pause()
    
    except KeyboardInterrupt:
        GPIO.cleanup()
    
    finally:
        GPIO.cleanup()
