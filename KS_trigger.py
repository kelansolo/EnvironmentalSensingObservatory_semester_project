#!/usr/bin/env python
import ptpy
from time import sleep
import datetime

def log_event_time(event_time, start_time):
    """Log the event time to a text file."""
    with open(f'shutter_event_log_{start_time}.txt', 'a') as log_file:
        log_file.write(f"{event_time}\n")

camera = ptpy.PTPy()
start = datetime.datetime.now()
while True:
    sleep(2)
    with camera.session():
        capture = camera.initiate_capture()
        bCapture=True
        while bCapture==True:
            evt = camera.event()
            if evt:
                if evt["EventCode"] == "CaptureComplete":
                    capture_time = datetime.datetime.now()
                    log_event_time(capture_time, start)
                    bCapture = False
                    print(evt)


# def main():
#     state = 'INIT'
#     if state = 
    