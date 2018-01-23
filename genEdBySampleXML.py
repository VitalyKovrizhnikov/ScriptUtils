import os
import base64
import sys
import fnmatch
import xml.etree.ElementTree as etree

TOTAL = 5
EDNO = 5000
ESIDNO = 6000
FOLDER_NAME = 'ED503'


def walkTrough(root, number):
	global EDNO
	global ESIDNO
	tag_name = root.tag.replace('{urn:cbr-ru:ed:v2.0}', '')
	if tag_name in ['PacketEPD', 'ED101', 'ED503','PacketEID','ED114','ED113']:
		EDNO += 1
		root.attrib['EDNo'] = str(EDNO)
		root.attrib['xmlns'] = 'urn:cbr-ru:ed:v2.0'
	if tag_name == 'AccDoc':
		root.attrib['AccDocNo'] = str(int(root.attrib['AccDocNo'])+1)
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
    for number in range(TOTAL):
    	ef = open(FOLDER_NAME + FILE_NAME + str(number) + '.xml', 'wb')
    	print(root.tag.replace('{urn:cbr-ru:ed:v2.0}', ''))
    	walkTrough(root, number)
    	xml_string = etree.tostring(root, encoding='windows-1251')
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
		FILE_NAME = '/'+FOLDER_NAME+'_'
		parseNGen(sys.argv[1])

            