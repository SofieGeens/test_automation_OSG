#import librairies
import time
import pyautogui as pag

#import functions from other files
from clickButton import clickButton
from clickOnText import clickOnText
from brainRT import openBrainRT, closeBrainRT
from moveFiles import emptyFolder, moveForUse
#general setting, needed for all devices
import settings as sets

#booleans that keep up with wether a test was succesful
heartrate = False
saturation = False
hartpattern = False

def main():
#start recording
	#close Shell+ if still open and give enough time to close properly
	try:
		closeBrainRT()
		time.sleep(1)
	except:
		pass
	#empty map where protocols are stored and only put needed protocols in there
	emptyFolder()
	moveForUse([sets.protocolFiles.get("morpheus_ref"),sets.protocolFiles.get("morpheus_bip")])
	#open Shell+ again and wait for it to start up properly
	openBrainRT()
	time.sleep(15)
	#start new measurement
	clickButton("./images/nieuweMeting.png")
	time.sleep(5)
	pag.write("test")
	time.sleep(0.1)
	pag.press("enter")
	time.sleep(1)
	clickButton("./images/chooseProtocol.png")
	time.sleep(0.5)
	s=sets.protocolNames.get("morpheus_ref")
	clickOnText(s.replace(" ",""),'l')  #get rid of spaces, because clickOnText cannot deal with them
	pag.press("enter")
	clickButton("./images/starten.png")
	time.sleep(20)
	click=clickButton("./images/record.png")
	time.sleep(5)

#check SaO2 signals
	#h=readValue(settings.heart[0],settings.heart[1])	#read heartrate
	#if h<
#data transition

#impedence check

#signal check

#onboard sensors

main()