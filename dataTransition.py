from relaisCommand import relaisCommand
import pyautogui as pag
from python_imagesearch.imagesearch import imagesearch
import time
import settings as sets

def checkBt(conn):
	for i in range(sets.maxWait):							#try for some time, if it takes to long, decide i doesn't work
		x,y = imagesearch("./images/bluethoot.png")				#find the correct pixel
		if x!= -1:
			s = pag.screenshot()
			color = s.getpixel((x,y))
			if color[0]<5 and color[1]>130 and color[2]<5:	#values close to the green color used
				print("cable ok")							#for debugging
				return True	
		time.sleep(1)
	return False

def checkCable():
	for i in range(sets.maxWait):							#try for some time, if it takes to long, decide i doesn't work
		x,y = imagesearch("./images/cable.png")				#find the correct pixel
		print(x,y)
		if x!= -1:
			s = pag.screenshot()
			color = s.getpixel((x,y))
			if color[0]<5 and color[1]>130 and color[2]<5:	#values close to the green color used
				print("cable ok")							#for debugging
				return True	
		time.sleep(1)
	return False											#return false if image matching failed or if color is nog correct