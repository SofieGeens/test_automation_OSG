from relaisCommand import relaisCommand
import pyautogui as pag
from python_imagesearch.imagesearch import imagesearch
import time
import settings as sets

def checkCableTobt(conn):	
	wait=0
	print("start")
	while(1):
		x,y = imagesearch("./images/bluethoot.png")
		if x!= -1:
			s = pag.screenshot()
			color = s.getpixel((x,y))
			print(x,y,color)
			if color[0]<5 and color[1]>130 and color[2]<5: #values close to the green color used, 
				print("cable to bt ok")
				relaisCommand(conn,7,sets.cards,1) #reconnect cable
				#wait for switch back to cable, should be quick
				wait=0
				while(1):
					x,y = imagesearch("./images/cable.png")
					if x!= -1:
						s = pag.screenshot()
						color = s.getpixel((x,y))
						if color[0]<5 and color[1]>130 and color[2]<5: #values close to the green color used, 
							break
					if wait>=sets.maxWait:
						print("bt to cable not ok")
						return False
					time.sleep(1)
					wait+=1
				print("bt to cable ok")
				return True
			else:
				print("wait")
				if wait>=sets.maxWait:
					print("cable to bt not ok")
					break
				time.sleep(1)
				wait+=1
