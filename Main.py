#cardhave a weird order now, most important and most used card is last, because it doesn't work as the third one
#import librairies
import time
import serial
import pyvisa
import cv2
import easyocr
import mysql.connector
import pyautogui as pag
from math import floor
from serial.serialutil import EIGHTBITS
from python_imagesearch.imagesearch import imagesearch
from subprocess import Popen


#import functions from other files
from clickButton import clickButton, clickButtonPrecise, clickButtonPreciseArea
from clickOnText import clickOnText, clickOnTextOpenCV
from moveFiles import emptyFolder, moveForUse
from checkCableTobt import checkCableTobt
from relaisCommand import relaisCommand
from readValue import readValue
from findImage import findImage
from removeVerticalLines import removeLines

#general setting, needed for all devices
import settings as sets

def main():
#set up to use ocr, relais, database and function generator later
	#database
	dbConn = mysql.connector.connect(user='Sofie', password='MySQLw@chtw00rd',host='127.0.0.1',database='masterproef')
	cursor = dbConn.cursor()
	#ocr
	ocr = easyocr.Reader(['en'])
	#connenction with serial conn
	conn=serial.Serial(port=sets.serconn,baudrate=19200,bytesize=EIGHTBITS,timeout=3) 
	conn.read(100)
	relaisCommand(conn,1,1,0)	#initialise relais
	time.sleep(1)
	relaisCommand(conn,6,sets.cards,1)	#turn usb on and off again
	time.sleep(0.2)
	relaisCommand(conn,3,0,0)	#reset all relais to off
	relaisCommand(conn,6,sets.cards,2) #turn on G2, otherwise nothing can be measured
	#function generator
	rm = pyvisa.ResourceManager()
	adress = rm.list_resources()[0] #the correct adress (for the function generator) always comes first in the list_resources
	afg = rm.open_resource(adress)
	afg.write("*RST")

	#booleans that keep up with wether a test needs to be performed
	cursor.execute("SELECT testID FROM test WHERE testName = 'morpheus';")
	testID = cursor.fetchall()[0][0]
	cursor.execute("SELECT * FROM testparameters WHERE testID = " + str(testID) + ";")
	result = cursor.fetchall()[0]
	oxymeter = result[1]	#heartrate and saturation
	bodypos = result[2]		#bodyposition
	impRef = result[3]		#reference impedence
	impAct = result[4]		#active impedence
	sig = result[5]			#signal waveform
	sigBip = result[6]		#bipolar signal waveform
	press = result[7]		#pressure sensors
	flash = result[8]		#flash light
	button = result[9]		#event button
	btToc = result[10]		#bluetooth to cable
	cTobt = result[11]		#cable to bluetooth
#start recording
	#close Shell+ if still open and give enough time to close properly
	try:
		Popen(["taskkill","/IM","C:\Program Files (x86)\BrainRT\ShellPlus.exe"])
		time.sleep(1)
	except:
		pass
	#empty map where protocols are stored and only put needed protocols in there
	emptyFolder()
	moveForUse(sets.protocolFiles.get("morpheus_ref"))
	#open Shell+ again and wait for it to start up properly
	Popen(sets.pathToShellPlus)
	time.sleep(15)
	#start new measurement
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
	while True:
		if clickButtonPrecise("./images/record.png"):
			break
		x,y = imagesearch("./images/morpheusNotFound.png")
		if x!= -1:
			print("de recorder kon niet worden gedetecteerd")
			exit() 
	pag.move(500,500) #move the mouse out of the way so that no hover pop up apears
#data transition
	"""
	#wait for everything to be initialized well
	wait=0
	while(1):	
		x,y = imagesearch("./images/cable.png")
		if x!= -1:
			s = pag.screenshot()
			color = s.getpixel((x,y))
			if color[0]<5 and color[1]>130 and color[2]<5: #values close to the green color used
				print("cable ok")
				break
		if wait >= sets.maxWait:
			print("cable not ok")
			break	#waited to long, decide it doesn't work
		time.sleep(1)
		wait+=1
	x,y = imagesearch("./images/morpheusNotFound.png")
	if x!= -1:
		print("de recorder kon niet worden gedetecteerd")
		exit()
	relaisCommand(conn,6,sets.cards,1) #interrupt cable
	#this might take a while to work so we go to the next step and check again from time to time with checkCableTobt function
#check SaO2 signals
	#Because a patient simulator is used and not a real person, the values are set and this means a picture of it can be searched
	#because of that, we don't need ocr or coordinates
	wait=0
	while(1):
		x,y = imagesearch("./images/oxymeter.png",precision = 0.95)
		if x != -1:
			oxymeter = True
			print("oxymeter ok")
			break
		if wait>= 5: #sets.maxWait:
			print("oxymeter not ok")
			break
		time.sleep(1)
		wait+=1
	#chek if the pulse signal comes trough by looking for an image match, again this is possible because it is always the same
	wait=0
	while(1):
		x,y = imagesearch("./images/pulsesignal.png")
		if x != -1:
			pulseSignal = True
			print("pulsesignal ok")
			break
		if wait>= 5: #sets.maxWait:
			print("pulsesignal not ok")
			break
		time.sleep(1)
		wait+=1
#data transmission transition
	print("data transition")
	btTocable = checkCableTobt(conn)
	"""
#impedence check
	time.sleep(3)
	clickButton("./images/impedence.png")
	while not clickButton("./images/activeInput.png"):
		pass
	while readValue(sets.x1[0],sets.y1[0],sets.x2[0],sets.y2[0],ocr) == -1:
		pass
	#reference input not shorted
	while not clickButton("./images/referenceInput.png"):
		pass
	#relaisCommand(conn,1,1,0)
	relaisCommand(conn,3,sets.cards,6)
	wait = 0
	test=True
	value = readValue(sets.refImp[0],sets.refImp[1],sets.refImp[2],sets.refImp[3],ocr)
	while not value>sets.minBigImpedence:
		wait += 1
		time.sleep(1)
		if wait >= sets.maxWait:
			test=False
			break
		value = readValue(sets.refImp[0],sets.refImp[1],sets.refImp[2],sets.refImp[3],ocr)
	if test: #smallImpedence
		referenceNotShorted = True
		print("refNS ok")
	else:
		print("refNS not ok")
	#reference input shorted
	relaisCommand(conn,7,sets.cards,4)
	wait = 0
	value = readValue(sets.refImp[0],sets.refImp[1],sets.refImp[2],sets.refImp[3],ocr)
	while True:
			if (value<=maxSmallImpedence and value !=-1):
				longEnough = True
				for i in range(5):										#stay stable on correct value for some time
					if not (value<=maxSmallImpedence and value !=-1):
						longEnough=False
						break
					time.sleep(0.5)
				if longEnough:
					break
			wait += 1
			time.sleep(1)
			if wait >= sets.maxWait:
				break
			value = readValue(sets.x1[i],sets.y1[i],sets.x2[i],sets.y2[i])
	if longEnough: #small impedence 
		referenceShorted = True
		print("refS ok")
	else:
		print("refS not ok")
	#active inputs not shorted
	relaisCommand(conn,6,sets.cards,4)			#back to voltage divider mode
	clickButton("./images/referenceInput.png")
	time.sleep(0.1)
	clickButton("./images/activeInput.png")
	time.sleep(5)
	red = 0
	relais = 4
	card = sets.cards
	conn.read(100)	#empty relais buffer
	for i in range(len(sets.x1)):
		wait = 0
		test=True
		value = readValue(sets.x1[i],sets.y1[i],sets.x2[i],sets.y2[i],ocr)
		while not value>sets.minBigImpedence:
			wait += 1
			time.sleep(1)
			if wait >= sets.maxWait:
				test=False
				break
			value = readValue(sets.x1[i],sets.y1[i],sets.x2[i],sets.y2[i],ocr)
		if test:
			red+=1
	if red == len(sets.x1):
		activeNotShorted = True
		print("activeS ok")
	else:
		print("aciveS not ok")
	relaisCommand(conn,7,card,relais)		#turn off last relais for next test
	conn.read(4)
	#active inputs shorted
	relais = 4
	card = sets.cards
	relaisCommand(conn,7,sets.cards,2)		#switch from voltage divider to shorted
	conn.read(4)
	green=0
	for i in range(len(sets.x1)):
		relaisCommand(conn,7,card,relais)
		conn.read(4)
		relais *= 2
		if relais > 128:
			relais = 1
			card += 1
			if card==sets.cards+1:
				card = 1
		relaisCommand(conn,6,card,relais)
		conn.read(4)
		wait = 0
		value = readValue(sets.x1[i],sets.y1[i],sets.x2[i],sets.y2[i],ocr)
		while True:
			if (value<=maxSmallImpedence and value !=-1):
				longEnough = True
				for i in range(5):										#stay stable on correct value for some time
					if not (value<=maxSmallImpedence and value !=-1):
						longEnough=False
						break
					time.sleep(0.5)
				if longEnough:
					break
			wait += 1
			time.sleep(1)
			if wait >= sets.maxWait:
				break
			value = readValue(sets.x1[i],sets.y1[i],sets.x2[i],sets.y2[i],ocr)
		if longEnough:
			green+=1
	if green == len(sets.x1):
		activeNotShorted = True
		print("activeNS ok")
	else:
		print("aciveNS not ok")
	#close the impedence window
	clickButton("./images/closeImpedence.png")
#signal check
	"""
	#setting some settings to get the view right and compare sine to a correct sine wave
	clickButtonPrecise("./images/1000MicroV.png")
	time.sleep(0.2)
	clickButtonPrecise("./images/2000MicroV.png")
	time.sleep(0.2)
	#there is another 2secs button on the top half of the screen
	clickButtonPreciseArea("./images/10secs.png",0,floor(sets.m_height[0]/2),floor(sets.m_width[0]/2),sets.m_height[0])
	wait=0
	while not clickButtonPreciseArea("./images/2secs.png",0,floor(sets.m_height[0]/2),floor(sets.m_width[0]/2),sets.m_height[0]):
		wait+=1
		if wait>sets.maxWait:
			break
	"""
	#set signal on function generator (sine, 10Hz 4Vpp)
	afg.write("FUNCTION SIN")
	afg.write("FREQUENCY 10")
	afg.write("VOLTAGE:UNIT VPP")
	afg.write("OUTPUT:IMP INF")
	afg.write("VOLTAGE:AMPLITUDE 4") #voltage divider makes it 4 mVpp
	afg.write('OUTPUT1 on')
	#let signal go trough for every input
	conn.read(100)
	relaisCommand(conn,3,sets.cards,250)
	conn.read(4)
	for i in range(1,sets.cards):
		print("loop")
		relaisCommand(conn,3,i,255)
		conn.read(4)
	#TODO: fft
	#turn off all relais, not needed, but just in case
	relaisCommand(conn,3,0,0)
	#close current measurement
	Popen(["taskkill","/IM","BrtTask.exe"])
#signal check bip
	#move the correct protocol to the folder to use it
	try:
		Popen(["taskkill","/IM","C:\Program Files (x86)\BrainRT\ShellPlus.exe"])
		time.sleep(1)
	except:
		pass
	#empty map where protocols are stored and only put needed protocols in there
	emptyFolder()
	moveForUse(sets.protocolFiles.get("morpheus_ref"))
	#open Shell+ again and wait for it to start up properly
	Popen(sets.pathToShellPlus)
	time.sleep(15)
	#start new measurement
	pag.keyDown("alt")
	pag.keyDown("b")
	pag.keyUp("alt")
	pag.keyUp("b")
	pag.press("n")
	pag.write("test")
	pag.press("enter")
	pag.press("enter")
	clickButton("./images/starten.png")
	#let signal go trough for every input
	relaisCommand(conn,3,sets.cards,250)
	conn.read(4)
	for i in range(1,sets.cards):
		relaisCommand(conn,3,i,255)
		conn.read(4)
	time.sleep(20)
	click=clickButton("./images/record.png")
	#TODO: fft
	input("check signals; press enter to continue")
#onboard sensors (comes last because a person is needed to perform these actions)
	#get back to reference test
	#TODO: fix that it opens without clickOnText
	
	input("change bodyposition, press enter to continue")
	print("check Pdiff and Pgage, press enter to continue")
	#TODO: close BrainRT
	#TODO: make rapport
#close the serial connection, database connection and cursor on database
	conn.close()
	cursor.close()
	dbConn.close()

main()