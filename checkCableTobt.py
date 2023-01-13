from findImage import findImage
def checkCableTobt():
	if findImage("./images/cableTobt.png"):
		#TODO kabel terug aansluiten
		print("sluit kabel aan")
		#wait for switch back to cable, should be quick
		while(not (findImage("./images/btToCable.png") or findImage("./images/defaultCablebt.png"))):
			pass
		print("bt stuff ok")
		return True
	else:
		return False