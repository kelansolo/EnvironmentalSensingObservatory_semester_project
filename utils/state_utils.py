import time
import RPi.GPIO as GPIO

def blink(n, pin, delay_on, delay_off = None):
    if delay_off is None:
        delay_off = delay_on
    for _ in range(n):
            GPIO.output(pin, GPIO.HIGH)   # Turn on
            time.sleep(delay_on)                         # Pause 1 second
            GPIO.output(pin, GPIO.LOW)    # Turn off
            time.sleep(delay_off)


def input_on(pin):
    if GPIO.input(pin) == GPIO.HIGH:
        return 0
    else:
        start_time = time.time()       
        while GPIO.input(pin) == GPIO.LOW:
            pass  # Do nothing, just wait for release        
        held_time = time.time() - start_time  
    return held_time 

def next_state(new_state):
    print("state -> {}".format(new_state))
    return new_state