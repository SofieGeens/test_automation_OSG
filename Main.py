#cards have a weird order now, most important and most used card is last, because it doesn't work as the first one
#for now results are written to a .txt file
#import librairies
import time
import serial
import pyvisa
import os
import mysql.connector
import pyautogui as pag
from math import floor
from serial.serialutil import EIGHTBITS
from python_imagesearch.imagesearch import imagesearch
from subprocess import Popen


#import functions from other files
from clickButton import clickButton, clickButtonPrecise, clickButtonPreciseArea
from moveFiles import emptyFolder, moveForUse
from dataTransition import checkBt, checkCable
from relaisCommand import relaisCommand
from readValue import readValue
from brt2p_func import fft, oxyMeter, getPath
from startMeasurement import startMeasurement

#general setting, needed for all devices
import settings as sets

def main():
#set up relais, database and function generator later
	#database
	dbConn = mysql.connector.connect(user= os.environ.get('MYSQLUSER_OSG'), password=os.environ.get('MYSQLPASSWORD_OSG'),host='127.0.0.1',database='masterproef')
	cursor = dbConn.cursor()			#sends queries to the db
	#connenction with serial conn
	conn=serial.Serial(port=sets.serconn,baudrate=19200,bytesize=EIGHTBITS,timeout=3) 
	conn.read(100)
	relaisCommand(conn,1,1,0)			#initialise relais
	time.sleep(1)
	relaisCommand(conn,6,sets.cards,1)	#turn usb on and off again
	time.sleep(0.2)
	relaisCommand(conn,3,0,0)			#reset all relais to off
	relaisCommand(conn,6,sets.cards,2)	#turn on G2, otherwise nothing can be measured
	#function generator
	"""
	rm = pyvisa.ResourceManager()
	adress = rm.list_resources()[0]		#the correct adress (for the function generator) always comes first in the list_resources
	afg = rm.open_resource(adress)
	afg.write("*RST")					#reset the function generator
	"""
	#initialise txt file to write results to
	resultFile = open("testResults.txt",'w')

	#booleans that keep up with wether a test needs to be performed
	cursor.execute("SELECT testID FROM test WHERE testName = 'morpheus';")
	testID = cursor.fetchall()[0][0]	#testID is foreign key in all other tables of database
	cursor.execute("SELECT oxy,bodypos,impRef,impAct,sig,sigBip,press,flash,button,cb FROM testparameters WHERE testId = " + str(testID) + ";")
	result = cursor.fetchall()[0]
	#booleans that keep up with wether a test needs to be performed
	oxymeter = result[0]	#heartrate and saturation
	bodypos = result[1]		#bodyposition
	impRef = result[2]		#reference impedence
	impAct = result[3]		#active impedence
	sig = result[4]			#signal waveform
	sigBip = result[5]		#bipolar signal waveform
	press = result[6]		#pressure sensors
	flash = result[7]		#flash light
	button = result[8]		#event button
	cb = result[9]			#data transition between cable and bluetooth
#start recording
	#close Shell+ if still open and give enough time to close properly
	try:
		os.system("taskkill /f /im ShellPlus.exe")
		time.sleep(1)
	except:
		pass
	#empty map where protocols are stored and only put needed protocols in there
	emptyFolder()
	cursor.execute("SELECT fileName FROM protocols WHERE testID = "+str(testID)+" ORDER BY protocolId;")
	result = cursor.fetchall() 
	print(result)
	fname = result[0][0]
	moveForUse(fname)
	#open Shell+ again, wait for it to start up properly and start the measurement
	Popen(sets.pathToShellPlus)
	time.sleep(15)
	startMeasurement()
	"""
#data transition
	checkCable()												#wait for cable connection to be fully settled
	if cb:
		relaisCommand(conn,6,sets.cards,1)						#interrupt cable between device and computer to switch to bluetooth mode, this takes a while to work so we go to the next step and check again after checking the SaO2 with checkCableTobt function
	else:
		print("probleem")
#check SaO2 signal
	if oxymeter:
		#chek if the pulse signal comes trough by looking for an image match, this is possible because the signal is always the same because of the use of a virtual patient
		pulsesig=False
		for i in range(sets.maxWait):							#try maxWait times before deciding it is not correct
			x,y = imagesearch("./images/pulsesignal.png")
			if x != -1:											#signal found, the signal has the correct shape
				pulsesig = True
				resultFile.write("pulsesignaal ok \n")
				break
			time.sleep(1)
		if not pulsesig:
			resultFile.write("pulsesignaal niet ok\n")
#data transmission transition
	if cb:
		#TODO: TODO in dataTransition.py
		if checkBt(conn):
			resultFile.write("cable naar bluetooth ok\n")
		else:
			resultFile.write("cable naar bluetooth niet ok\n")
	relaisCommand(conn,7,sets.cards,1)							#reconnect cable
	if cb:
		if checkCable(): 
			resultFile.write("bluetooth naar cable ok\n")
		else:
			resultFile.write("bluetooth naar cable niet ok\n")
	"""
#impedence check
	if impRef:
		time.sleep(3)
		#start impedence measurement
		#TODO: TODO in clickButton.py
		clickButton("./images/impedence.png")
		#reference input not shorted
		while not clickButtonPrecise("./images/activeInput.png"):		#switch to reference input screen
			pass
		while not clickButtonPrecise("./images/referenceInput.png"):
			pass
		relaisCommand(conn,3,sets.cards,6)						#set relais to voltage divider
		wait = 0
		test=True
		cursor.execute("SELECT x1, y1, x2, y2 FROM impedancecoordinates WHERE inputId IN (SELECT DISTINCT inputId FROM inputs WHERE testId = "+str(testID)+") ORDER BY inputId;")
		result = cursor.fetchall()
		cursor.execute("SELECT inputName FROM inputs where  testId = "+str(testID)+" ORDER BY inputId;")
		names = cursor.fetchall()
		value = readValue(result[0][0],result[0][1],result[0][2],result[0][3],names[0][0]+"_NS.png")
		while not value>sets.minBigImpedence:					#impedence should be big
			wait += 1
			time.sleep(1)
			if wait >= sets.maxWait:							#waited to long, decide test was unsuccesfull
				test=False
				break
			value = readValue(result[0][0],result[0][1],result[0][2],result[0][3],names[0][0]+"_NS.png")
		if test: 
			referenceNotShorted = True
			resultFile.write("referentie input impedantie niet kortgesloten ok")
		else:
			resultFile.write("referentie input impedantie niet kortgesloten niet ok")
		#reference input shorted
		relaisCommand(conn,7,sets.cards,4)						#set relais to short
		value = readValue(result[0][0],result[0][1],result[0][2],result[0][3],names[0][0]+"_S.png")
		test = False
		for i in range(sets.maxWait):							#try a coulple of times to give time to settle
			if (value<=sets.maxSmallImpedence and value !=-1):
				stable = True
				for i in range(sets.stableImpedence):			#stay stable on correct value for some time
					if not (value<=sets.maxSmallImpedence and value !=-1):
						stable = False
						break
					time.sleep(1)
				if stable:
					resultFile.write("referentie input impedantie kortgesloten ok")
					test=True
					break
			time.sleep(1)
			value = readValue(result[0][0],result[0][1],result[0][2],result[0][3],names[0][0]+"_S.png")
		if not test:										#test unsuccesfull
			resultFile.write("referentie input impedantie kortgesloten niet ok")
		#active inputs not shorted
		relaisCommand(conn,6,sets.cards,4)					#switch relais to voltage divider mode
		correct = 0
		conn.read(100)										#empty relais buffer
		for i in range(1,len(result)):						#for every input
			wait = 0
			test=True
			value = readValue(result[i][0],result[i][1],result[i][2],result[i][3],names[i][0]+"_NS.png") #i+1 because first value (index 0) in result is reference input 
			while not value>sets.minBigImpedence:
				wait += 1
				time.sleep(1)
				if wait >= sets.maxWait:					#waited to long, decide it doesn't work
					test=False
					break
				value = readValue(result[i][0],result[i][1],result[i][2],result[i][3],names[i][0]+"_NS.png")
			if test:
				correct+=1
		if correct == len(result):
			activeNotShorted = True
			resultFile.write("active inputs niet kortgesloten ok")
		else:
			resultFile.write("active inputs niet kortgesloten niet ok")
		#relaisCommand(conn,7,sets.cards,relais)				#turn off last relais for next test
		conn.read(4)
		#active inputs shorted
		relais = 4											#first relais on this card are for other purposes
		card = sets.cards									#weird order in cards because one doesn't fully work, will get fixed
		relaisCommand(conn,7,sets.cards,2)					#switch from voltage divider to shorted
		conn.read(4)										#clear buffer
		correct=0
		for i in range(1,len(result)):
			relaisCommand(conn,7,card,relais)				#turn off relais of previous measurement
			conn.read(4)									#clear buffer
			relais *= 2										#relais adress works by setting bit on high, ex.: 00100000 is the 6th relais, 00000100 is the 3th relais, to go to next relais, bitshift to left of multiply by 2 
			if relais > 128:								#out of relais on this card, go to first relais of next card
				relais = 1
				card += 1
				if card==sets.cards+1:						#because of weird order of relais cards, will get fixed
					card = 1
			relaisCommand(conn,6,card,relais)				#switch on relais card
			conn.read(4)									#clear buffer
			value = readValue(result[i][0],result[i][1],result[i][2],result[i][3],names[i][0]+"_NS.png")
			test = False
			for j in range(sets.maxWait):							#try a coulple of times to give time to settle
				if (value==0 and value !=-1):
					break
					stable = True
					for i in range(sets.stableImpedence):			#stay stable on correct value for some time
						value = readValue(result[i][0],result[i][1],result[i][2],result[i][3],names[i][0]+"_NS.png")
						if not (value<=sets.maxSmallImpedence and value !=-1):
							stable = False
							break
						time.sleep(1)
					if stable:
						print("actS ok")
						test=True
						break
				time.sleep(1)
				value = readValue(result[i][0],result[i][1],result[i][2],result[i][3],names[i][0]+"_NS.png")
		if not test:										#test unsuccesfull
			print("actS not ok")
		#close the impedence window
		clickButton("./images/closeImpedence.png")
		#TODO: close prev measurement
#start new measurement to get clean data, because some other measurements stop during impedance check
	#TODO: fixen met meerder protocols
	startMeasurement()
#signal check and oxymeter check
	"""
	#set signal on function generator (sine, 10Hz 4Vpp)
	afg.write("FUNCTION SIN")
	afg.write("FREQUENCY 10")
	afg.write("VOLTAGE:UNIT VPP")
	afg.write("OUTPUT:IMP INF")
	afg.write("VOLTAGE:AMPLITUDE 4") #voltage divider makes it 4 mVpp
	afg.write('OUTPUT1 on')
	#let signal go trough for every input
	conn.read()
	relaisCommand(conn,3,sets.cards,250)
	conn.read(4)
	for i in range(1,sets.cards):
		print("loop")
		relaisCommand(conn,3,i,255)
		conn.read(4)
	time.sleep(3)
	#turn off all relais, not needed, but just in case
	relaisCommand(conn,3,0,0)
	#close current measurement
	Popen(["taskkill","/IM","BrtTask.exe"])
	time.sleep(3)					#give program some time to shut down
	path = getPath()
	#TODO: TODO in fft function (brt2p_func)
	result = fft(path)	
	correct = 0
	for item in result:
	#TODO: check of die 4 wel klopt
		if len(item[0])==1 and item[0] == 10 and item[1]==4:
			correct +=1
	if correct == len(result):
		print("signalRef ok")
	else:
		print("signalRef not ok")
	if oxyMeter(path)[0] == 98.0 and oxyMeter(path)[1] == 80.0:
		print("oxymeter ok")
	else:
		print("oxymeter not ok")
#signal check bip
	#move the correct protocol to the folder to use it
	Popen(["taskkill","/IM","C:\Program Files (x86)\BrainRT\ShellPlus.exe"])
	time.sleep(3)					#give program some time to shut down
	#empty map where protocols are stored and only put needed protocols in there
	emptyFolder()
	moveForUse(sets.protocolFiles.get("morpheus_bip"))
	#open Shell+ again and wait for it to start up properly
	Popen(sets.pathToShellPlus)
	time.sleep(15)
	#start new measurement
	startMeasurement()
	#let signal go trough for every input
	relaisCommand(conn,3,sets.cards,250)
	conn.read(4)
	for i in range(1,sets.cards):
		relaisCommand(conn,3,i,255)
		conn.read(4)
	click=clickButton("./images/record.png")
	time.sleep(3)
	Popen(["taskkill","/IM","BrtTask.exe"])
	result = fft(getPath())
	correct = 0
	for item in result:
	#TODO: check of die 4 wel klopt
		if len(item[0])==1 and item[0] == 10 and item[1]==4:
			correct +=1
	if correct == len(result):
		print("signalBip ok")
	else:
		print("signalBip not ok")
#onboard sensors (comes last because a person is needed to perform these actions)
	#get back to reference test
	#close Shell+ if still open and give enough time to close properly
	Popen(["taskkill","/IM","C:\Program Files (x86)\BrainRT\ShellPlus.exe"])
	time.sleep(1)
	#empty map where protocols are stored and only put needed protocols in there
	emptyFolder()
	moveForUse(sets.protocolFiles.get("morpheus_ref"))
	#open Shell+ again and wait for it to start up properly
	Popen(sets.pathToShellPlus)
	time.sleep(15)
	#start new measurement
	startMeasurement()
	input("change bodyposition, press enter to continue")
	print("check Pdiff and Pgage, press enter to continue")
	#TODO: close BrainRT
	#TODO: make rapport
#close the serial connection, textfile, database connection and cursor on database
	conn.close()
	resultFile.close()
	cursor.close()
	dbConn.close()
	"""
main()