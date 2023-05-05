import settings as sets
import os

def emptyFolder():
	files = os.listdir(sets.protocolsUse) #get all files form  the folder
	try:
		#remove the samples folder, otherwise the next step doesn't work
		os.rmdir(sets.sampleFolder)
	except:
		pass
	for f in files:
		sourcePath = os.path.join(sets.protocolsUse,f) #complete the path to include the filename
		destinationPath = os.path.join(sets.protocolsStorage,f)
		os.rename(sourcePath,destinationPath)

def moveForUse(fname):
	sourcePath = os.path.join(sets.protocolsStorage,fname)
	destinationPath = os.path.join(sets.protocolsUse,fname)
	os.rename(sourcePath,destinationPath)