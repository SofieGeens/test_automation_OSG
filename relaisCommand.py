import serial

def relaisCommand(conn,cmd,adr,data):
	conn.write(int(cmd).to_bytes(1,"little"))
	conn.write(int(adr).to_bytes(1,"little"))
	conn.write(int(data).to_bytes(1,"little"))
	xor=cmd^adr
	#print(cmd,adr,data,xor^data)
	conn.write(int(xor^data).to_bytes(1,"little"))

"""
from serial.serialutil import EIGHTBITS
import settings as sets
import time
conn=serial.Serial(port="COM13",baudrate=19200,bytesize=EIGHTBITS,timeout=3)
relais = 4
card = sets.cards
relaisCommand(conn,3,sets.cards,250)
conn.read(4)
for i in range(1,sets.cards):
	relaisCommand(conn,3,i,255)
	conn.read(4)
conn.close()
"""