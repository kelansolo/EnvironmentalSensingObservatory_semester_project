import serial
from datetime import datetime
import csv


# SERIAL_PORT = "/dev/serial0"
SERIAL_PORT = "/dev/ttyS0"
BAUD_RATE = 38400 

# Constants for TIM-TM2 UBX message
SYNC_1 = 0xB5
SYNC_2 = 0x62
CLASS_ID = 0x0D  # TIM class
MSG_ID = 0x03    # TM2 message

running = True

start_time = datetime.now().strftime('%y%m%d_%H%M%S')
directory = './Data'
filename = f'{directory}/gpstime_event_log_{start_time}.csv'




def decode_tow(tim_tm):
    # Extract the rising edge Time of Week (TOW)
    towR = int.from_bytes(tim_tm[6 + 8:6 + 12], byteorder='little', signed=False)
    return towR/1000



# In the NMEA message, the position gets transmitted as:
# DDMM.MMMMM, where DD denotes the degrees and MM.MMMMM denotes
# the minutes. However, I want to convert this format to the following:
# DD°MM'SS" 
def formatDegreesMinutes(coordinates, digits):

    parts = coordinates.split(".")

    if (len(parts) != 2):
        return coordinates

    if (digits > 3 or digits < 2):
        return coordinates
    
    left = parts[0]
    right = parts[1]
    degrees = str(left[:-2])
    minutes = str(left[-2:])
    seconds = str((float("0."+right[:digits]))*60) # turn minutes into seconds

    return degrees + "°" + minutes + "'" + seconds +"\""

# This method reads the data from the serial port
# and then parses the NMEA messages it transmits.
def getPositionData(data):
    message = data[0:6]
    if (message == b'$GNRMC'):
        parts = data.decode('utf-8').split(",")
        if parts[2] == 'V':
            # V = Warning, most likely, there are no satellites in view...
            print ("GPS receiver warning")
        else:
            longitude = formatDegreesMinutes(parts[5], 3)
            latitude = formatDegreesMinutes(parts[3], 3)
            return latitude, longitude
    else:
        # Handle other NMEA messages and unsupported strings
        pass


print ("Application started!")
gps = serial.Serial(SERIAL_PORT, baudrate = BAUD_RATE, timeout = 0.5)

while running:
    try:
        data = gps.readline()
        if  len(data) > 8 and data[0] == SYNC_1 and data[1] == SYNC_2 and data[2] == CLASS_ID and data[3] == MSG_ID:
            tow = decode_tow(data)
            print(tow)
            with open(filename, 'a', newline='') as log_file:
                writer = csv.writer(log_file)
                writer.writerow(tow)

        else:
            getPositionData(data)
    except KeyboardInterrupt:
        running = False
        gps.close()
        print ("Application closed!")
    except Exception as error:
        print ("Application error:",error)