import pyautogui as pag

def clickButton(img):
    x,y=pag.locateCenterOnScreen(img,confidence=0.9)
    pag.click(x=x,y=y)