import cv2
import numpy as np

def findImage(template,findIn,simularity):
	templ = cv2.imread(template)
	#convert to grayscale
	img = cv2.cvtColor(findIn,cv2.COLOR_BGR2GRAY)
	#image matching
	result = cv2.matchTemplate(img,templ,cv2.TM_CCOEFF_NORMED)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
	if max_val>simularity:
		return True
	else:
		return False