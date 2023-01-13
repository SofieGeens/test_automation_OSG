from python_imagesearch.imagesearch import imagesearch
import pyautogui as pag

def clickButton(img):
    x,y = imagesearch(img)
    #image search gives the upper left coordinate, this might nog be part of the button yet, with adding 5 pixels, we are sure to get on the button but nog past it
    x+=5
    y+=5
    if x != -1:
        #print("position : ", x, y)
        pag.click(x=x,y=y)
    else:
        print("image not found")