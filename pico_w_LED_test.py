import time
from machine import Pin

led = Pin("LED", Pin.OUT)  # Create LED object using the onboard LED

for _ in range(10):  # Repeat the blink cycle 10 times
    led.value(1)  # Set LED to turn on
    time.sleep(1)  # Wait for 1 second
    led.value(0)  # Set LED to turn off
    time.sleep(1)  # Wait for 1 second
    