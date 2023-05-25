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
	print(device)
	fileName = sys.argv[2]
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
	resultFile = open(fileName,'a')

	#booleans that keep up with wether a test needs to be performed
	cursor.execute("SELECT testID FROM test WHERE testName = '"+device+"';")
	testID = cursor.fetchall()[0][0]	#testID is foreign key in all other tables of database
	cursor.execute("SELECT oxy,bodypos,impRef,impAct,sig,sigBip,press,flash,button,cb FROM testparameters WHERE testId = " + str(testID) + ";")
	result = cursor.fetchall()[0]
	#booleans that keep up with wether a test needs to be performed
	oxy = result[0]			#heartrate and saturation
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
	"""
	Popen(sets.pathToShellPlus)
	time.sleep(15)
	startMeasurement()
#check SaO2 signal
	if oxy:
		cursor.execute("UPDATE progress SET oxysig=1")
		dbConn.commit()
		#chek if the pulse signal comes trough by looking for an image match, this is possible because the signal is always the same because of the use of a virtual patient
		pulsesig=False
		for i in range(sets.maxWait):							#try maxWait times before deciding it is not correct
			x,y = imagesearch(sets.images+"pulsesignal.png")
			if x != -1:											#signal found, the signal has the correct shape
				pulsesig = True
				resultFile.write("<p style='color:green;'>pulsesignal ok </p>\n")
				cursor.execute("UPDATE progress SET oxysig=2")
				dbConn.commit()
				break
			time.sleep(1)
		if not pulsesig:
			resultFile.write("\n<p style='color:red;'>pulsesignal not ok</p>\n")
			cursor.execute("UPDATE progress SET oxysig=3")
			dbConn.commit()
		pag.screenshot(sets.reportImages+"pulsesig.png",region = (sets.pulseSig[0],sets.pulseSig[1],sets.pulseSig[2]-sets.pulseSig[0],sets.pulseSig[3]-sets.pulseSig[1]))
		resultFile.write("<img src='"+sets.reportImages+"pulsesig.png' alt='Pulse signal'>\n")
#data transition
	success=True
	checkCable()												#wait for cable connection to be fully settled
	if cb:
		cursor.execute("UPDATE progress SET cb=1")
		dbConn.commit()
		relaisCommand(conn,6,sets.cards,1)						#interrupt cable between device and computer to switch to bluetooth mode, this takes a while to work 
	time.sleep(5)
	if cb:
		if checkBt(conn):
			resultFile.write("<p style='color:green;'>cable to bluetooth ok</p>\n")
		else:
			resultFile.write("<p style='color:red;'>cable to bluetooth not ok</p>\n")
			success=False
		pag.screenshot(sets.reportImages+"c2b.png",region = (sets.dataTrans[0],sets.dataTrans[1],sets.dataTrans[2]-sets.dataTrans[0],sets.dataTrans[3]-sets.dataTrans[1]))
		resultFile.write("<img src='"+sets.reportImages+"c2b.png' alt='kabel naar bluetooth'>\n")
		relaisCommand(conn,7,sets.cards,1)							#reconnect cable
		if checkCable(): 
			resultFile.write("<p style='color:green;'>bluetooth to cable ok</p>\n")
		else:
			resultFile.write("<p style='color:red;'>bluetooth to cable not ok</p>\n")
			success=False
		pag.screenshot(sets.reportImages+"b2c.png",region = (sets.dataTrans[0],sets.dataTrans[1],sets.dataTrans[2]-sets.dataTrans[0],sets.dataTrans[3]-sets.dataTrans[1]))
		resultFile.write("<img src='"+sets.reportImages+"b2c.png' alt='bluetooth naar kabel'>\n")
	if success:
		cursor.execute("UPDATE progress SET cb=2")
	else:
		cursor.execute("UPDATE progress SET cb=3")
	dbConn.commit()
#impedence check
	success=True
	if impRef:
		cursor.execute("UPDATE progress SET impRef=1")
		dbConn.commit()
		time.sleep(3)
		#start impedence measurement
		pag.click(x=sets.impedance[0],y=sets.impedance[1])
		time.sleep(10)
		#reference input not shorted
		pag.click(x=sets.dropdownImpedance[0],y=sets.dropdownImpedance[1])		#switch to reference input screen
		time.sleep(1)
		pag.click(x=sets.reference[0],y=sets.reference[1])
		relaisCommand(conn,3,sets.cards,6)						#set relais to voltage divider
		wait = 0
		test=True
		cursor.execute("SELECT x1, y1, x2, y2 FROM impedancecoordinates WHERE inputId IN (SELECT DISTINCT inputId FROM inputs WHERE testId = "+str(testID)+") ORDER BY inputId;")
		result = cursor.fetchall()
		cursor.execute("SELECT inputName FROM inputs where  testId = "+str(testID)+" ORDER BY inputId;")
		names = cursor.fetchall()
		value = readValue(result[0][0],result[0][1],result[0][2],result[0][3],sets.reportImages+names[0][0]+"_NS.png")
		while not value>sets.minBigImpedence:					#impedence should be big
			wait += 1
			time.sleep(1)
			if wait >= sets.maxWait:							#waited to long, decide test was unsuccesfull
				test=False
				break
			value = readValue(result[0][0],result[0][1],result[0][2],result[0][3],sets.reportImages+names[0][0]+"_NS.png")
		if test: 
			referenceNotShorted = True
			resultFile.write("<p style='color:green;'>referentie input impedance not shorted ok</p>\n")
		else:
			resultFile.write("<p style='color:red;'>referentie input impedance not shorted not ok</p>\n")
			success=False
		resultFile.write("<img src='"+sets.reportImages+names[0][0]+"_NS.png' alt='impedantiemeting'>\n")
		#reference input shorted
		relaisCommand(conn,7,sets.cards,4)						#set relais to short
		value = readValue(result[0][0],result[0][1],result[0][2],result[0][3],sets.reportImages+names[0][0]+"_S.png")
		test = False
		for i in range(sets.maxWait):							#try a coulple of times to give time to settle
			if (value<=sets.maxSmallImpedence and value !=-1):
				stable = True
				for i in range(sets.stableImpedence):			#stay stable on correct value for some time
					if not (value<=sets.maxSmallImpedence and value !=-1):
						stable = False
						break
					value = readValue(result[0][0],result[0][1],result[0][2],result[0][3],sets.reportImages+names[0][0]+"_S.png")
					time.sleep(1)
				if stable:
					resultFile.write("<p style='color:green;'>reference input shorted ok</p>\n")
					test=True
					break
			time.sleep(1)
			value = readValue(result[0][0],result[0][1],result[0][2],result[0][3],sets.reportImages+names[0][0]+"_S.png")
		if not test:										#test unsuccesfull
			resultFile.write("<p style='color:red;'>reference input shorted not ok</p>\n")
			success=False
		resultFile.write("<img src='"+sets.reportImages+names[0][0]+"_S.png' alt='impedantiemeting'>\n")
	if success:
		cursor.execute("UPDATE progress SET impRef=2")
	else:
		cursor.execute("UPDATE progress SET impRef=3")
	dbConn.commit()
	success=True
	if impAct:
		cursor.execute("UPDATE progress SET impAct=1")
		dbConn.commit()
		#active input not shorted
		pag.click(x=sets.dropdownImpedance[0],y=sets.dropdownImpedance[1])		#switch to reference input screen
		time.sleep(0.5)
		pag.click(x=sets.active[0],y=sets.active[1])
		relaisCommand(conn,6,sets.cards,4)					#switch relais to voltage divider mode
		conn.read(100)										#empty relais buffer
		for i in range(1,len(result)):						#for every input
			wait = 0
			test=True
			value = readValue(result[i][0],result[i][1],result[i][2],result[i][3],sets.reportImages+names[i][0]+"_NS.png") 
			while not value>sets.minBigImpedence:
				wait += 1
				time.sleep(1)
				if wait >= sets.maxWait:					#waited to long, decide it doesn't work
					test=False
					break
				value = readValue(result[i][0],result[i][1],result[i][2],result[i][3],sets.reportImages+names[i][0]+"_NS.png")
			if test:
				resultFile.write("<p style='color:green;'>active input "+names[i][0]+" not shorted ok</p>\n")
			else:
				resultFile.write("<p style='color:red;'>active input "+names[i][0]+" not shorted not ok</p>\n")
				success=False
		resultFile.write("<img src='"+sets.reportImages+names[i][0]+"_NS.png' alt='impedantiemeting'>\n")
		conn.read(4)
		#active inputs shorted
		relais = 4											#first relais on this card are for other purposes
		card = sets.cards									#weird order in cards because one doesn't fully work, will get fixed
		relaisCommand(conn,7,sets.cards,2)					#switch from voltage divider to shorted
		conn.read(4)										#clear buffer
		for i in range(1,len(result)):
			#print("loop1")
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
			value = readValue(result[i][0],result[i][1],result[i][2],result[i][3],sets.reportImages+names[i][0]+"_S.png")
			test = False
			for j in range(sets.maxWait):					#try a coulple of times to give time to settle
				#print("loop2")
				if (value<=sets.maxSmallImpedence and value !=-1):
					stable = True
					for k in range(sets.stableImpedence):	#stay stable on correct value for some time
						print("loop",k)
						value = readValue(result[i][0],result[i][1],result[i][2],result[i][3],sets.reportImages+names[i][0]+"_S.png")
						if not (value<=sets.maxSmallImpedence and value !=-1):
							stable = False
							break
						time.sleep(1)
					if stable:
						resultFile.write("<p style='color:green;'>active input "+names[i][0]+" shorted ok</p>")
						test = True
						print("break loop")
						break
					else:
						print("dont't break loop")
				time.sleep(1)
				value = readValue(result[i][0],result[i][1],result[i][2],result[i][3],sets.reportImages+names[i][0]+"_S.png")
			if not test:
				resultFile.write("<p style='color:red;'>active input "+names[i][0]+" shorted not ok</p>")
				success=False
			resultFile.write("<img src='"+sets.reportImages+names[i][0]+"_S.png' alt='impedantiemeting'>")
		if success:
			cursor.execute("UPDATE progress SET impAct=2")
		else:
			cursor.execute("UPDATE progress SET impAct=3")
		dbConn.commit()
	#close the impedence window
	pag.click(x=sets.impedance[0],y=sets.impedance[1])
	time.sleep(1)
	#close current measurement
	os.system("taskkill /f /im BrtTask.exe")
	time.sleep(10)
#signal check and oxymeter check
	#set signal on function generator
	success=True
	if sig:
		cursor.execute("UPDATE progress SET sig=1")
		dbConn.commit()
		afg.write("FUNCTION SIN")
		afg.write("FREQUENCY "+str(sets.frequency))
		afg.write("VOLTAGE:UNIT VPP")
		afg.write("OUTPUT:IMP INF")
		afg.write("VOLTAGE:AMPLITUDE "+str(sets.amplitude)) #voltage divider makes it 1000 times smaller
		afg.write('OUTPUT1 on')
		#let signal go trough for every input by switching all necessary relais
		conn.read()
		relaisCommand(conn,3,sets.cards,250)
		conn.read(100)
		for i in range(1,sets.cards):
			relaisCommand(conn,6,i,255)
			print(conn.read(4))
		#start new measurement to get clean data, because some other measurements stop during impedance check
		relaisCommand(conn,6,sets.cards,1)	#turn usb on and off again
		time.sleep(0.2)
		relaisCommand(conn,7,sets.cards,1)
		startMeasurement()
		time.sleep(15)										    #let it run long enough to get enough datapoints
		pag.screenshot(sets.reportImages+"signal_ref0.png")						#screenshot for in report
		pag.screenshot(sets.reportImages+"oxymeter.png",region = (sets.oxymeter[0],sets.oxymeter[1],sets.oxymeter[2]-sets.oxymeter[0],sets.oxymeter[3]-sets.oxymeter[1]))
		#close current measurement
		os.system("taskkill /f /im BrtTask.exe")
		time.sleep(15)										#give program some time to shut down
		path = getPath()
	if oxy:
		cursor.execute("UPDATE progress SET oxy=1")
		dbConn.commit()
		result = oxyMeter(path)
		print("oxymeter:", result)
		if result[0] > 97.0 and result[0] < 99.0 and result[1] > 78.0 and result[1] < 82.0:
			resultFile.write("<p style='color:green;'>oxymeter values ok</p>\n")
			cursor.execute("UPDATE progress SET oxy=2")
			dbConn.commit()
		else:
			resultFile.write("<p style='color:red;'>oxymeter values not ok</p>\n")
			cursor.execute("UPDATE progress SET oxy=3")
			dbConn.commit()
		resultFile.write("<img src='"+sets.reportImages+"oxymeter.png' alt='oxymeter waarden'>\n")
	
	if sig:
		result = np_fft(path,cursor,False)	
		cursor.execute("SELECT inputName FROM inputs where  testId = "+str(testID)+" ORDER BY inputId;")
		names = cursor.fetchall()
		index = 1
		ampl= (sets.amplitude/2)*1000
		for item in result:
		#TODO: fixen wat die 4 moet zijn, nog geen idee hoe, misschien gewoon subtiel weglaten?
			#print(item)
			#print(len(item[0])==1,item[0][0] == 10,item[1]>=ampl-0.05*ampl,item[1]<=ampl+0.05*ampl)
			if (len(item[0])==1 and item[0][0] == 10 and item[1]>=ampl-0.05*ampl and item[1]<=ampl+0.05*ampl):
				resultFile.write("<p style='color:green;'>reference signal "+names[index][0]+" ok</p>\n")
			else:
				resultFile.write("<p style='color:red;'>reference signal "+names[index][0]+" not ok</p>\n")
				success=False
			index+=1
	os.system("taskkill /f /im ShellPlus.exe")
	if sig:
		resultFile.write("<img src='"+sets.reportImages+"signal_ref0.png' alt='referentie signaal' width='90%'>\n")
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
				pag.screenshot(sets.reportImages+"signal_ref"+str(i)+".png")
				resultFile.write("<img src='"+sets.reportImages+"signal_ref"+str(i)+".png' alt='referentie signaal' width='90%'>\n")
				os.system("taskkill /f /im BrtTask.exe")
				time.sleep(5)
				os.system("taskkill /f /im ShellPlus.exe")
				time.sleep(10)
			else:
				break
	if success:
		cursor.execute("UPDATE progress SET sig=2")
	else:
		cursor.execute("UPDATE progress SET sig=3")
	dbConn.commit()
#signal check bip
	success=True
	if sigBip:
		cursor.execute("UPDATE progress SET sigBip=1")
		dbConn.commit()
		#move the correct protocol to the folder to use it
		os.system("taskkill /f /im ShellPlus.exe")
		time.sleep(3)					#give program some time to shut down
		#empty map where protocols are stored and only put needed protocols in there
		emptyFolder()
		cursor.execute("SELECT inputName FROM inputs where bip = 1 AND testId = "+str(testID)+" ORDER BY inputId;")
		names = cursor.fetchall()
		ampl = (sets.amplitude/2)*1000
		for protocol in protocols:
			if "bip" in protocol[0]:
				cursor.execute("SELECT protocolId FROM protocols where  fileName = '"+protocol[0]+"';")
				bipId = cursor.fetchall()[0][0]
				moveForUse(protocol[0])
				#open Shell+ again and wait for it to start up properly
				Popen(sets.pathToShellPlus)
				time.sleep(15)
				#start new measurement
				startMeasurement()
				time.sleep(5)
				pag.screenshot(sets.reportImages+"signal_bip0.png")
				os.system("taskkill /f /im BrtTask.exe")
				time.sleep(15)
				os.system("taskkill /f /im ShellPlus.exe")
				time.sleep(3)
				result = np_fft(getPath(),cursor,True)
				index = 0
				for item in result:
				#TODO: check of die 4 wel klopt
					print(item)
					#print(len(item[0])==1,item[0][0] == 10,item[1]>=ampl-0.05*ampl,item[1]<=ampl+0.05*ampl,len(item[0])==1 and item[0] == 10 and item[1]>=ampl-0.05*ampl and item[1]<=ampl+0.05*ampl)
					if len(item[0])==1 and item[0][0] == 10 and item[1]>=ampl-0.05*ampl and item[1]<=ampl+0.05*ampl:
						resultFile.write("<p style='color:green;'>bipolar signal "+names[index][0]+" ok</p>\n")
					else:
						resultFile.write("<p style='color:red;'>bipolar signal "+names[index][0]+" not ok</p>\n")
						success=False
					index+=1
				resultFile.write("<img src='"+sets.reportImages+"signal_bip0.png' alt='bipolair signaal' width='90%'>\n")
				break
		for i in range(bipId+1,len(protocols)):
			emptyFolder()
			moveForUse(protocols[i][0])
			Popen(sets.pathToShellPlus)
			time.sleep(15)
			startMeasurement()
			time.sleep(3)
			pag.screenshot("reports/images/signal_bip"+str(i)+".png")
			resultFile.write("<img src='"+sets.reportImages+"signal_bip"+str(i)+".png' alt='bipolair signaal' width='90%'>\n")
			os.system("taskkill /f /im BrtTask.exe")
			time.sleep(5)
			os.system("taskkill /f /im ShellPlus.exe")
			time.sleep(10)
	if success:
		cursor.execute("UPDATE progress SET sigBip=2")
	else:
		cursor.execute("UPDATE progress SET sigBip=3")
	dbConn.commit()
	"""
#onboard sensors (comes last because a person is needed to perform these actions)
	#get back to reference test
	emptyFolder()											#empty map where protocols are stored and only put needed protocols in there
	moveForUse(protocols[0][0])
	#open Shell+ again and wait for it to start up properly
	Popen(sets.pathToShellPlus)
	time.sleep(15)
	#start new measurement
	startMeasurement()
	cursor.execute("UPDATE progress SET press=1, bodypos=1")
	dbConn.commit()
#close the serial connection, textfile, database connection and cursor on database
	conn.close()
	resultFile.close()										#close the file without closing the body, because some more info is added at the end (about bodypos and pressure sensors)
	cursor.close()
	dbConn.close()
main()