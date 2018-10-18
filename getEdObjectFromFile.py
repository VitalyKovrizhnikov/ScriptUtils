import os
import base64
import sys
import fnmatch
import xml.etree.ElementTree as etree

EDNO = 5000
OBJECT = '<Empty/>'
DICTION_MODE = 1


def parseED574(root):
	global DICTION_MODE
	global EDNO
	tag_name = root.tag.replace('{urn:cbr-ru:ed:v2.0}', '')
	if tag_name in ['ED574']:
		DICTION_MODE = root.attrib['DictionMode']
		EDNO = root.attrib['EDNo']
	else:
		print(tag_name)

def parseObject(root):
	global OBJECT
	tag_name = root.tag.replace('{urn:cbr-ru:dsig:env:v1.1}', '')
	if tag_name in ['Object']:
		OBJECT = str(base64.b64decode(root.text.encode()), encoding='windows-1251').replace("b'", '').replace("'", '').replace('\\n','')
	else:
		print(tag_name)
	for child in root:
		parseObject(child)

def getEdObjectFromFile(xfile):
	global DICTION_MODE
	global EDNO
	global OBJECT
	tree = etree.parse(xfile)
	root = tree.getroot()
	parseObject(root)
	if OBJECT != '<Empty/>':
		root = etree.fromstring(OBJECT)
		parseED574(root)
		ef = open('ED574_DM_' + DICTION_MODE + '_' + EDNO + '.xml', 'wb')
		xml_string = etree.tostring(root, encoding='windows-1251')
		ef.write(xml_string)
		ef.close()

if __name__ == "__main__":
	if sys.argv[1]:
		getEdObjectFromFile(sys.argv[1])