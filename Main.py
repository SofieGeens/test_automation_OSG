#cards have a weird order now, most important and most used card is last, because it doesn't work as the first one
#for now results are written to a .txt file
#import librairies
import time
import serial
import pyvisa
import os
import sys
import mysql.connector
import pyautogui as pag
from math import floor
from serial.serialutil import EIGHTBITS
from python_imagesearch.imagesearch import imagesearch
from subprocess import Popen


#import functions from other files
from moveFiles import emptyFolder, moveForUse
from dataTransition import checkBt, checkCable
from relaisCommand import relaisCommand
from readValue import readValue
from brt2p_func import np_fft, oxyMeter, getPath
from startMeasurement import startMeasurement

#general setting, needed for all devices
import settings as sets

def main():
#set up relais, database and function generator later
	#database
	dbConn = mysql.connector.connect(user= os.environ.get('MYSQLUSER_OSG'), password=os.environ.get('MYSQLPASSWORD_OSG'),host='127.0.0.1',database='masterproef')
	cursor = dbConn.cursor()			#sends queries to the db
	#take command line arguments
	device = sys.argv[1]
	serialNumber = sys.argv[2]
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
	rm = pyvisa.ResourceManager()
	adress = rm.list_resources()[0]		#the correct adress (for the function generator) always comes first in the list_resources
	afg = rm.open_resource(adress)
	afg.write("*RST")					#reset the function generator
	#initialise txt file to write results to
	resultFile = open(serialNumber+".html",'a')

	#booleans that keep up with wether a test needs to be performed
	cursor.execute("SELECT testID FROM test WHERE testName = '"+device+"';")
	testID = cursor.fetchall()[0][0]	#testID is foreign key in all other tables of database
	cursor.execute("SELECT oxy,bodypos,impRef,impAct,sig,sigBip,press,flash,button,cb FROM testparameters WHERE testId = " + str(testID) + ";")
	result = cursor.fetchall()[0]
	#booleans that keep up with wether a test needs to be performed
	oxy = result[0]	#heartrate and saturation
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
	protocols = cursor.fetchall() 
	fname = protocols[0][0]
	moveForUse(fname)
	#open Shell+ again, wait for it to start up properly and start the measurement
	Popen(sets.pathToShellPlus)
	time.sleep(15)
	startMeasurement()
#data transition
	checkCable()												#wait for cable connection to be fully settled
	if cb:
		relaisCommand(conn,6,sets.cards,1)						#interrupt cable between device and computer to switch to bluetooth mode, this takes a while to work so we go to the next step and check again after checking the SaO2 with checkCableTobt function
#check SaO2 signal
	if oxy:
		#chek if the pulse signal comes trough by looking for an image match, this is possible because the signal is always the same because of the use of a virtual patient
		pulsesig=False
		for i in range(sets.maxWait):							#try maxWait times before deciding it is not correct
			x,y = imagesearch("./images/pulsesignal.png")
			if x != -1:											#signal found, the signal has the correct shape
				pulsesig = True
				resultFile.write("<p style='color:green;'>pulsesignaal ok </p>")
				break
			time.sleep(1)
		if not pulsesig:
			resultFile.write("<p style='color:red;'>pulsesignaal niet ok</p>")
		pag.screenshot("pulsesig.png",region = (sets.pulseSig[0],sets.pulseSig[1],sets.pulseSig[2],sets.pulseSig[3]))
		resultFile.write("<img src='pulsesig.png' alt='Pulse signal'>")
#data transmission transition

	if cb:
		if checkBt(conn):
			resultFile.write("<p style='color:green;'>kabel naar bluetooth ok</p>")
		else:
			resultFile.write("<p style='color:red;'>kabel naar bluetooth niet ok</p>")
		pag.screenshot("c2b.png",region = (sets.dataTrans[0],sets.dataTrans[1],sets.dataTrans[2],sets.dataTrans[3]))
		resultFile.write("<img src='c2b.png' alt='kabel naar bluetooth'>")
		relaisCommand(conn,7,sets.cards,1)							#reconnect cable
		if checkCable(): 
			resultFile.write("<p style='color:green;'>bluetooth naar kabel ok</p>")
		else:
			resultFile.write("<p style='color:red;'>bluetooth naar kabel niet ok</p>")
		pag.screenshot("b2c.png",region = (sets.dataTrans[0],sets.dataTrans[1],sets.dataTrans[2],sets.dataTrans[3]))
		resultFile.write("<img src='b2c.png' alt='bluetooth naar kabel'>")
#impedence check
	if impRef:
		time.sleep(3)
		#start impedence measurement
		pag.click(x=sets.impedance[0],y=sets.impedance[1])
		time.sleep(10)
		#reference input not shorted
		pag.click(x=sets.dropdownImpedance[0],y=sets.dropdownImpedance[1])		#switch to reference input screen
		time.sleep(0.5)
		pag.click(x=sets.reference[0],y=sets.reference[1])
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
			resultFile.write("<p style='color:green;'>referentie input impedantie niet kortgesloten ok</p>")
		else:
			resultFile.write("<p style='color:red;'>referentie input impedantie niet kortgesloten niet ok</p>")
		resultFile.write("<img src='"+names[0][0]+".png' alt='impedantiemeting'>")
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
					value = readValue(result[0][0],result[0][1],result[0][2],result[0][3],names[0][0]+"_S.png")
					time.sleep(1)
				if stable:
					resultFile.write("<p style='color:green;'>referentie input impedantie kortgesloten ok</p>")
					test=True
					break
			time.sleep(1)
			value = readValue(result[0][0],result[0][1],result[0][2],result[0][3],names[0][0]+"_S.png")
		if not test:										#test unsuccesfull
			resultFile.write("<p style='color:red;'>referentie input impedantie kortgesloten niet ok</p>")
		resultFile.write("<img src='"+(names[0][0]+".png' alt='impedantiemeting'>")
		#reference input not shorted
		pag.click(x=sets.dropdownImpedance[0],y=sets.dropdownImpedance[1])		#switch to reference input screen
		time.sleep(0.5)
		pag.click(x=sets.active[0],y=sets.active[1])
		relaisCommand(conn,6,sets.cards,4)					#switch relais to voltage divider mode
		conn.read(100)										#empty relais buffer
		for i in range(1,len(result)):						#for every input
			wait = 0
			test=True
			value = readValue(result[i][0],result[i][1],result[i][2],result[i][3],names[i][0]+"_NS.png") 
			while not value>sets.minBigImpedence:
				wait += 1
				time.sleep(1)
				if wait >= sets.maxWait:					#waited to long, decide it doesn't work
					test=False
					break
				value = readValue(result[i][0],result[i][1],result[i][2],result[i][3],names[i][0]+"_NS.png")
			if test:
				resultFile.write("<p style='color:green;'>active input "+names[i][0]+" niet kortgesloten ok</p>")
			else:
				resultFile.write("<p style='color:red;'>active input "+names[i][0]+" niet kortgesloten niet ok</p>")
			resultFile.write("<img src='"+names[i][0]+".png' alt='impedantiemeting'>")
		conn.read(4)
		#active inputs shorted
		relais = 4											#first relais on this card are for other purposes
		card = sets.cards									#weird order in cards because one doesn't fully work, will get fixed
		relaisCommand(conn,7,sets.cards,2)					#switch from voltage divider to shorted
		conn.read(4)										#clear buffer
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
			value = readValue(result[i][0],result[i][1],result[i][2],result[i][3],names[i][0]+"_S.png")
			test = False
			for j in range(sets.maxWait):					#try a coulple of times to give time to settle
				if (value==0 and value !=-1):
					break
					stable = True
					for i in range(sets.stableImpedence):	#stay stable on correct value for some time
						value = readValue(result[i][0],result[i][1],result[i][2],result[i][3],names[i][0]+"_S.png")
						if not (value<=sets.maxSmallImpedence and value !=-1):
							stable = False
							break
						time.sleep(1)
					if stable:
						resultFile.write("<p style='color:green;'>active input "+names[i][0]+" kortgesloten ok</p>")
						test = True
						break
				if not test:
					resultFile.write("<p style='color:red;'>active input "+names[i][0]+" niet kortgesloten niet ok</p>")
				resultFile.write("<img src='"+names[i][0]+".png' alt='impedantiemeting'>")
				time.sleep(1)

	#close the impedence window
	pag.click(x=sets.impedance[0],y=sets.impedance[1])
	time.sleep(1)
	#close current measurement
	os.system("taskkill /f /im BrtTask.exe")
	time.sleep(10)
#signal check and oxymeter check
	#set signal on function generator
	if sig:
		afg.write("FUNCTION SIN")
		afg.write("FREQUENCY "+str(sets.frequency))
		afg.write("VOLTAGE:UNIT VPP")
		afg.write("OUTPUT:IMP INF")
		afg.write("VOLTAGE:AMPLITUDE "+str(sets.amplitude)) #voltage divider makes it 1000 times smaller
		afg.write('OUTPUT1 on')
		#let signal go trough for every input by switching all necessary relais
		conn.read()
		relaisCommand(conn,3,sets.cards,250)
		conn.read(10)
		for i in range(1,sets.cards):
			relaisCommand(conn,3,i,255)
			conn.read(4)
		#start new measurement to get clean data, because some other measurements stop during impedance check
		relaisCommand(conn,6,sets.cards,1)	#turn usb on and off again
		time.sleep(0.2)
		relaisCommand(conn,7,sets.cards,1)
		startMeasurement()
		time.sleep(15)										    #let it run long enough to get enough datapoints
		pag.screenshot("signal_ref0.png")						#screenshot for in report
		#close current measurement
		os.system("taskkill /f /im BrtTask.exe")
		time.sleep(10)										#give program some time to shut down
		path = getPath()
		result = np_fft(path,cursor,False)	
		correct = 0
		for item in result:
		#TODO: fixen wat die 4 moet zijn, nog geen idee hoe, misschien gewoon subtiel weglaten?
			print(item[1])
			if len(item[0])==1 and item[0] == 10 and item[1]==4:
				correct +=1
		if correct == len(result):
			resultFile.write("<p style='color:green;'>referentie signaal "+names[i][0]+" ok</p>")
		else:
			resultFile.write("signalRef not ok")
	if oxy:
		result = oxyMeter(path)
		if result[0] == 98.0 and result[1] == 80.0:
			resultFile.write("<p style='color:green;'>oxymeter waarden ok</p>")
		else:
			resultFile.write("<p style='color:green;'>oxymeter waarden not ok</p>")
	os.system("taskkill /f /im ShellPlus.exe")
	if sig:
		for i in range(1,len(protocols)):
			if not "bip" in protocols[i][0]:
				relaisCommand(conn,6,sets.cards,1)	#turn usb on and off again
				time.sleep(0.2)
				relaisCommand(conn,7,sets.cards,1)
				emptyFolder()
				moveForUse(protocols[i][0])
				time.sleep(0.5)
				Popen(sets.pathToShellPlus)
				time.sleep(15)
				startMeasurement()
				time.sleep(10)
				pag.screenshot("signal_ref"+str(i)+".png")
				resultFile.write("<img src='signal_ref"+str(i)+".png' alt='referentie signaal'>")
				os.system("taskkill /f /im BrtTask.exe")
				time.sleep(5)
				os.system("taskkill /f /im ShellPlus.exe")
				time.sleep(10)
			else:
				break
#signal check bip
	if sigBip:
		#move the correct protocol to the folder to use it
		os.system("taskkill /f /im ShellPlus.exe")
		time.sleep(3)					#give program some time to shut down
		#empty map where protocols are stored and only put needed protocols in there
		bipId = 0
		emptyFolder()
		for protocol in protocols:
			if "bip" in protocol[0]:
				cursor.execute("SELECT protocolId FROM protocols where  fileName = '"+protocol[0]+"';")
				bipId = cursor.fetchall()[0][0]
				#TODO: NOG EEN FETCH EN DAN MET DIE ID EEN LOOP BEGINNEN
				moveForUse(protocol[0])
				#open Shell+ again and wait for it to start up properly
				Popen(sets.pathToShellPlus)
				time.sleep(15)
				#start new measurement
				startMeasurement()
				time.sleep(3)
				pag.screenshot("signal_bip0.png")
				os.system("taskkill /f /im BrtTask.exe")
				time.sleep(3)
				os.system("taskkill /f /im ShellPlus.exe")
				time.sleep(15)
				result = np_fft(getPath(),cursor,True)
				correct = 0
				for item in result:
				#TODO: check of die 4 wel klopt
					if len(item[0])==1 and item[0] == 10 and item[1]==4:
						correct +=1
				if correct == len(result):
					resultFile.write("signalBip ok")
				else:
					resultFile.write("signalBip not ok")
		for i in range(bipId+1,len(protocols)):
			emptyFolder()
			moveForUse(protocols[i][0])
			Popen(sets.pathToShellPlus)
			time.sleep(15)
			startMeasurement()
			time.sleep(3)
			pag.screenshot("signal_ref"+str(i)+".png")
			os.system("taskkill /f /im BrtTask.exe")
			time.sleep(5)
			os.system("taskkill /f /im ShellPlus.exe")
			time.sleep(10)
#onboard sensors (comes last because a person is needed to perform these actions)
	#get back to reference test
	emptyFolder()											#empty map where protocols are stored and only put needed protocols in there
	moveForUse(protocols[0][0])
	#open Shell+ again and wait for it to start up properly
	Popen(sets.pathToShellPlus)
	time.sleep(15)
	#start new measurement
	startMeasurement()
#close the serial connection, textfile, database connection and cursor on database
	conn.close()
	resultFile.close()										#close the file without closing the body, because some more info is added at the end (about bodypos and pressure sensors)
	cursor.close()
	dbConn.close()
main()