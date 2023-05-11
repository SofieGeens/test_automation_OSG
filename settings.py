serconn = "COM11"															#serial port to which the relais cards are connected
cards = 3																	#number of relaiscards
maxWait = 30																#maximum time to wait for something to happen before we descide it doesn't work
stableImpedence = 5															#time the value's for impedence check should be correct before test is passed
maxSmallImpedence = 1														#biggest a shorted impedence is allowed to be
minBigImpedence = 5000														#smallest a not shorted impedence is allowed to be 
frequency = 10																#all devices are tested at the same frequency
amplitude = 4																#all tests are done with the same amplitude
pathToShellPlus = "C:\Program Files (x86)\BrainRT\ShellPlus.exe"			#path needed to start shell+
pathToTesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"			#path needed to use tesseract
protocolsUse = "C:\ProgramData\OSG\BrainRT\Config\Recording Templates"		#place where the templates loaded into brainRT are stored
protocolsStorage = "C:\ProgramData\OSG\BrainRT\Config\Protocol Storage"		#place where unused protocols are saved
sampleFolder = "C:\ProgramData\OSG\BrainRT\Config\Protocol Storage\Samples"	#sample folder that needs to be deleted every time, otherwise there are problems with it
record = [25,65]															#coordinates of record button
impedence = [140,65]														#coordinates of button to start and stop impedence measurement
dropdownImpededance = [245,220]												#coordinates of where to click first to switch between reference input and active input (open dropdown menu)
reference = [245,265]														#coordinates to switch to reference input (in dropdown menu)
active = [245,245]															#coordinates to switch to active input (in dropdown menu)
start = [540,520]															#coordinates to start measurement (button without keyboard shortcut)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#monitor settings
m_width=[]
m_height=[]
m_x=[]
#from screeninfo import get_monitors
"""
for m in get_monitors():
	m_width.append(m.width)
	m_height.append(m.height)
	m_x.append(m.x)
"""