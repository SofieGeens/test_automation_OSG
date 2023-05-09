import serial

def relaisCommand(conn,cmd,adr,data):
	conn.write(int(cmd).to_bytes(1,"little"))	#write bitstring of this number to conn in little endian format
	conn.write(int(adr).to_bytes(1,"little"))	#write bitstring of this number to conn in little endian format
	conn.write(int(data).to_bytes(1,"little"))	#write bitstring of this number to conn in little endian format
	xor=cmd^adr									#checksum is xor of all previous numbers
	conn.write(int(xor^data).to_bytes(1,"little"))#write bitstring of this number to conn in little endian format

#for quick testing and setting relais myself if something went wrong
"""
from serial.serialutil import EIGHTBITS
import settings as sets
import time
conn=serial.Serial(port="COM11",baudrate=19200,bytesize=EIGHTBITS,timeout=3)
relaisCommand(conn,1,1,0)
conn.read(100)
relaisCommand(conn,3,3,250)
print(conn.read(4))
conn.read(4)
for i in range(1,sets.cards):
	#print("loop")
	relaisCommand(conn,3,i,255)
	print(conn.read(4))
conn.close()
"""