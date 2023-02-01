import cv2
import numpy as np

def findImage(template,findIn,simularity):
	img = cv2.imread(findIn)
	#convert to grayscale
	img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	#image matching
	result = cv2.matchTemplate(img,templ,cv2.TM_CCOEFF_NORMD)

	min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
	if max_val>simularity:
		return True
	else:
		return False