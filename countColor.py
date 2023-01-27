from PIL import Image
from PIL import ImageGrab

def countGreen(x1,y1,x2,y2):
	img = ImageGrab.grab(bbox =(x1,y1,x2,y2), include_layered_windows=False)
	count = 0
	for x in range(img.width):
		for y in range(img.height):
			color = img.getpixel((x,y))
			if color[0]<100 and color[1]>100:
				count+=1
	return count
def countRed(x1,y1,x2,y2):
	img = ImageGrab.grab(bbox =(x1,y1,x2,y2), include_layered_windows=False)
	count = 0
	for x in range(img.width):
		for y in range(img.height):
			color = img.getpixel((x,y))
			if color[0]>150 and color[1]<100:
				count+=1
	return count