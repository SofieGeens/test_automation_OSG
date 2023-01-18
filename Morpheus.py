#import librairies
import time
import serial
import pyvisa
import pyautogui as pag
from serial.serialutil import EIGHTBITS
from python_imagesearch.imagesearch import imagesearch


#import functions from other files
from clickButton import clickButton, clickButtonPrecise
from clickOnText import clickOnText
from brainRT import openBrainRT, closeBrainRT
from moveFiles import emptyFolder, moveForUse
from checkCableTobt import checkCableTobt
from relaisCommand import relaisCommand
from readValue import readValue
#general setting, needed for all devices
import settings as sets

#booleans that keep up with wether a test was succesful
oxymeter = False
pulseSignal = False
btTocable = False
cableTobt = False
referenceNotShorted = False
referenceShorted = False
activeNotShorted = False
activeShorted = False

def main():
#set up to use relais and function generator later
	conn=serial.Serial(port=sets.serconn,baudrate=19200,bytesize=EIGHTBITS,timeout=3) #start connenction with serial conn
	relaisCommand(conn,1,1,0) #initialise relais
	time.sleep(1)
	relaisCommand(conn,7,1,1)
	
	rm = pyvisa.ResourceManager()
	adress = rm.list_resources()[0] #the correct adress (for the function generator) always comes first in the list_resources
	afg = rm.open_resource(adress)
	afg.write("*RST")
#start recording
	"""
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
	
#data transition
	#wait for everything to be initialized well
	while(1):	
		x,y = imagesearch("./images/cable.png")
		if x!= -1:
			s = pag.screenshot()
			color = s.getpixel((x,y))
			if color[0]<5 and color[1]>130 and color[2]<5: #values close to the green color used, 
				break
	print("cable ok")
	relaisCommand(conn,6,1,1) #interrupt cable
	#this might take a while to work so we go to the next step and check again from time to time with checkCableTobt function

#check SaO2 signals
	#it takes some time before the saO2 signals are read correctly
	time.sleep(10)
	cableTobt = checkCableTobt(conn)
	#Because a patient simulator is used and not a real person, the values are set and this means a picture of it can be searched
	#because of that, we don't need ocr or coordinates
	oxymeter = imagesearch("./images/oxymeter.png")
	#chek if the pulse signal comes trough by looking for an image match, again this is possible because it is always the same
	pulseSignal = imagesearch("./images/pulsesignal.png")
	#wait till the data transition check is fully completed before starting impedence check
	if oxymeter:
		print("oxymeter ok")
	if pulseSignal:
		print("pulsesignal ok")
	if not cableTobt:
		while(1):
			btTocable = checkCableTobt(conn)
			if btTocable:
				print("break")
				break;
	"""
#impedence check
	time.sleep(3)
	clickButton("./images/impedence.png")
	time.sleep(1)
	while not clickButton("./images/activeInput.png"):
		pass
	#reference input not shorted
	#clickButton("./images/activeInput.png")
	time.sleep(1)
	clickButton("./images/referenceInput.png")
	time.sleep(5)					#it takes long before the values are correct
	if readValue(190,350,235,370) > 1000: 
		referenceNotShorted = True
	#reference input shorted
	relaisCommand(7,1,3)
	if readValue(190,350,235,370) < 1000: 
		referenceShorted = True
	#active inputs not shorted
	clickButton("./images/referenceInput.png")
	time.sleep(0.1)
	clickButton("./images/activeInput.png")
	#active inputs shorted

#signal check
	#setting some settings to get the view right and compare sine to a correct sine wave
	clickButtonPrecise("./images/1000MicroV.png")
	time.sleep(0.2)
	clickButtonPrecise("./images/2000MicroV.png")
	time.sleep(0.2)
	clickButtonPrecise("./images/10secs.png")
	time.sleep(0.2)
	clickButtonPrecise("./images/2secs.png")
	#set signal on function generator (sine, 10Hz 4Vpp)
	afg.write("FUNCTION SIN")
	afg.write("FREQUENCY 10")
	afg.write("VOLTAGE:UNIT VPP")	
	afg.write("VOLTAGE:AMPLITUDE 4") #voltage divider makes it 4 mVpp
	afg.write('output1 on')
	#let signal go trough for every input
	relaisCommand(3,1,254)
	for i in range(2,settings.cards+1):
		relaisCommand(3,i,255)
#signal check bip
#onboard sensors
	#onboard sensors come last because a person is needed to perform these actions

main()