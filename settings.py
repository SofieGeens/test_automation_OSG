serconn = "COM4"
cards = 1 #number of cards
nop = 10  #number of possible positive inputs
nopu = 5  #number of positive inputs used
nonu = 1  #number of negative inputs used
heart = []
sat = []
pathToShellPlus = "C:\Program Files (x86)\BrainRT\ShellPlus.exe"
pathToTesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
protocolsUse = "C:\ProgramData\OSG\BrainRT\Config\Recording Templates"
protocolsStorage = "C:\ProgramData\OSG\BrainRT\Config\Protocol Storage"
sampleFolder = "C:\ProgramData\OSG\BrainRT\Config\Protocol Storage\Samples"
protocolFiles = {"morpheus_bip":"Validation Morpheus v3 bip.XML","morpheus_ref":"Validation Morpheus v3 ref.xml"}
protocolNames = {"morpheus_bip":"Validation Morpheus v3 bip","morpheus_ref":"Validation Morpheus v3 ref"}
#-------------------------------------------------------------------------------------------
#monitor settings
m_width=[]
m_height=[]
m_x=[]
from screeninfo import get_monitors
for m in get_monitors():
	m_width.append(m.width)
	m_height.append(m.height)
	m_x.append(m.x)