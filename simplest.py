#!/usr/bin/python


import njelib
import sys


if len(sys.argv) < 4:
    print (sys.argv[0], "RHOST OHOST ip [password]")
    sys.exit()

print ("[+] RHOST:", sys.argv[1])
print ("[+] OHOST:", sys.argv[2])
print ("[+] IP   :", sys.argv[3])
port = 175
if len(sys.argv) > 4:
    print ("[+] Port  :", sys.argv[4])
    port = int(sys.argv[4])
else:
    port = 175

if len(sys.argv) > 5:
    print ("[+] Pass  :", sys.argv[5])
    password = sys.argv[5]
else:
    password = ''



# nje.set_debuglevel(1)
nje = njelib.NJE(sys.argv[1],sys.argv[2])
while True:
    try:
        t = nje.session(host=sys.argv[3],port=port, timeout=2,password=password)            
        commandToTest = str(input("Provide command: ")).strip()
        nmr = nje.sendCommand(commandToTest) 
        nje.disconnect()
        print(nmr)
    except KeyboardInterrupt:
        print("KEYBOARD INTERRUPT")
        nje.disconnect()
        break
    except Exception as e:
        print("ERROR", e)
        break
