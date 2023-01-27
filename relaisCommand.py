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
for i in range(len(sets.x1)):
	#print("off:",card,relais)
	relaisCommand(conn,7,card,relais)
	print(conn.read(4))
	relais *= 2
	if relais > 128:
		relais = 1
		card += 1
		if card==sets.cards+1:
			card = 1
	#print("on:",card,relais)
	relaisCommand(conn,6,card,relais)
	print(conn.read(4))
	time.sleep(1)
conn.close()
"""