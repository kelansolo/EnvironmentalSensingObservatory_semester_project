#!/bin/bash
echo "--- Starting log and caputre ---"
exec sudo /home/pi/ESO/env/bin/python /home/pi/ESO/utils/continous_log.py "$1"&
exec sudo /home/pi/ESO/env/bin/python /home/pi/ESO/utils/continous_capture.py &