#import librairies
import time

#import functions from other files
from clickButton import clickButton
from clickOnText import clickOnText

#start recording
clickOnText("ValidationMorpheusv3ref",'r')
time.sleep(0.5)
clickOnText("Verdermeten",'l')
time.sleep(0.5)
clickButton("images/ja.png")
time.sleep(20)
clickButton("images/record.png")

#check SaO2 signals

#data transition

#impedence check

#signal check

#onboard sensors