#!/usr/bin/python
from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.link import TCLink
from topos import RingTopo
import sys
import urllib
import json
import requests
import time

PORT = 8888
URL = 'http://localhost:8080/tee/routes/10.0.0.1/10.0.0.3'
URL_MOVE_F = 'http://localhost:8080/tee/move/{fromRoute}/{flow}/{toRoute}'

#Test constants
SWITCH_COUNT = 4
HOST_PER_SWITCH = 1
BANDWIDTH = 50

def command_wrapper(h, cmd):
    sys.stdout.write("{host} :: {cmd} ... ".format(host=h, cmd=cmd))
    sys.stdout.flush()
    h.cmd(cmd)
    sys.stdout.write("Done\n")


def main():
    net = Mininet(topo=RingTopo(k=SWITCH_COUNT, n=HOST_PER_SWITCH, lopts={"bw": BANDWIDTH}), controller=RemoteController, switch=OVSSwitch,
                  link=TCLink, autoSetMacs=True)
    print "Starting network.."
    print "Number of switches: {}".format(SWITCH_COUNT)
    print "Hosts per switch: {}".format(HOST_PER_SWITCH)
    print "Link bandwidth: {} Mb/s".format(BANDWIDTH)
    net.start()
    print "Hosts:"
    print net.hosts

    h1 = net.getNodeByName("h1")
    h3 = net.getNodeByName("h3")

    command_wrapper(h3, 'iperf -s &')
    time.sleep(10)
    command_wrapper(h1, 'iperf -t 10000 -c 10.0.0.3 -d&')

    while True:
        text = urllib.urlopen(URL).read()
        js = json.loads(text)
        print js
        if js:
            if len(js) < 2:
                continue
            r1 = js[0]
            r2 = js[1]
            break
        time.sleep(1)
        print "Retrying to read from REST API.."

    if not js[0]['flows']:
        r1, r2 = r2, r1

    r1_id = r1['id']
    r2_id = r2['id']

    g_passed = True
    for f in r1['flows']:
        url = URL_MOVE_F.format(fromRoute=r1_id, flow=f['id'], toRoute=r2_id)
        print ""
        print "Press enter to move flow id:"+str(f['id'])+" ("+f['srcIP']+" -> "+f['dstIP']+")"
        # TODO print flow description
        sys.stdin.read(1)
        r = requests.get(url)
        print "HTTP GET :: "+url
        print "Response "+str(r)

        #Verify if flows were moved
        passed = True
        text = urllib.urlopen(URL).read()
        js = json.loads(text)
        if js:
            r1n = js[0]
            r2n = js[1]
        if r1n['id'] != r1_id:
            r1, r2 = r2, r1
        # Check if flow was removed from old route
        if len([flow for flow in r1n['flows'] if flow['id'] == f['id']]) != 0:
            print "Error: flow was not removed from old route"
            passed = False
        # Check if flow was added to new route
        if len([flow for flow in r2n['flows'] if flow['id'] == f['id']]) != 1:
            print "Error: flow was not added to new route"
            passed = False
        if not passed:
            g_passed = False

    if g_passed:
        print "Test PASSED"
    else:
        print "Test FAILED"

    print ""
    print "Press enter to close ..."
    sys.stdin.read(1)
    print "Closing network"
    net.stop()


if __name__ == "__main__":
    main()
