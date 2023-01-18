from relaisCommand import relaisCommand
import pyautogui as pag
from python_imagesearch.imagesearch import imagesearch

def checkCableTobt(conn):	
	ok = False
	x,y = imagesearch("./images/bluethoot.png")
	if x!= -1:
		s = pag.screenshot()
		color = s.getpixel((x,y))
		print(color)
		if color[0]<5 and color[1]>130 and color[2]<5: #values close to the green color used, 
			ok = True
			print("cable to bt")
	if ok:
		relaisCommand(conn,7,1,1) #reconnect cable
		#wait for switch back to cable, should be quick
		while(1):	
			x,y = imagesearch("./images/cable.png")
			if x!= -1:
				s = pag.screenshot()
				color = s.getpixel((x,y))
				if color[0]<5 and color[1]>130 and color[2]<5: #values close to the green color used, 
					break
		print("bt to cable ok")
		return True
	else:
		return False