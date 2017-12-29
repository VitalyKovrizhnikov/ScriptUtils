import os
import base64
import sys
import fnmatch

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

if __name__ == "__main__":
    for param in sys.argv:
        if fnmatch.fnmatch(param, '*.py'):
            print('Сам скрипт передал себя параметром')
        else:
            print('Разбор ' + param)
            f = open(param, 'rb')
            ef = open(param + '.b64.xml', 'wb')
            envelop = wrapenvelop(str(base64.b64encode(f.read())).replace("b'", '').replace("'", ''))
            ef.write(bytes(envelop, 'windows-1251'))
            ef.close()
            f.close()
                
        
        

