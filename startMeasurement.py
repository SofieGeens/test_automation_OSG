import pyautogui as pag
from clickButton import clickButton

def startMeasurement():
	#start new measurement with keyboard shortcuts
	pag.keyDown("alt")
	pag.keyDown("b")
	pag.keyUp("alt")
	pag.keyUp("b")
	pag.press("n")
	pag.write("test")
	pag.press("enter")
	pag.press("enter")
	while not clickButton("./images/starten.png"):
		pass
	startrec = False
	#start the recorcing
	for i in range(sets.maxWait):						#wait for this button to appear, then click it
		if clickButtonPrecise("./images/record.png"):
			startrec = True
			break
		time.sleep(1)
	#exit out of program if recorder could not be found
	if not startrec:
		print("de recorder kon niet gevonden worden")
		exit()
	pag.move(500,500) #move the mouse out of the way so that no hover pop up apears