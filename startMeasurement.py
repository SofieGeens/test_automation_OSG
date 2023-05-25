import pyautogui as pag
from clickButton import clickButton, clickButtonPrecise
import time
import settings as sets

def startMeasurement():
	#start new measurement with keyboard shortcuts
	pag.click(500,500)		#make sure BrainRT is the active window
	pag.keyDown("alt")
	pag.keyDown("b")
	pag.keyUp("alt")
	pag.keyUp("b")
	time.sleep(0.5)
	pag.press("n")
	time.sleep(3)
	pag.write("test")
	pag.press("enter")
	for i in range(sets.maxWait):
		if clickButton(sets.images+"chooseProtocol.png"):
			break
	pag.press("down")
	pag.press("enter")
	pag.press("enter")
	pag.press("enter")
	start = False
	for i in range(sets.maxWait):
		if clickButton(sets.images+"starten.png"):
			start = True
			break
	if not start:
		print("de startknop kon niet gevonden worden")
		exit()
	startrec = False
	#start the recorcing
	for i in range(sets.maxWait):						#wait for this button to appear, then click it
		if clickButtonPrecise(sets.images+"record.png"):
			startrec = True
			break
		time.sleep(1)
	#exit out of program if recorder could not be found
	if not startrec:
		print("de recorder kon niet gevonden worden")
		exit()
	pag.move(500,500) #move the mouse out of the way so that no hover pop up apears