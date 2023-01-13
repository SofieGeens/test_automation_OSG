#import librairies
import pyautogui as pag
import time
import pytesseract
#import functions from other files
from PIL import Image, ImageGrab, ImageOps, ImageEnhance
from Levenshtein import distance

import settings as sets

pytesseract.pytesseract.tesseract_cmd = sets.pathToTesseract

#text should be without spaces, options for button: 'l' for left, 'r' for right, 'm' for middle
def clickOnText(text,button): 
	#check every monitor seperatly for efficiency
	for monitor in range(len(sets.m_height)):
		x1 = sets.m_x[monitor]
		y1 = 0
		x2 = sets.m_x[monitor] + sets.m_width[monitor]
		y2 = sets.m_height[monitor]
		screenshot = ImageGrab.grab(bbox =(x1,y1,x2,y2), include_layered_windows=False, all_screens=True)	#take a screenshot
		img = screenshot.convert('L')	 #make the image grayscale to make ocr easier
		contraster = ImageEnhance.Contrast(img)
		img = contraster.enhance(2)		 #increase contrast to make ocr easier
		result = findAndClick(img,text,button,monitor)
		if result == 1:
			return result
		else:
			#try again with inverted image, this might get better results
			img = ImageOps.invert(img)
			result = findAndClick(img,text,button,monitor)
			if result == 1:
				return result
	return -1

def findAndClick(image,text,button,monitor):
	#data contains all chars currently on the screen with their upper and lower y and left and right x coordinate
	data=pytesseract.image_to_boxes(image,output_type=pytesseract.Output.DICT)
	s=""
	#put all chars together in string s
	for ch in data['char']:
		s+=ch
	#calculate the edit distance, this is slow, but ocr isn't flawless, so 1 or 2 chars can be read wrong and it will still work
	dis=5	#initiate dis as greater then 2
	i=0		#initiate index
	for j in range(len(s)-len(text)-1):
		dis=distance(s[j:j+len(text)],text)
		#print(s[j:j+len(text)-1],text,dis)
		i=j+int(len(text)/2)
		if dis<=2:
			break
	#print(i)
	if dis<=2:
		#define some variables for readability
		height= sets.m_height[monitor]
		left=data['left'][i]
		right=data['right'][i]
		top=data['top'][i]
		bottom=data['bottom'][i]

		#the coordinate of the middle of the middle char of the text, for some reason, the y-axis is pointing up in data, for other purposes y-axix is pointing down
		middle = [int(left+(right-left)/2) , int(height-(bottom+(top-bottom)/2))]
		if button == 'r':
			pag.click(x=middle[0],y=middle[1],button='right')
		if button == 'l':
			pag.click(x=middle[0],y=middle[1])
		if button == 'm':
			pag.click(x=middle[0],y=middle[1],button='middle')
		return 1
	else:
		print("text not found")
		return -1