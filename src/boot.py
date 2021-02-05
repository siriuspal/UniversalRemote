''' Execute at Every Boot '''
# This file is executed on every boot (including wake-boot from deepsleep)

import gc
import utime

import webrepl
import network

import machine


gc.enable()

ap = network.WLAN(network.AP_IF)
ap.active(False)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

try:
    while not wlan.isconnected():
        # Update Wi-Fi SSID and Password here
        wlan.connect('SSID', 'PASSWORD')
        utime.sleep(1)
except Exception as exc:
    utime.sleep(5)
    machine.reset()

try:
    webrepl.start()
except Exception:
    pass
