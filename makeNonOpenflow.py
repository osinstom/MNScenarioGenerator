#!/usr/bin/env python
"""@package util

Changing all ovs switches named s[number] to work in legacy mode and support stp.
@author Wiktor Kujawa (wkujawa@elka.pw.edu.pl)
"""
import subprocess
import re
from sys import exit
from util import makeLegacySwitch, turnStp


def main():
    """ Turn all switches into legacy mode (non-openflow)"""
    out = subprocess.check_output(["ifconfig", "-a"])
    switches = re.findall(r'(s[0-9]*)\s+Link', out)

    if not switches:
        print "No switches found!"
        exit(1)

    for switch in switches:
        print "Disconnecting switch %s from controller" % switch
        makeLegacySwitch(switch)
        print "Turning on stp for switch %s" % switch
        turnStp(switch)

    print "Done."
    print "Be aware that switches needs few seconds to change mode and another for STP to start working."


if __name__ == "__main__":
    main()
