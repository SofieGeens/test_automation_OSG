import pytesseract
import numpy as np
import settings as sets
from PIL import Image, ImageGrab, ImageEnhance

pytesseract.pytesseract.tesseract_cmd = sets.pathToTesseract

def readValue(x1,y1,x2,y2):	
	screenshot = ImageGrab.grab(bbox =(x1,y1,x2,y2), include_layered_windows=False)
	img = screenshot.convert('L')	 #make the image grayscale to make ocr easier
	contraster = ImageEnhance.Contrast(img)
	img = contraster.enhance(5)		 #increase contrast to make ocr easier
	img.show()
	d=np.array(img)
	for x in range(img.width):
		for y in range(img.height):
			if img.getpixel((x,y))>50:
				img.putpixel((x,y),255)
	contraster = ImageEnhance.Contrast(img)
	img = contraster.enhance(5)		 #increase contrast to make ocr easier
	img.save("tmp.png")
	return int(pytesseract.image_to_string(img))