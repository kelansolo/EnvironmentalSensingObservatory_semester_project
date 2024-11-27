import os
import RPi.GPIO as GPIO
from datetime import datetime
import time
import serial
import csv

from utils.ublox_utils import *
from utils.state_utils import * 

SERIAL_PORT = "/dev/ttyS0"
BAUD_RATE = 38400 

# Constants for TIM-TM2 UBX message
SYNC_1 = 0xB5
SYNC_2 = 0x62
CLASS_ID = 0x0D  # TIM class
MSG_ID = 0x03    # TM2 message

LED_PIN = 4
INPUT_PIN = 24

capturing = False
start_capture = False
run = False
stop = False
gps_event_filename = "FILE ERROR"
rpi_event_filename  = "FILE ERROR"

# state = 0
gps = serial.Serial(SERIAL_PORT, baudrate = BAUD_RATE, timeout = 0.5)

# INIT
GPIO.setmode(GPIO.BCM)          # Use GPIO pin number
GPIO.setwarnings(False)         # Ignore warnings in our case
GPIO.setup(LED_PIN, GPIO.OUT)    # GPIO pin as output pin
GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # GPIO pin as output pin


while True:
    if input_on(INPUT_PIN) > 0.2: # debounce
        stop = run
        run = not run
    
    if capturing and stop:
        print("-----> STOP CAPTURING ")
        stop = False
        capturing = False
        os.system("/home/pi/ESO/shell/stop.sh")
    
    elif start_capture and not capturing and not stop:
        print("-----> START CAPTURE")
        capturing = True
        start_capture = False 

        start_time = datetime.now().strftime('%y%m%d_%H%M%S')
        directory = './Data'
        gps_event_filename = f'{directory}/gpstime_event_log_{start_time}.csv'
        rpi_event_filename = f'{directory}/shutter_event_log_{start_time}.csv'

        if not os.path.exists(directory):
            os.makedirs(directory)

        os.system(f"/home/pi/ESO/shell/run.sh {rpi_event_filename}")     
    
    if run:
        data = gps.readline()
        if capturing and len(data) > 8 and data[0] == SYNC_1 and data[1] == SYNC_2 and data[2] == CLASS_ID and data[3] == MSG_ID:
            log_gps_event(data, gps_event_filename)
        elif in_box:
            start_capture = not capturing
        else:
            stop = True
        


            











try:
    while True:
        if state == 0: # init
            print("state: 0")
            blink(8,LED_PIN,0.1)
            os.system("/home/pi/ESO/shell/stop.sh")
            state = next_state(1)
            print("-----> WAITING FOR INPUT")

        elif state == 1: # Wait for input
            if GPIO.input(INPUT_PIN) == GPIO.LOW:
                if detect_button_release(INPUT_PIN):
                    start_time = datetime.now().strftime('%y%m%d_%H%M%S')
                    directory = './Data'
                    gps_filename = f'{directory}/gpstime_event_log_{start_time}.csv'
                    rpi_event_filename = f'{directory}/shutter_event_log_{start_time}.csv'

                    if not os.path.exists(directory):
                        os.makedirs(directory)

                    state = next_state(10)
        
        elif state == 10: # get data
            data = gps.readline()
            if capturing == True:
                state = next_state(20)
            else:
                state = next_state(30) #TODO add capturning condition
            

        elif state == 20: # log event
            if  len(data) > 8 and data[0] == SYNC_1 and data[1] == SYNC_2 and data[2] == CLASS_ID and data[3] == MSG_ID:
                tow = decode_tow(data)
                with open(gps_filename, 'a', newline='') as log_file:
                    writer = csv.writer(log_file)
                    writer.writerow(tow)
            
            if GPIO.input(INPUT_PIN) == GPIO.LOW:
                if detect_button_release(INPUT_PIN):
                    state = next_state(90)
            

        elif state == 30:
            os.system(f"/home/pi/ESO/shell/run.sh {rpi_event_filename}")
            # start_capture = True
            state = next_state(10)
            print("-----> CAPTURING ")

        elif state == 3:
            blink(1,LED_PIN,0.05)
            for _ in range(20):
                if GPIO.input(INPUT_PIN) == GPIO.LOW:
                    if detect_button_release(INPUT_PIN):
                        state = next_state(90)
                else:
                    time.sleep(0.1)

        elif state == 90:
            print("-----> STOP CAPTURING ")
            os.system("/home/pi/ESO/shell/stop.sh")
            state = next_state(0)

except KeyboardInterrupt:
    os.system("/home/pi/ESO/shell/stop.sh")
    print("Program interrupted.")
finally:
    GPIO.cleanup()  # Ensures that GPIO pins are reset
