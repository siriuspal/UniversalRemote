# UniversalRemote
## Universal IR Remote developed using ESP32, MicroPython, and MQTT

### Background:
I have a LG TV and Yamaha Home Theatre System. I was tired of using two remotes by my side and all universal remotes with macro options were expensive. So I designed an IR Remote which allowed me to use a mobile as a universal remote. The code in this repository is just my specific implementation, however it's easy to expand to any number of remotes and any custom macro.

To capture the required IR Codes, I used generic IR receiver and captured signals on a USB oscilloscope. I decoded the protocol (IR NEC) using PulseView SigRok https://sigrok.org/wiki/PulseView 

IR NEC protocol is described here in detail: https://techdocs.altium.com/display/FPGA/NEC+Infrared+Transmission+Protocol
There are many sources over Internet for IR remote codes - e.g. for LG TV https://gitlab.com/snippets/1690600
For above resource, the format of code was different than what I captured directly using PulseView, so I wrote a helper script to convert format.

### Setup:
#### Hardware:
Generic ESP-WROOM-32 Development Board with USB port
Generic IR LED
MOSFET, Resistor, Wires
USB Cable
5V USB Power Supply
#### Enclosure:
Custom 3D Printed Enclosure designed using OnShape
#### Software:
MicroPython ver 1.13 (esp32-idf3-20200902-v1.13.bin) https://micropython.org/download/esp32/
umqtt.robust2 (and umqtt.simple2) https://github.com/fizista/micropython-umqtt.robust2
#### Other:
Raspberry Pi as MQTT Broker
MQTT Dashboard as Remote https://play.google.com/store/apps/details?id=com.app.vetru.mqttdashboard&hl=en_IN&gl=US
Wi-Fi Router
