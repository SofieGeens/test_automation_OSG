import settings as sets
import os

def emptyFolder():
	files = os.listdir(sets.protocolsUse) #get all files form the folder
	for f in files:
		sourcePath = os.path.join(sets.protocolsUse,f)				#complete the path to include the filename
		destinationPath = os.path.join(sets.protocolsStorage,f)
		try:
			os.rename(sourcePath,destinationPath)						#rename moves the files from sourcePath to destinationPath
		except:
			pass

def moveForUse(fname):
	sourcePath = os.path.join(sets.protocolsStorage,fname)
	destinationPath = os.path.join(sets.protocolsUse,fname)
	os.rename(sourcePath,destinationPath)							#rename moves the files from sourcePath to destinationPath