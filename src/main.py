''' Main file to execute all micropython codes '''

import _thread
import machine
import utime
import mqtt

# Simple implementation for logging
logfile = 'mainlog.txt'


try:
    _thread.start_new_thread(mqtt.start, ())
except Exception as exc:
    with open(logfile, 'a+') as f:
        print(str(exc))
        f.write(str(exc))
        f.write('\n')
    utime.sleep(5)
    machine.reset()
