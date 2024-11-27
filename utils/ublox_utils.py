
import csv

def decode_tow(tim_tm):
    # Extract the rising edge Time of Week (TOW)
    towR = int.from_bytes(tim_tm[6 + 8:6 + 12], byteorder='little', signed=False)
    return towR/1000

def in_box():
    return True

def log_gps_event(data, filename):
    tow = decode_tow(data)
    with open(filename, 'a', newline='') as log_file:
        writer = csv.writer(log_file)
        writer.writerow(tow)