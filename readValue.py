import easyocr
import numpy as np
import settings as sets
from PIL import Image, ImageGrab, ImageEnhance

pytesseract.pytesseract.tesseract_cmd = sets.pathToTesseract

def readValue(x1,y1,x2,y2,filename):
	screenshot = ImageGrab.grab(bbox =(x1,y1,x2,y2), include_layered_windows=False)
	img = screenshot.convert('L')	 #make the image grayscale to make ocr easier
	# resize image
	w,h = img.size
	dimention = (w*3, h*3)
	resized = img.resize(dimention)		#double image size to get optimal height for ocr (30 pixels)
	contraster = ImageEnhance.Contrast(resized)
	img = contraster.enhance(2.5)		 #increase contrast to make ocr easier
	#there is still a light grey circle on the background, remove it
	for x in range(img.width):			
		for y in range(img.height):
			if img.getpixel((x,y))>50:
				img.putpixel((x,y),255)
	img.save(filename)					#save the image, for debugging
	result = pytesseract.image_to_string(img, config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789')	#psm 6: assume uniform block of text, oem 3: use whatever engine mode that is available
	print(result)
	try:
		return int(result)
	except:
		#return 0 if nothing could be read
		print(-1)
		return -1