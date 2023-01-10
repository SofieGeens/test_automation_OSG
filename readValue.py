import pyautogui as pag
import cv2
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def countGreen(filename):

    img=Image.open(filename)
    width,height=img.size
    greenpxl=0
    for i in range(width):
        for j in range(height):
            color=img.getpixel((i,j))
            if(color[0]<150 and color[1]>=150 and color[2]<150):
                greenpxl+=1
    if greenpxl>0:
        print('green pixels:',greenpxl)
    return greenpxl

def readValue(x1,y1,x2,y2):
    #print('readvalue:',x1,y1,x2-x1,y2-y1)
    img=pag.screenshot('tmp.png',region=(x1,y1,x2-x1,y2-y1))
    filename='tmp.png'
    if countGreen(filename)>5:
        return 0
    img=cv2.imread(filename)
    img=cv2.bitwise_not(img)
    text=pytesseract.image_to_string(img)
    try:
        return float(text)
    except:
        return 1