import time
import RPi.GPIO as GPIO
import glob
import os
import logging

# Configure the logger
logging.basicConfig(
    filename='LOGs/app.log',               # Specify the log file name
    level=logging.DEBUG,               # Set the logging level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s'  # Define the log message format
)


def blink(n, pin, delay_on, delay_off = None):
    if delay_off is None:
        delay_off = delay_on
    for _ in range(n):
            GPIO.output(pin, GPIO.HIGH)   # Turn on
            time.sleep(delay_on)                         # Pause 1 second
            GPIO.output(pin, GPIO.LOW)    # Turn off
            time.sleep(delay_off)


def input_on(pin):
    if GPIO.input(pin) == GPIO.HIGH:
        return 0
    else:
        start_time = time.time()       
        while GPIO.input(pin) == GPIO.LOW:
            pass  # Do nothing, just wait for release        
        held_time = time.time() - start_time  
    return held_time 

def log_message(message):
    # Write an informational log message
    logging.info(message)

def log_status(capturing, start_capture, run , stop , error):
    message = f"STATES: capturing: {capturing}  | start_capture: {start_capture}  |  run: {run}  |  stop: {stop}  |  error: {error}"
    logging.debug(message)

def log_error(e):
    logging.error(f"Error:{e}")


def lastest_file(path):
    list_of_files = glob.glob(path)
    latest_file = max(list_of_files, key=os.path.getmtime)
    return latest_file