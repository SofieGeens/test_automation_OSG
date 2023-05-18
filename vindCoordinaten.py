import pyautogui as pag
import time

pag.PAUSE=5
pag.FAILSAFE=True

while(1):
    x,y=pag.position()
    print(x,y)
    time.sleep(0.5)