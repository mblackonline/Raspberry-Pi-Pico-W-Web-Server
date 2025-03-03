# Raspberry Pi Pico W Web Server Project

This project, inspired by the [DIY Projects Lab writeup](https://diyprojectslab.com/raspberry-pi-pico-w-web-server/), enables you to set up a web server on the Raspberry Pi Pico W, allowing you to control the onboard LED via a web interface.

A special thanks to [DIY Project Lab](https://diyprojectslab.com/) for their excellent guide, which helped me learn more about working with the Pico W.

## Prerequisites

1. Set up MicroPython:
   - Download the UF2 file for Pico W: [MicroPython for Pico W](https://micropython.org/download/RPI_PICO_W/)
   - Hold down the BOOTSEL button and connect your Pico W via USB to your computer. Once mounted, copy the UF2 file to the Pico.

2. Download and install the [Thonny IDE](https://thonny.org/), then open Thonny and connect your Pico W with the MicroPython interpreter.

## Testing the LED

1. Create a file named `pico_w_LED_test.py` and save it to the root of the Pico. Paste the following code into the file:

    ```python
    import time
    from machine import Pin

    led = Pin("LED", Pin.OUT)

    for _ in range(10):
        led.value(1)
        time.sleep(1)
        led.value(0)
        time.sleep(1)
    ```

2. Run the script in Thonny; the LED should blink.

## Testing the WiFi

1. Create a file named `network_scan_test.py` and paste the following code into it:

    ```python
    import network
    import time

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # Scan for networks
    scan_duration = 10  # in seconds
    interval = 5  # in seconds
    end_time = time.time() + scan_duration

    while time.time() < end_time:
        networks = wlan.scan()
        print("Networks found:", networks)
        time.sleep(interval)
    ```

## Storing WiFi Credentials

1. Create a file named `wifi_secrets.py` to store your WiFi login credentials. Paste the following code into it, updating it with your credentials:

    ```python
    wifi_secrets = {
        'ssid': 'WiFiNetwork',
        'Password': 'YourPassword'
    }
    ```

## Creating the Web Interface

1. Create an `index.html` file to toggle the LED on and off:

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Raspberry Pi Pico W (version 1)</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <main>
            <article>
                <h1 style="color: black;"><strong>Raspberry Pi Pico W Webserver</strong></h1>
                <h2>Control LED Using Webserver</h2>
                <p><a href="https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html#picow-technical-specification">Raspberry Pi Pico W Documentation</a></p>
                <a href="?led=on"><button class="button">Click to Turn LED On</button></a>&nbsp;
                <a href="?led=off"><button class="button button3">Click to Turn LED Off</button></a>
            </article>
        </main>
    </body>
    </html>
    ```

## Running the Web Server

1. Create a `main.py` file to set up the web server and control the LED:

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

    # See the MAC address in the wireless chip OTP
    mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
    print('mac = ' + mac)

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
    ```

2. **Run the code in Thonny**:
   - Connect your Pico W to your computer and open Thonny.
   - Load the `main.py` file in Thonny.
   - Click the green "Run" button or press F5 to execute the script. This will start the web server.
   - Navigate to the IP address shown in the Thonny terminal output to control the LED via the web. 


   ## Acknowledgment

This README was created with the assistance of AI.
