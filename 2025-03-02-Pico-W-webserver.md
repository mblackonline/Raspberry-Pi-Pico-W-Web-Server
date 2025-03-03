# Pico W Web Server - (a fun weekend project)

I've been wanting to learn more about working with the Raspberry Pi Pico, and came across some great projects on the [DIY Projects Lab website](https://diyprojectslab.com/). One of the projects that caught my eye was the "[Raspberry Pi Pico W Web Server project](https://diyprojectslab.com/raspberry-pi-pico-w-web-server/)." This aligned well with my desire to learn more about using the Pico as a simple web server, as I've been thinking about trying to create a cat feeder project that this would be useful for.  

Below, I will provide my tweaks to the project (adapted from the DIY Projects Lab website). 

## What You Need

*   Raspberry Pi Pico W
*   MicroPython
*   Thonny IDE
*   Basic Micropython/HTML knowledge

## Web Server Setup

1.  Install MicroPython: Download the UF2 file from the [MicroPython website](https://micropython.org/download/RPI_PICO_W/). Hold the BOOTSEL button on your Pico W and connect it to your computer. Copy the UF2 file to the Pico W.
2.  Install Thonny IDE: Download and install Thonny from [thonny.org](https://thonny.org/).
3.  Connect to Pico W: In Thonny, go to "Tools" -> "Options" -> "Interpreter" and select "MicroPython (Raspberry Pi Pico)".
4.  Create `wifi_secrets.py`: Create a file named `wifi_secrets.py` with your Wi-Fi credentials.
5.  Create `index.html`: Create a file named `index.html`.
6.  Create `style.css`: Create a file named `style.css`.
7.  Create `main.py`: Create a file named `main.py`.
8.  Upload Files: Upload all files (`wifi_secrets.py`, `index.html`, `style.css`, `main.py`) to your Pico W.

## My Changes

*   Refactored the index.html page and moved the CSS styles to `style.css`.
*   Documentation Link: Updated to the official [Raspberry Pi Pico W Documentation](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html#picow-technical-specification).

You can find the code for this project on my [GitHub](https://github.com/yourgithubusername/pico-w-web-server).

## Credit

- Thanks to DIY Projects Lab: [Raspberry Pi Pico W Web Server](https://diyprojectslab.com/raspberry-pi-pico-w-web-server/) for their documentation to help me learn more about the Pi Pico W. 

- And thanks to the Raspberry Pi Foundation for their documentation.