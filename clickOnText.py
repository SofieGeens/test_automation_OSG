import pytesseract
from PIL import ImageGrab #needed to take screenshot
import pyautogui as pag
import settings

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def clickOnText(text,button): #text should be without spaces 
	screenshot = ImageGrab.grab() #take a screenshot
	img = screenshot.convert('L') #make the image grayscale, easier to process

	#data contains all chars currently on the screen with their upper and lower y and left and right x coordinate
	data=pytesseract.image_to_boxes(img,output_type=pytesseract.Output.DICT) 
	#print(data)
	s=""
	#put all chars together in string s
	for ch in data['char']:
		s+=ch
	#print(s)
	i=s.find(text)
	print(i)
	if i>0:
		print(data['left'][i],data['right'][i])
		print(data['top'][i],data['bottom'][i])
		middle = [int(data['left'][i]+((data['right'][i]-data['left'][i])/2)) , int(settings.resolution[1]-(data['bottom'][i]+((data['top'][i]-data['bottom'][i])/2)))]#the x,ycoordinate of the middle of the first char of text occuring in s
		print(middle)
		if button == 'r':
			pag.click(x=middle[0],y=middle[1],button='right')
		if button == 'l':
			pag.click(x=middle[0],y=middle[1])
	else:
		print(text+" niet gevonden")