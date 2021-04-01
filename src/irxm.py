''' Module to Transmit IR Signals '''
# This module generates sequence needed for IR NEC format

from machine import Pin
from esp32 import RMT


def add_leadpulse(lst):
    ''' Add lead pulse and space '''
    pulse = 30000
    space = 15000
    lst.extend([pulse, space])
    return lst


def add_endpulse(lst):
    ''' Add lead pulse and space '''
    pulse = 1875
    lst.append(pulse)
    return lst


def add_zero(lst):
    ''' Add pulses for logical zero '''
    pulse = 1875
    space = 1875
    lst.extend([pulse, space])
    return lst


def add_one(lst):
    ''' Add pulses for logical one '''
    pulse = 1875
    space = 5625
    lst.extend([pulse, space])
    return lst


def send_byte(byt, lst):
    ''' Manipulates a byte to be sent '''
    for _i in range(8):
        if byt & 0x01:
            add_one(lst)
        else:
            add_zero(lst)
        byt = byt >> 1


def send_command(add, com, comn=None):
    ''' Sends command on IR input is address and command '''
    # RMT(channel=0, pin=4, source_freq=80000000, clock_div=24, carrier_freq=38222, carrier_duty_percent=50)
    remote = RMT(0, pin=Pin(4), clock_div=24, carrier_freq=38222)

    lst = list()
    add_leadpulse(lst)

    send_byte(add, lst)
    send_byte(~add, lst)
    send_byte(com, lst)
    
    
    # I identified some keys on Yamaha remote did not send exact invert of command, instead some bits were peculiar.
    # This deviated from NEC protocol, but work around was simple.
    # If peculiar code is present that's sent, otherwise inverted code is sent.
    if comn is None:
        send_byte(~com, lst)
    else:
        send_byte(comn, lst)

    add_endpulse(lst)

    remote.write_pulses(lst, start=1)
    remote.wait_done()
    del lst
    # Without deinit and reinitializing remote after every use, second use of remote will hang it.
    # This issue may have been resolved in MicroPython 1.13 or later. Not tested.
    # However using below command is a workaround that works :)
    remote.deinit()
