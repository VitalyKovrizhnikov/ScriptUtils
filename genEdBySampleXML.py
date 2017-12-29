import os
import base64
import sys
import fnmatch
import xml.etree.ElementTree as etree

TOTAL = 10000
EDNO = 5000
FOLDER_NAME = 'ED'

def walkTrough(root, number):
	tag_name = root.tag.replace('{urn:cbr-ru:ed:v2.0}', '')
	if tag_name in ['PacketEPD', 'ED101']:
		global EDNO
		EDNO += 1
		root.attrib['EDNo'] = str(EDNO)
		root.attrib['xmlns'] = 'urn:cbr-ru:ed:v2.0'
	if tag_name == 'AccDoc':
		root.attrib['AccDocNo'] = str(int(root.attrib['AccDocNo'])+1)
	if tag_name == 'Purpose':
		root.text = 'Оплата по договору номер ' + str(number)
	for child in root:
		print(' ' + str(child.tag.replace('{urn:cbr-ru:ed:v2.0}', '')))
		walkTrough(child, number)


def parseNGen(xfile):
    os.mkdir(FOLDER_NAME)
    print('Разбор ' + param)
    tree = etree.parse(param)
    root = tree.getroot()
    for number in range(TOTAL):
    	ef = open(FOLDER_NAME + '/EN101_' + str(number) + '.xml', 'wb')
    	print(root.tag.replace('{urn:cbr-ru:ed:v2.0}', ''))
    	walkTrough(root, number)
    	xml_string = etree.tostring(root, encoding='windows-1251')
    	ef.write(xml_string)
    	ef.close()


if __name__ == "__main__":
    for param in sys.argv:
        if fnmatch.fnmatch(param, '*.py'):
            print('Сам скрипт передал себя параметром')
        else:
            parseNGen(param)