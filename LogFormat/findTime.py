import sys
import os
import fnmatch
import re

FILENAME = 'console.log'
TIME = 60000

def format(filename):
	counter = 0
	file = open(filename, 'r',encoding='utf-8')
	outputfile = open('TIME' + filename, 'w')

	for line in file:
		counter += 1
		finds = re.findall('took \d* ms',line)
		for val in finds:
			ms = re.findall(' \d* ',val)
			if int(ms[0]) > TIME:
				print(val)
				outputfile.writelines(val + ' line = ' + str(counter) + '\n')
	outputfile.close()

if __name__ == "__main__":
	for file in sys.argv:
		if fnmatch.fnmatch(file, '*.log'):
			print(file)
			format(file)
