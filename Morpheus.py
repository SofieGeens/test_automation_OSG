#import librairies
import time
import serial
import pyvisa
import pyautogui as pag
from serial.serialutil import EIGHTBITS

#import functions from other files
from clickButton import clickButton
from clickOnText import clickOnText
from brainRT import openBrainRT, closeBrainRT
from moveFiles import emptyFolder, moveForUse
from findImage import findImage
from checkCableTobt import checkCableTobt
#general setting, needed for all devices
import settings as sets

#booleans that keep up with wether a test was succesful
oxymeter = False
pulseSignal = False
btTocable = False
cableTobt = False

def main():
#set up to use relais and function generator later
	#conn=serial.Serial(port=sets.serconn,baudrate=19200,bytesize=EIGHTBITS,timeout=3) #start connenction with serial conn
	#conn.write(bytes.fromhex("01010000")) #initialise relais
	rm = pyvisa.ResourceManager()
	adress = rm.list_resources()[0] #the correct adress always comes first in the list_resources
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
	"""
#data transition
	#wait for everything to be initialized well
	while(not findImage("./images/defaultCablebt.png")):
		pass
	#TODO: usb onderbreken
	print("onderbreek kabel")
	#this might take a while to work so we go to the next step and check again from time to time with checkCableTobt function
#check SaO2 signals
	#it takes some time before the saO2 signals are read correctly
	time.sleep(10)
	cableTobt = checkCableTobt()
	#Because a patient simulator is used and not a real person, the values are set and this means a picture of it can be searched
	#because of that, we don't need ocr or coordinates
	oxymeter = findImage("./images/oxymeter.png")
	#chek if the pulse signal comes trough by looking for an image match, again this is possible because it is always the same
	pulseSignal = findImage("./images/pulsesignal.png")
	#wait till the data transition check is fully completed before starting impedence check
	if oxymeter:
		print("oxymeter ok")
	if pulseSignal:
		print("pulsesignal ok")
	if not cableTobt:
		while(1):
			btTocable = checkCableTobt()
			if btTocable:
				break;
	print("break")
	

#impedence check
	#clickButton("./images/impedence.png")

#signal check
	#setting some settings to get the view right and compare sine to a correct sine wave
	print("screen settings")
	clickButton("./images/1000MicroV.png")
	time.sleep(0.05)
	clickButton("./images/2000MicroV.png")
	time.sleep(0.05)
	clickButton("./images/10secs.png")
	time.sleep(0.05)
	clickButton("./images/2secs.png")
	#set signal on function generator (sine, 10Hz 4mVpp)
	afg.write("FUNCTION SIN")
	afg.write("FREQUENCY 10")
	afg.write("VOLTAGE:AMPLITUDE 0.004")
	afg.write('output1 on')
#onboard sensors
	#onboard sensors come last because a person is needed to perform these actions

main()