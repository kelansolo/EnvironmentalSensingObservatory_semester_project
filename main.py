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

LED_PIN_BLUE = 23
LED_PIN_RED = 22
INPUT_PIN = 24

capturing = False
start_capture = False
run = False
stop = False
error = False
gps_event_filename = "FILE ERROR"
rpi_event_filename  = "FILE ERROR"
UBX_VERSION_QUERY = b'\xb5\x62\x0a\x04\x00\x00\x0e\x34'  # UBX-CFG-POLL for version information

kml_path = "./map.geo.admin.ch_KML_20241211161754.kml"

gps = serial.Serial(SERIAL_PORT, baudrate = BAUD_RATE, timeout = 0.5)


# INIT
GPIO.setmode(GPIO.BCM)          # Use GPIO pin number
GPIO.setwarnings(False)         # Ignore warnings in our case
GPIO.setup(LED_PIN_RED, GPIO.OUT)    # GPIO pin as output pin
GPIO.setup(LED_PIN_BLUE, GPIO.OUT)    # GPIO pin as output pin
GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # GPIO pin as output pin

GPIO.output(LED_PIN_RED, GPIO.LOW)
GPIO.output(LED_PIN_BLUE, GPIO.LOW)

# Test GPS
if gps.is_open:
    print("GPS connection is open.")
    gps.write(UBX_VERSION_QUERY)
    time.sleep(0.1)
    response = gps.read(50)  # Read up to 50 bytes of response
    blink(8,LED_PIN_BLUE,0.1)
    if response:
        print(f"GPS is responsive")
        blink(8, LED_PIN_BLUE, 0.1)
    else:
        print("No response from GPS. It may be unplugged or unresponsive.")
        error = True
else:
    print("GPS connection failed to open.")
    error = True

GPIO.output(LED_PIN_BLUE, GPIO.HIGH)

try:
    while not error:
        if input_on(INPUT_PIN) > 0.2: # debounce
            stop = run
            run = not run
        
        if capturing and stop:
            print("-----> STOP CAPTURING ")
            stop = False
            capturing = False
            os.system("/home/pi/ESO/shell/stop.sh")
            GPIO.output(LED_PIN_RED, GPIO.LOW)
            GPIO.output(LED_PIN_BLUE, GPIO.HIGH)
        
        elif start_capture and not capturing and not stop:
            print("-----> START CAPTURE")
            capturing = True
            start_capture = False 

            start_time = datetime.now().strftime('%y%m%d_%H%M%S')
            directory = '/home/pi/ESO/Data'
            gps_event_filename = f'{directory}/gpstime_event_log_{start_time}.csv'
            rpi_event_filename = f'{directory}/shutter_event_log_{start_time}.csv'

            if not os.path.exists(directory):
                os.makedirs(directory)

            os.system(f"/home/pi/ESO/shell/run.sh {rpi_event_filename}")     
            GPIO.output(LED_PIN_RED, GPIO.HIGH)
            GPIO.output(LED_PIN_BLUE, GPIO.LOW)
        
        if run:
            data = gps.readline()
            if capturing and len(data) > 8 and data[0] == SYNC_1 and data[1] == SYNC_2 and data[2] == CLASS_ID and data[3] == MSG_ID:
                log_gps_event(data, gps_event_filename)
            
            # data = data.decode('ascii').strip()
            # fields = data.split(",")
            if in_box(): #TODO Implement function!!
            # if fields[0] == '$GNRMC' and is_location_in_kml_area(float(fieds[3])/100, float(fieds[5])/100, kml_path): #lat, lon
                start_capture = not capturing
            else:
                stop = True

except KeyboardInterrupt:
    print("-----> SHUT DOWN")
    os.system("/home/pi/ESO/shell/stop.sh")
    GPIO.cleanup()

except:
    error = True
    os.system("/home/pi/ESO/shell/stop.sh")
    GPIO.output(LED_PIN_RED, GPIO.LOW)

if error:
    GPIO.output(LED_PIN_RED, GPIO.HIGH)
    GPIO.output(LED_PIN_BLUE, GPIO.HIGH)
