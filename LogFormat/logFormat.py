import sys
import os
import fnmatch

FILENAME = 'console.log'

def format(filename):
	file = open(filename, 'r',encoding='utf-8')
	outputfile = open('FORMAT' + filename, 'w')

	for line in file:
		outputfile.writelines(line.replace('INFO', '\nINFO').replace('exec ','\n\nexec ').replace('declare','\n\ndeclare').replace('[values=','\n\n[values='))
	outputfile.close()

if __name__ == "__main__":
	for file in sys.argv:
		if fnmatch.fnmatch(file, '*.log'):
			print(file)
			format(file)


