#!/usr/bin/python
__author__ = 'v1t3x'

from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.link import TCLink
from topos import TestTopo
import util
import time
from subprocess import call
import sys
from mininet.term import makeTerm

background_traffic = {
    't1': ('h1', [('iperf', 'hs1', '50M')]),
    't2': ('h2', [('iperf', 'hs2', '50M')]),
    't3': ('h3', [('iperf', 'hs3', '50M')])
}

actions_map = {
    't1': ('h1', [('wget', 'hs1', '1MB'), ('wget', 'hs1', '1MB'), ('wget', 'hs1', '1MB')]),
    't2': ('h2', [('wget', 'hs2', '100MB')]),
    't3': ('h3', [('sleep', '', 3), ('wget', 'hs3', '100MB')]),
}

INITIALIZATION_DELAY = 10
LEGACY_INITIALIZATION_DELAY = 20
TEST_ITERATIONS = 5
INTER_TEST_DELAY = 1


def main():
    net = Mininet(topo=TestTopo(lopts={"bw": 100}), controller=RemoteController, switch=OVSSwitch,
                  link=TCLink, autoSetMacs=True)

    print "Starting network.."
    net.start()

    if len(sys.argv) == 2 and sys.argv[1] == 'legacy':
        util.turn_legacy_on()
        print "Waiting {} s ...".format(LEGACY_INITIALIZATION_DELAY)
        time.sleep(LEGACY_INITIALIZATION_DELAY)

    server_names = ['hs1', 'hs2', 'hs3']
    host_names = []

    print "Waiting {} s for initialization of mininet and controller...".format(INITIALIZATION_DELAY)
    time.sleep(INITIALIZATION_DELAY)

    util.test_init()
    checksums = util.get_checksums()

    # Configure servers
    for hs in server_names:
        print "Configuring server " + hs
        util.launch_twistd_ftp(net, hs)
        util.launch_twistd_web(net, hs)
        util.launch_iperf(net, hs)

    for hs in host_names:
        print "Configuring hosts " + hs
        util.launch_iperf(net, hs)

    for (k, v) in background_traffic.items():
        print 'Launching background traffic with thread for {} with {}'.format(k, v)
        host_thread = util.HostThread(net, v[0])
        host_thread.set_actions(v[1])
        host_thread.start()

    # sys.stdin.read(1)

    results = []
    valid = True
    for i in xrange(TEST_ITERATIONS):
        # TODO initialize environment (for download results)
        threads = []
        start = time.time()
        for (k, v) in actions_map.items():
            print 'Launching thread for {} with {}'.format(k, v)
            host_thread = util.HostThread(net, v[0])
            host_thread.set_actions(v[1])
            threads.append(host_thread)
            host_thread.start()

        for t in threads:
            t.join()

        elapsed = time.time() - start
        results.append(elapsed)
        print "{}: elapsed time {}".format(i, elapsed)

        # TODO check correctness
        if not util.validate(checksums):
            valid = False

        if i < TEST_ITERATIONS-1:
            print "Waiting before next execution: {} s ...".format(INTER_TEST_DELAY)
            time.sleep(INTER_TEST_DELAY)

    print ''
    print "--- Test Summary ({}): ---".format("PASSED" if valid else "FAILED")
    for i in xrange(TEST_ITERATIONS):
        print "{}: {}".format(i, results[i])
    print "Avg: {}".format(sum(results) / len(results))
    print "------------------------------"
    print ''

    # makeTerm(net.getNodeByName('h1'))
    # print "Press enter.."
    # sys.stdin.read(1)

    print "Killing twistd deamons"
    call(['pkill', '-9', 'twistd'])
    call(['pkill', '-9', 'iperf'])

    # TODO stop timer
    print "Stopping network.."
    net.stop()


if __name__ == "__main__":
    main()
