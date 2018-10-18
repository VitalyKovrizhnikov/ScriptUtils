import os
import sys
import xml.etree.ElementTree as etree
from random import randrange

TOTAL = 5
EDNO = 5000
ESIDNO = 6000
ACCDOCNO = 50
FOLDER_NAME = 'ED101_25042018'

CTRL_CODE_PACK_NEW = ['1110', '1210', '2010', '2011', '2300',
'2301', '2302', '2303', '2304', '2305', '2306', '2307', '2308', '2309', 
'2312', '2313', '2314', '2315', '2316', '2317', '2318', '2320', '2321', '2322', '2323',
'2324', '2325', '2331', '2332', '2333', '2402', '2403', '2404', '2405', '2406', '2407',
'2408', '2409', '2319', '2347', '2352', '2334', '2341', '2342', '2343',
'2344', '2345', '2346', '2349', '2353', '2360', '2361', '2362', '2363', '2326', '2335', '2328', '0303',
'2329', '2336', '2338', '2339', '2348', '2351', '2364', '2366', '2367',
'2368', '2382', '2383', '0011', '0020', '2340', '2384', '2385', '2386', 
'2381', '2500', '2501', '2502', '2503', '2504', '2505', '2506', '2507',
'2508', '2509', '2510', '2511', '2512', '2513', '2514', '2515', '2516', '2517', '2518',
'2519', '2520', '2521', '2524', '2525', '2528', '2530', '2531', '2532', '2533', '2534',
'2535', '2536', '2537', '2538', '2539', '2540', '2824']


CTRL_CODE_SINGLE_NEW = ['2396', '4005', '4073', '4103', '4206',
'4822', '4823', '4863', '4983', '4984', '4992']

CTRL_CODE_PACK_114_NEW = [2204, 2205, 2206, 2827, 2828, 2829, 2832, 2858]

CTRL_CODE_NONFIC_NEW = ['0010','0011','0012','0020','0101','0102','0103','0104','0105',
'0106','0107','0109','0201','0202','0203','0204','0205','0206',
'0209','0302','0304','0305','0306','0307','0401','0402','0999',
'1100','1200','2000','2001','2002','2003','2004','2007','2100',
'2101','2323','2558','3051','3052','3053','3054','3055','3056',
'3089','3090','3091','3092','3093','3094','3095','3096','3097','3098','3099']


def walkTrough(root, number):
	global EDNO
	global ESIDNO
	global ACCDOCNO
	tag_name = root.tag.replace('{urn:cbr-ru:ed:v2.0}', '')
	if tag_name in ['PacketEPD', 'ED101', 'ED103', 'ED104', 'ED105', 'ED107', 'ED503','ED114','ED113']:
		EDNO += 1
		root.attrib['EDNo'] = str(EDNO)
		root.attrib['xmlns'] = 'urn:cbr-ru:ed:v2.0'
		root.attrib['Sum'] = str(randrange(9999))
	if tag_name == 'AccDoc':
		root.attrib['AccDocNo'] = str(ACCDOCNO)
		ACCDOCNO += 1
	if tag_name == 'Purpose':
		root.text = 'Оплата по договору номер ' + str(number)
	if tag_name in ['ED205', 'ED201', 'ED206','ED277', 'PacketEID', 'PacketESID']:
		ESIDNO += 1
		root.attrib['EDNo'] = str(ESIDNO)
		root.attrib['xmlns'] = 'urn:cbr-ru:ed:v2.0'
	if tag_name in ['ED205', 'ED201', 'ED206']:
		root.attrib['CtrlCode'] = str(number)
	if tag_name in ['EDRefID']:
		EDNO += 5
		root.attrib['EDNo'] = str(EDNO)
	for child in root:
		print(' ' + str(child.tag.replace('{urn:cbr-ru:ed:v2.0}', '')))
		walkTrough(child, number)


def parseNGen(xfile):
    os.mkdir(FOLDER_NAME)
    print('Разбор ' + xfile)
    tree = etree.parse(xfile)
    root = tree.getroot()
    for number in range(TOTAL): #CTRL_CODE_PACK_NEW: #
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
		ESIDNO = int(sys.argv[4])
	if sys.argv[1]:
		FILE_NAME = '/'+FOLDER_NAME+'_'
		parseNGen(sys.argv[1])

            