import os
import RPi.GPIO as GPIO
from datetime import datetime
import time
import serial



from utils.ublox_utils import is_location_in_kml_area, log_gps_event, dmm_to_decimal
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
gps_connection_ok = False
gps_event_filename = "FILE ERROR"
rpi_event_filename  = "FILE ERROR"
UBX_VERSION_QUERY = b'\xb5\x62\x0a\x04\x00\x00\x0e\x34'  # UBX-CFG-POLL for version information

#path to kml file
kml_path = lastest_file("/home/pi/ESO/KMLs/*.kml")

# set connection to GPS
gps = serial.Serial(SERIAL_PORT, baudrate = BAUD_RATE, timeout = 0.5)


# INIT
GPIO.setmode(GPIO.BCM)          # Use GPIO pin number
GPIO.setwarnings(False)         # Ignore warnings in our case
GPIO.setup(LED_PIN_RED, GPIO.OUT)    # GPIO pin as output pin
GPIO.setup(LED_PIN_BLUE, GPIO.OUT)    # GPIO pin as output pin
GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # GPIO pin as output pin

#set all LEDs to Low
GPIO.output(LED_PIN_RED, GPIO.LOW)
GPIO.output(LED_PIN_BLUE, GPIO.LOW)

# Test GPS connection
while True:
    if not gps_connection_ok and gps.is_open:
        log_message("GPS connection is open.")
        gps.write(UBX_VERSION_QUERY)
        time.sleep(0.1)
        response = gps.readlines()  # Read up to 50 bytes of response
        if response:
            gps_connection_ok = True
            log_message(f"GPS is responsive")
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
                log_status(capturing, start_capture, run , stop , error)
            
            if capturing and stop:
                log_message(f"STOP CAPTURING  at {long}, {lat}")
                stop = False
                capturing = False
                os.system("/home/pi/ESO/shell/stop.sh")
                GPIO.output(LED_PIN_RED, GPIO.LOW)
                GPIO.output(LED_PIN_BLUE, GPIO.HIGH)
            
            elif start_capture and not capturing and not stop:
                log_message(f"START CAPTURE at {long}, {lat}")
                capturing = True
                start_capture = False 

                start_time = datetime.now().strftime('%y%m%d_%H%M%S')
                directory = '/home/pi/ESO/Data'
                gps_event_filename = f'{directory}/gpstime_event_log_{start_time}.csv'
                rpi_event_filename = f'{directory}/shutter_event_log_{start_time}.csv'

                if not os.path.exists(directory):
                    os.makedirs(directory)

                os.system(f"/home/pi/ESO/shell/run.sh {rpi_event_filename}")     
                blink(8,LED_PIN_RED, 0.1)
            
            if run:
                GPIO.output(LED_PIN_RED, GPIO.HIGH)
                GPIO.output(LED_PIN_BLUE, GPIO.LOW)
                data = gps.readline()
                if capturing and len(data) > 8 and data[0] == SYNC_1 and data[1] == SYNC_2 and data[2] == CLASS_ID and data[3] == MSG_ID:
                    log_gps_event(data, gps_event_filename)
                
                data = data.decode('latin-1').strip()
                fields = data.split(",")
                if fields[0] == '$GNRMC':
                    try:
                        lat = dmm_to_decimal(fields[3])
                        long = dmm_to_decimal(fields[5])
                    except:
                        lat = "0.0"
                        long = "0.0"
                    if is_location_in_kml_area(lat,long, kml_path): #lat, lon
                        start_capture = not capturing
                    elif capturing:
                        print("-----> OUT OF ZONE")
                        stop = True

    except KeyboardInterrupt:
        print("-----> SHUT DOWN")
        os.system("/home/pi/ESO/shell/stop.sh")
        GPIO.cleanup()

    except Exception as e:
        log_error(e)
        error = True

    if error:
        log_message("ERROR")
        log_status(capturing, start_capture, run , stop , error)

        os.system("/home/pi/ESO/shell/stop.sh")
        GPIO.output(LED_PIN_RED, GPIO.HIGH)
        GPIO.output(LED_PIN_BLUE, GPIO.HIGH)
        time.sleep(5)
        GPIO.output(LED_PIN_RED, GPIO.LOW)
        GPIO.output(LED_PIN_BLUE, GPIO.LOW)
        gps_connection_ok = False
        error = False
