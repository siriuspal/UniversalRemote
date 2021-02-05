A simple schematics for directly driving IR LED.  

In my setup the ESP32 board is placed under TV and home theatre and facing away from these units. Meaning the IR light bounces off the opposite wall or furniture and controls the equipment.  
The LED is powered directly with 5V without any resistor. Since RMT waveform is modulated with 38,222 Hz signal, the pulses are short duration.  
