import easyocr
import numpy as np
import settings as sets
from PIL import Image, ImageGrab, ImageEnhance

#pytesseract.pytesseract.tesseract_cmd = sets.pathToTesseract

def readValue(x1,y1,x2,y2,ocr):
	screenshot = ImageGrab.grab(bbox =(x1,y1,x2,y2), include_layered_windows=False)
	img = screenshot.convert('L')	 #make the image grayscale to make ocr easier
	w,h = img.size
	dimention = (w*3, h*3)
	# resize image
	resized = img.resize(dimention)		#double image size to get optimal height for ocr (30 pixels)
	contraster = ImageEnhance.Contrast(resized)
	img = contraster.enhance(2.5)		 #increase contrast to make ocr easier
	#img.show()
	d=np.array(img)
	for x in range(img.width):
		for y in range(img.height):
			if img.getpixel((x,y))>50:
				img.putpixel((x,y),255)
	img.save("tmp.png")
	result = ocr.readtext(img)
	print(result[0][1])
	try:
		return int(result[0][1])
	except:
		print(-1)
		return -1