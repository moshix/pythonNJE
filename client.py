#!/usr/bin/python


import njelib
import argparse
import sys
import signal
import re
import time

# this class for screen formatting
class c:
    BLUE = '\033[94m'
    DARKBLUE = '\033[0;34m'
    PURPLE = '\033[95m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[1;37m'
    ENDC = '\033[0m'
    DARKGREY = '\033[1;30m'


    def disable(self):
        self.BLUE = ''
        self.GREEN = ''
        self.YELLOW = ''
        self.DARKBLUE = ''
        self.PURPLE = ''
        self.WHITE= ''
        self.RED = ''
        self.ENDC = ''
#####################################
# local functions 

def locSendcmd():
    test_command = "cpq n"                                                # standard NJE CP command
    nmr = nje.sendCommand(test_command)                                   # now send test command
    print (c.GREEN+"[+] "+c.YELLOW+"Reply Received:"+c.WHITE)
    print ("\n",nmr)


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


nje = njelib.NJE(sys.argv[1],sys.argv[2])
nje.set_debuglevel(1)
t = nje.session(host=sys.argv[3],port=port, timeout=2,password=password)
if t:
    # nje.dumbClient()
    locSendcmd()
    nje.disconnect()
    # Reply = nje.sendCommand("cpq n")
    # print(Reply, flush=True)
else:
    print ("[!] Error, unable to connect!")
