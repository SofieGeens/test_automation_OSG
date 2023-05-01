serconn = "COM11"
cards = 3 #number of cards
maxWait = 30 #maximum time to wait for something to happen before we descide it doesn't work
stableImpedence = 5 #time the value's for impedence check should be correct before test is passed
maxSmallImpedence = 1
minBigImpedence = 1000
refImp = [190,350,230,370]
x1=[85,140,190,240,295,345,400,455,505,560,610,665,85,140,190]#,240,295,345,400,455,505,560,610,665]
y1=[510,510,510,510,510,510,510,510,510,510,510,510,460,460,460]#,460,460,460,460,460,460,460,460,460]
x2=[130,180,235,285,340,390,445,495,550,600,655,710,130,180,235]#,285,340,390,445,495,550,600,655,710]
y2=[530,530,530,530,530,530,530,530,530,530,530,530,475,475,475]#,475,475,475,475,475,475,475,475,475]
channelList = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"]
pathToShellPlus = "C:\Program Files (x86)\BrainRT\ShellPlus.exe"
pathToTesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
protocolsUse = "C:\ProgramData\OSG\BrainRT\Config\Recording Templates"
protocolsStorage = "C:\ProgramData\OSG\BrainRT\Config\Protocol Storage"
sampleFolder = "C:\ProgramData\OSG\BrainRT\Config\Protocol Storage\Samples"
protocolFiles = {"morpheus_bip":"Validation Morpheus v3 bip.XML","morpheus_ref":"Validation Morpheus v3 ref.xml"}
protocolNames = {"morpheus_bip":"Validation Morpheus v3 bip","morpheus_ref":"Validation Morpheus v3 ref"}
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#monitor settings
m_width=[]
m_height=[]
m_x=[]
from screeninfo import get_monitors
for m in get_monitors():
	m_width.append(m.width)
	m_height.append(m.height)
	m_x.append(m.x)