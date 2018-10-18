import os
import base64
import sys
import fnmatch
import xml.etree.ElementTree as etree
from random import randrange

TOTAL = 5
EDNO = 5000
ESIDNO = 6000
ACCDOCNO = 50
FOLDER_NAME = 'ED101_25042018'


def walkTrough(root, number):
	global EDNO
	global ESIDNO
	global ACCDOCNO
	tag_name = root.tag.replace('{urn:cbr-ru:ed:v2.0}', '').replace('{urn:cbr-ru:v2.0}', '')
	print(tag_name)
	if tag_name in ['PacketEPD', 'ED101', 'ED503','PacketEID','ED114','ED113','ED107']:
		EDNO += 1
		root.attrib['EDNo'] = str(EDNO)
		root.attrib['xmlns'] = 'urn:cbr-ru:ed:v2.0'
		root.attrib['Sum'] = str(randrange(9999))
		print(EDNO)
	if tag_name == 'AccDoc':
		root.attrib['AccDocNo'] = str(ACCDOCNO)
		ACCDOCNO += 1
	if tag_name == 'Purpose':
		root.text = 'Оплата по договору номер ' + str(number)
	if tag_name in ['ED205', 'ED206']:
		ESIDNO += 1
		root.attrib['EDNo'] = str(ESIDNO)
		root.attrib['xmlns'] = 'urn:cbr-ru:ed:v2.0'
	if tag_name in ['EDRefID']:
		EDNO += 1
		root.attrib['EDNo'] = str(EDNO)
	for child in root:
		print(' ' + str(child.tag.replace('{urn:cbr-ru:ed:v2.0}', '')))
		walkTrough(child, number)


def parseNGen(xfile):
    os.mkdir(FOLDER_NAME)
    print('Разбор ' + xfile)
    tree = etree.parse(xfile)
    root = tree.getroot()
    ef = open(FOLDER_NAME + FILE_NAME + '.xml', 'wb')
    xml_string = bytearray(b'')
    for number in range(TOTAL):
    	print(root.tag.replace('{urn:cbr-ru:ed:v2.0}', ''))
    	walkTrough(root, number)
    	xml_string += etree.tostring(root, encoding='windows-1251')
    ef.write(xml_string)
    ef.close()


if __name__ == "__main__":
	if sys.argv[2]:
		FOLDER_NAME = sys.argv[2]
	if sys.argv[3]:
		TOTAL = int(sys.argv[3])
	if sys.argv[4]:
		EDNO = int(sys.argv[4])
	if sys.argv[1]:
		FILE_NAME = '/'+FOLDER_NAME
		parseNGen(sys.argv[1])

            