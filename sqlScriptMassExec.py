import os
import sys
import fnmatch
from subprocess import call

COMMAND = "..\serv facb01_2014 rko3 dca 123456"

def getListForLoad():
	listForLoad = []
	for param in sys.argv:
		if fnmatch.fnmatch(param, '*.SQL') or fnmatch.fnmatch(param, '*.sql'):
			listForLoad.append(param.replace('.SQL','').replace('.sql',''))
	return listForLoad


if __name__ == "__main__":
	scriptList = getListForLoad()
	loadBat = open('load.bat', 'w')
	for script in scriptList:
		loadBat.write('call %1 '+script+' %2 %3 %4 %5\n')
	loadBat.close()
	call("load.bat "+COMMAND)

	
