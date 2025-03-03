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
    