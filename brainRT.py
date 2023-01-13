from subprocess import Popen
import settings

path=settings.pathToShellPlus

def openBrainRT():
	Popen(path)


def closeBrainRT():
	Popen(["taskkill","/IM","ShellPlus.exe"])
