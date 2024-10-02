#!/usr/bin/env python
import ptpy
# import usb.core
# import usb.backend.libusb0
# import sys

# backend = usb.backend.libusb0.get_backend(find_library=lambda x: "C:/Users/kelan/AppData/Roaming/Python/Python312/site-packages/libusb/_platform/_windows/x64/libusb-1.0.dll")
# dev = usb.core.find(backend=backend)



camera = ptpy.PTPy()
with camera.session():
    capture = camera.initiate_capture()
