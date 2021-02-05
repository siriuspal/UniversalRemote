''' File converts remote code from internet to captured code '''
# Source for internet LG Codes
# https://gitlab.com/snippets/1690600


# Example:
# InStart internet code is 20DFDF20, required output is 04FB
# EZAdj internet code is 20DFFF00, required output is 04FF

import numpy as np


intcode = 0x20DF33CC

firstbyte = 0xFF000000 & intcode
firstbyte = np.uint8(firstbyte >> 24)

addbits = 10 - len(bin(firstbyte))

appn = str()
for i in range(addbits):
    appn = appn + '0'

fbytes = appn + bin(firstbyte)[2:]
revfbytes = fbytes[::-1]

firstcode = hex(int(revfbytes, base=2))
print('first code is:', firstcode)


secbyte = 0x0000FF00 & intcode
secbyte = np.uint8(secbyte >> 8)

addbits = 10 - len(bin(secbyte))

appn = ''
for i in range(addbits):
    appn = appn + '0'

fbytes = appn + bin(secbyte)[2:]
revfbytes = fbytes[::-1]

seccode = hex(int(revfbytes, base=2))
print('last code is:', seccode)
