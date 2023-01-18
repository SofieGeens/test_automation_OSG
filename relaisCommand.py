import serial

def relaisCommand(conn,cmd,adr,data):
	conn.write(int(cmd).to_bytes(1,"little"))
	conn.write(int(adr).to_bytes(1,"little"))
	conn.write(int(data).to_bytes(1,"little"))
	conn.write(int(cmd^adr^data).to_bytes(1,"little"))