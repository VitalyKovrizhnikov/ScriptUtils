import os
import sys
import fnmatch
from subprocess import call

COMMAND = "..\serv"

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
	if sys.argv[1]:
		COMMAND += ' ' + sys.argv[1]
	if sys.argv[2]:
		COMMAND += ' ' + sys.argv[2]
	if sys.argv[3]:
		COMMAND += ' ' + sys.argv[3]
	if sys.argv[4]:
		COMMAND += ' ' + sys.argv[4]
	call("load.bat "+COMMAND)

	
