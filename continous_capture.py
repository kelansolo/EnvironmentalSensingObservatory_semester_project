import ptpy
from time import sleep
camera = ptpy.PTPy()
while True:
    sleep(2)
    with camera.session():
        capture = camera.initiate_capture()

    print("capture")