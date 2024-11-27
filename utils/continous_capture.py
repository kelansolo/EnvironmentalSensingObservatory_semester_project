import ptpy
from time import sleep
from datetime import datetime

current_time = datetime.now().strftime('%d%m%YT%H%M%S')
dt_camera = datetime.now().strftime('%Y%m%dT%H%M%S.0')

camera = ptpy.PTPy()
with camera.session():
    # Configure the camera
    camera.set_device_prop_value("ExposureProgramMode", 1)  # Mode manual
    camera.set_device_prop_value("ExposureTime", 5)         # 0.5 ms
    camera.set_device_prop_value("FNumber", 560)            # Aperture 1/5.6
    camera.set_device_prop_value("ExposureIndex", 200)      # ISO 200
    camera.set_device_prop_value("FocusMode", 1)            # 1 => Manual mode, 32784 => Auto
    camera.set_device_prop_value("FocusDistance", 65534)    # Distance approx 84m
    camera.set_device_prop_value("CompressionSetting", 1)   # JPEG compression
    camera.set_device_prop_value("DateTime", dt_camera+"+0000")

    # Continuous capture loop
    while True:
        current_camera_time = camera.get_device_prop_value("DateTime")
        print("Current camera time:", current_camera_time)
        capture = camera.initiate_capture()
        sleep(2)
