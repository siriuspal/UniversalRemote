''' MQTT Module '''

import _thread

import machine
import utime

from robust2 import MQTTClient

import irxm


logfile = 'mqttlog.txt'

pled = machine.Pin(2, machine.Pin.OUT)


def ledblink():
    # This is just simple feedback LED blink for everytime an IR code is sent
    pled.on()
    utime.sleep_ms(100)
    pled.off()


# Change below MQTT Broker IP Address
# I used Mosquitto on Raspbian
mqtt_server = 'MQTT BROKER IP ADDRESS'
client_id = 'esp32remote'

tvcodes = {
    'lgtvpower': [(0x04, 0x08)],
    'yamapower': [(0x7E, 0x2A, 0xD5)],
    'combopower': [(0x04, 0x08), (0x7E, 0x2A, 0xD5)],
    'yamavolp': [(0x7A, 0x1A, 0xE5)],
    'yamavolm': [(0x7A, 0x1B, 0xE4)],
    'lgtvsett': [(0x04, 0x43)],
    'lgtvinstart': [(0x04, 0xFB)],
    'lgtvezadj': [(0x04, 0xFF)],
    'lgtvezpic': [(0x04, 0x4D)],
    'lgtvinputs': [(0x04, 0x0B)],
    'lgtvuparrow': [(0x04, 0x40)],
    'lgtvdownarrow': [(0x04, 0x41)],
    'lgtvleftarrow': [(0x04, 0x07)],
    'lgtvrightarrow': [(0x04, 0x06)],
    'lgtvok': [(0x04, 0x44)],
    'lgtvback': [(0x04, 0x28)],
    'combonetflix': [(0x04, 0x56), (0x7A, 0x03, 0x7C)],
    'comboamazon': [(0x04, 0x5C), (0x7A, 0x03, 0x7C)],
    'lgtvhome': [(0x04, 0x7C)],
    'lgtvstop': [(0x04, 0xB1)],
    'lgtvrewind': [(0x04, 0x8F)],
    'lgtvforward': [(0x04, 0x8E)],
    'lgtvplay': [(0x04, 0xB0)],
    'lgtvpause': [(0x04, 0xBA)],
    'yamabddvd': [(0x7A, 0x00, 0x7F)],
    'yamatv': [(0x7A, 0x03, 0x7C)],
    'yamastraight': [(0x7A, 0x56, 0xA9)],
    'yamaenhancer': [(0x7A, 0x94, 0x6B)],
    'yamabass': [(0x7A, 0xBD, 0xC2)],
    'yamamute': [(0x7A, 0x1C, 0xE3)],
    'yamaprogleft': [(0x7A, 0x59, 0xA6)],
    'yamaprogright': [(0x7A, 0x58, 0xA7)],
    'yamainputup': [(0x7A, 0x1F, 0x60)],
    'yamainputdown': [(0x7A, 0x23, 0x5C)],
    'combochromecast': [(0x04, 0xCC), (0x7A, 0x03, 0x7C)],
    'comboxbox': [(0x04, 0xCE), (0x7A, 0x00, 0x7F)]
}


def sub_cb(topic, msg, _ret, _dup):
    if topic == b'irremote':
        _thread.start_new_thread(ledblink, ())
        code = msg.decode()
        try:
            for c in tvcodes[code]:
                irxm.send_command(*c)
                if len(tvcodes[code]) > 1:
                    utime.sleep(0.5)
        except KeyError:
            pass


def connect_and_subscribe():
    client = MQTTClient(client_id, mqtt_server)
    client.KEEP_QOS0 = False
    client.NO_QUEUE_DUPS = True
    client.MSG_QUEUE_MAX = 2
    client.set_callback(sub_cb)
    if not client.connect(clean_session=False):
        client.subscribe(b'irremote')
    return client


def restart_and_reconnect():
    utime.sleep(5)
    machine.reset()


def start():
    try:
        client = connect_and_subscribe()
    except Exception as exc:
        with open(logfile, 'a+') as f:
            print(str(exc))
            f.write(str(exc))
            f.write('\n')
        restart_and_reconnect()

    while True:
        utime.sleep_ms(50)
        try:
            if client.is_conn_issue():
                while client.is_conn_issue():
                    utime.sleep_ms(50)
                    client.reconnect()
            else:
                client.resubscribe()

            client.check_msg()
            client.send_queue()

        except Exception as exc:
            print(str(exc))
            with open(logfile, 'a+') as f:
                f.write(str(exc))
                f.write('\n')
            restart_and_reconnect()
