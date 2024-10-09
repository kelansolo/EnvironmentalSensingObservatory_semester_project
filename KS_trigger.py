import ptpy
import time

# Initialize the PTPy camera
camera = ptpy.PTPy()

with camera.session():
    capture = camera.initiate_capture()  # Initiate the capture session
    print("Capture session started. Capturing images every 5 seconds...")

    try:
        while True:
            evt = camera.event()  # Check for events
            if evt:
                print(evt)  # Print the event if any
            
            # Capture an image
            image = camera.capture()  # Capture an image
            print("Image captured: ", image)
            
            time.sleep(5)  # Wait for 5 seconds before capturing the next image

    except KeyboardInterrupt:
        print("Stopping image capture...")