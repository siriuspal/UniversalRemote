Normally MicroPython libraries can be installed using upip and they are saved in lib folder. In my case, umqtt.robust2 had some issues (module import failed) so I "sideloaded" it along side code and modified import statement appropriately.  

The "carrier_freq" keyword argument of RMT function of ESP32 is not implemented in MicroPython version earlier than 1.13.
