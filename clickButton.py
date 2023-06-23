from python_imagesearch.imagesearch import imagesearch, imagesearcharea
import pyautogui as pag

def clickButton(img):
    x,y = imagesearch(img)
    if x != -1:
        #image search gives the upper left coordinate, this might nog be part of the button yet, with adding 5 pixels, we are sure to get on the button but nog past it
        x+=5
        y+=5
        pag.click(x=x,y=y)
        return True
    else:
        return False

def clickButtonPrecise(img):
    x,y = imagesearch(img,precision=0.95)
    if x != -1:
        #image search gives the upper left coordinate, this might nog be part of the button yet, with adding 5 pixels, we are sure to get on the button but nog past it
        x+=5
        y+=5
        pag.click(x=x,y=y)
        #print(img + " clicked on",x,y)
        return True
    else:
        #print(img + "not found")
        return False