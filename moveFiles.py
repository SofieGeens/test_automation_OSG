import settings as sets
import os

def emptyFolder():
	files = os.listdir(sets.protocolsUse) #get all files form the folder
	try:
		#remove the samples folder, otherwise the next step doesn't work
		print("a")
		os.rmdir(sets.sampleFolder)
	except:
		print("b")
		#pass
	for f in files:
		sourcePath = os.path.join(sets.protocolsUse,f)				#complete the path to include the filename
		destinationPath = os.path.join(sets.protocolsStorage,f)
		os.rename(sourcePath,destinationPath)						#rename moves the files from sourcePath to destinationPath

def moveForUse(fname):
	sourcePath = os.path.join(sets.protocolsStorage,fname)
	destinationPath = os.path.join(sets.protocolsUse,fname)
	os.rename(sourcePath,destinationPath)							#rename moves the files from sourcePath to destinationPath