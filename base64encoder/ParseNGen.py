import os
import base64
import sys
import fnmatch
import xml.etree.ElementTree as etree

def wrapenvelop(file):
    envelop = """<?xml version="1.0" encoding="windows-1251"?>
<sen:SigEnvelope xmlns:sen="urn:cbr-ru:dsig:env:v1.1">
  <sen:SigContainer>
    <dsig:MACValue xmlns:dsig="urn:cbr-ru:dsig:v1.1">
MIIBZAYJKoZIhvcNAQcCoIIBVTCCAVECAQExDzANBgkrBgEEAZxWAQEFADALBgkqhkiG9w0BBwExggEsMIIBKAIBATBYMEQxCzAJBgNVBAYTAlJVMQswCQYDVQQIEwI5MjEMMAoGA1UEChMDQ0JSMQ0wCwYDVQQLEwRVQlpJMQswCQYDVQQDEwJDQQIQQDYQt/rw+WD1wOpbVRJXIjANBgkrBgEEAZxWAQEFAKBpMBgGCSqGSIb3DQEJAzELBgkqhkiG9w0BBwEwHAYJKoZIhvcNAQkFMQ8XDTE1MTExMzEyMjg0MlowLwYJKoZIhvcNAQkEMSIEIFBE+hJr2LIjgK0VgfXh7KiP1Hir6aS/xZZnRhgzBl/0MA0GCSsGAQQBnFYBAgUABED9KjkOx14/ViJGtE84yxlNnBoHXu3D/TIxNecdP4/v7HEp1+BqXyW86AWbGozD9GRoFnOnTYT1e7ffOV8jxjnK</dsig:MACValue>
  </sen:SigContainer>
  <sen:Object>
%(encodedfile)s
</sen:Object>
</sen:SigEnvelope> """ %{'encodedfile': file}
    return envelop

def walkTrough(root, wholeroot, name, foldername):
    name = name + '_' + root.tag.replace('{urn:cbr-ru:ed:v2.0}', '') 
    for attr in root.attrib:
        atholder = root.attrib[attr]
        print('       ' + str(attr))
        root.attrib[attr] = 'ERROR'
        ef = open(foldername + '/' +name + '_' + attr + '.xml', 'wb')
        encodedfile = base64.b64encode(etree.tostring(wholeroot, encoding='windows-1251'))
        envelop = wrapenvelop(str(encodedfile).replace("b'", '').replace("'", ''))
        ef.write(bytes(envelop, 'windows-1251'))
        ef.close()
        root.attrib[attr] = atholder
    for child in root:
        print(' ' + str(child.tag.replace('{urn:cbr-ru:ed:v2.0}', '')))
        walkTrough(child, wholeroot, name, foldername)

def parseNGen(xfile):
    print('Разбор ' + param)
    tree = etree.parse(param)
    root = tree.getroot()
    foldername = param.replace('.xml', '')
    os.mkdir(foldername)
    print(root.tag.replace('{urn:cbr-ru:ed:v2.0}', ''))
    walkTrough(root, root, param, foldername)
    

if __name__ == "__main__":
    for param in sys.argv:
        if fnmatch.fnmatch(param, '*.py'):
            print('Сам скрипт передал себя параметром')
        else:
            parseNGen(param)

