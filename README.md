Project was adapted from this: https://diyprojectslab.com/raspberry-pi-pico-w-web-server/


First, you require to set up MicroPython. Download the UF2 file here that’s especially meant for the Pico W. Hold down the BOOTSEL button and connect your Pico W via USB to your laptop. Once it’s mounted, copy the UF2 file that you just downloaded onto the Pico.
- You can download the Micropython software for the Pico W from here: https://micropython.org/download/RPI_PICO_W/

==========
- Open Thonny IDE and make connect your Pico W with the Micropython interpreter
===============
- To test to make sure the Pico W LED is working... Create a file named "pico_w_LED_test.py" and save it in the root of the Pico. Paste the below code into the file in Thonny and save it: 

```python
import time
from machine import Pin

led = Pin("LED", Pin.OUT)  # Create LED object using the onboard LED

for _ in range(10):  # Repeat the blink cycle 10 times
    led.value(1)  # Set LED to turn on
    time.sleep(1)  # Wait for 1 second
    led.value(0)  # Set LED to turn off
    time.sleep(1)  # Wait for 1 second
```
- Run the above script and the LED should blink

===================
- To test to make sure the Wifi card is working... create a file named network_scan_test.py, and paste the below code into it:
```python
import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

print(wlan.scan())
```
===========

- Create a file named 'wifi_secrets.py' to store your WIFI login credentials and paste the following into it (updating it with your correct information):

```python
wifi_secrets = {
    'ssid': 'WiFiNetwork',
    'Password': 'YourPassword'
    }
```

=============

- Create an index.html page that will be used to toggle on and off the LED when the Pi is connected to the web server: 

```html

<!DOCTYPE html>
<html>
<head>
<style>
.button {
  background-color: #4CAF50; /* Green */
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
}
.button3 {background-color: #f44336;} /* Red */ 
 
</style>
</head>
<body>
<html>
    <head>
       <h1 style="color: red;"><strong>Raspberry Pi Pico W Webserver</strong></h1>
      
    </head>
    <body>
  <h2>Control LED Using Webserver </h2>
   <p><a href="https://www.diyprojectslab.com/introduction-to-raspberry-pi-pico-w/">Getting Started with Raspberry Pi Pico W</a></p>
        <a href=\"?led=on\"><button class="button">ON</button></a>&nbsp;
        <a href=\"?led=off\"><button class="button button3">OFF</button></a> </body>
       <a href="https://www.diyprojectslab.com/introduction-to-raspberry-pi-pico-w"><img class="aligncenter wp-image-4863 size-full" src="https://www.diyprojectslab.com/wp-content/uploads/2022/11/pico-w.jpg" alt="" width="677" height="250" /></a>
</html>
```

=================

Create a file named main.py, which will create the webserver, connect the Pico, and allow you to toggle on and off the LED light: 

```python
import rp2
import network
import ubinascii
import machine
import urequests as requests
import time
from wifi_secrets import wifi_secrets
import socket

# Set country to avoid possible errors
rp2.country('US')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# If you need to disable powersaving mode
# wlan.config(pm=0xa11140)

# See the MAC address in the wireless chip OTP
mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
print('mac = ' + mac)

# Other things to query
# print(wlan.config('channel'))
# print(wlan.config('essid'))
# print(wlan.config('txpower'))

# Load login data from different file for safety reasons
ssid = wifi_secrets['ssid']
pw = wifi_secrets['Password']

wlan.connect(ssid, pw)

# Wait for connection with 10 second timeout
timeout = 20
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    timeout -= 1
    print('Waiting for connection...')
    time.sleep(1)

# Define blinking function for onboard LED to indicate error codes    
def blink_onboard_led(num_blinks):
    led = machine.Pin('LED', machine.Pin.OUT)
    for i in range(num_blinks):
        led.on()
        time.sleep(0.2)
        led.off()
        time.sleep(0.2)

# Handle connection error
# Error meanings
# 0  Link Down
# 1  Link Join
# 2  Link NoIp
# 3  Link Up
# -1 Link Fail
# -2 Link NoNet
# -3 Link BadAuth

wlan_status = wlan.status()
blink_onboard_led(wlan_status)

if wlan_status != 3:
    raise RuntimeError('Wi-Fi connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])

# Function to load in html page    
def get_html(html_name):
    with open(html_name, 'r') as file:
        html = file.read()
        
    return html

# HTTP server with socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening on', addr)
led = machine.Pin('LED', machine.Pin.OUT)

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('Client connected from', addr)
        r = cl.recv(1024)
        # print(r)

        r = str(r)
        led_on = r.find('?led=on')
        led_off = r.find('?led=off')
        print('led_on = ', led_on)
        print('led_off = ', led_off)
        if led_on > -1:
            print('LED ON')
            led.value(1)

        if led_off > -1:
            print('LED OFF')
            led.value(0)

        response = get_html('index.html')
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('Connection closed')

# Make GET request
#request = requests.get('http://www.google.com')
#print(request.content)
#request.close()
```

==========

Run the code