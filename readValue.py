import pytesseract
import numpy as np
import settings as sets
from PIL import Image, ImageGrab, ImageEnhance

pytesseract.pytesseract.tesseract_cmd = sets.pathToTesseract

def readValue(x1,y1,x2,y2):	
	screenshot = ImageGrab.grab(bbox =(x1,y1,x2,y2), include_layered_windows=False)
	img = screenshot.convert('L')	 #make the image grayscale to make ocr easier
	width = int(img.shape[1] * 2)
	height = int(img.shape[0] * 2)
	dimention = (width, height)
	# resize image
	resized = cv2.resize(img, dimention)
	contraster = ImageEnhance.Contrast(img)
	img = contraster.enhance(2.5)		 #increase contrast to make ocr easier
	#img.show()
	d=np.array(img)
	for x in range(img.width):
		for y in range(img.height):
			if img.getpixel((x,y))>50:
				img.putpixel((x,y),255)
	contraster = ImageEnhance.Contrast(img)
	img.save("tmp.png")
	result = pytesseract.image_to_string(img, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
	print(result)
	try:
		return int(result)
	except:
		print(-1)
		return -1