#!/usr/bin/python

"""
Custom topology for Mininet, generated by GraphML-Topo-to-Mininet-Network-Generator.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.node import Node
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.util import dumpNodeConnections

class BenchmarkTopo( Topo ):
    "KTR BenchmarkTopo."

    def __init__( self, **opts ):
        "Create topology."

        # Initialize Topology
        Topo.__init__( self, **opts )

        # add nodes
        # switches first
        sw1 = self.addSwitch( 's1' )
        sw2 = self.addSwitch( 's2' )
        sw3 = self.addSwitch( 's3' )
        sw4 = self.addSwitch( 's4' )
        sw5 = self.addSwitch( 's5' )
        sw6 = self.addSwitch( 's6' )

        # and now hosts
        h1 = self.addHost( 'srv1' )
        h2 = self.addHost( 'srv2' )
        h3 = self.addHost( 'cl1' )
        h4 = self.addHost( 'cl2' )
        h5 = self.addHost( 'log' )

        # add edges between switch and corresponding host
        self.addLink( sw1 , h1 )
        self.addLink( sw5 , h2 )
        self.addLink( sw6 , h3 )
        self.addLink( sw2 , h4 )
        self.addLink( sw3 , h5 )

        # add edges between switches
        self.addLink( sw1 , sw2, bw=10, delay='1ms' )
        self.addLink( sw1 , sw3, bw=10, delay='1ms' )
        self.addLink( sw2 , sw4, bw=10, delay='1ms' )
        self.addLink( sw3 , sw4, bw=10, delay='1ms' )
        self.addLink( sw3 , sw5, bw=10, delay='1ms' )
        self.addLink( sw4 , sw5, bw=10, delay='1ms' )
        self.addLink( sw4 , sw6, bw=10, delay='1ms' )
        self.addLink( sw5 , sw6, bw=10, delay='1ms' )

topos = { 'benchmark': ( lambda: BenchmarkTopo() ) }

# here the code defining the topology ends
# the following code produces an executable script working with a remote controller
# and ssh access to the the mininet hosts from within the ubuntu vm
def setupNetwork():
    "Create network and run simple performance test"
    topo = BenchmarkTopo()

    # Controller for KTR network
    net = Mininet(topo=topo, controller=lambda a: RemoteController( a, ip='141.13.92.68', port=6633 ), host=CPULimitedHost, link=TCLink)
    return net

def connectToRootNS( network, switch, ip, prefixLen, routes ):
#def connectToRootNS( network, ip, prefixLen, routes ):
    """Connect hosts to root namespace via switch. Starts network.
      network: Mininet() network object
      switch: switch to connect to root namespace
      ip: IP address for root namespace node
      prefixLen: IP address prefix length (e.g. 8, 16, 24)
      routes: host networks to route to"""
    # Create a node in root namespace and link to switch 0
    root = Node( 'root', inNamespace=False )
    #for switch in network.switches:
    intf = TCLink( root, switch ).intf1
    root.setIP( ip, prefixLen, intf )
    # Start network that now includes link to root namespace
    network.start()
    # Add routes from root ns to hosts
    for route in routes:
        root.cmd( 'route add -net ' + route + ' dev ' + str( intf ) )

def sshd( network, cmd='/usr/sbin/sshd', opts='-D' ):
    "Start a network, connect it to root ns, and run sshd on all hosts."
    ip = '10.123.123.1'  # our IP address on host network
    routes = [ '10.0.0.0/8' ]  # host networks to route to
    switch = network.switches[ 0 ]  # switch to use
    connectToRootNS( network, switch, ip, 8, routes )
    #connectToRootNS( network, ip, 8, routes )
    for host in network.hosts:
        host.cmd( cmd + ' ' + opts + '&' )
    print
    print "*** Hosts are running sshd at the following addresses:"
    print
    for host in network.hosts:
        print host.name, host.IP()
    print
    print "*** Type 'exit' or control-D to shut down network"

    print "Dumping host connections"
    dumpNodeConnections(network.hosts)
    print "Testing network connectivity"
    network.pingAll()

    ## TEST NETWORK THROUGHPUT VIA MININET'S IPERF
    #print "Testing bandwidth between srv1 and cl1"
    #h1, h2 = network.getNodeByName('srv1', 'cl1')
    #network.iperf((h1, h2))
    #network.iperf((h1, h2))
    #network.iperf((h1, h2))
    #network.iperf((h1, h2))
    #network.iperf((h1, h2))
    #network.iperf((h1, h2))
    #network.iperf((h1, h2))
    #network.iperf((h1, h2))
    #network.iperf((h1, h2))
    #network.iperf((h1, h2))
    #print "Testing bandwidth between srv2 and cl2"
    #h3, h4 = network.getNodeByName('srv2', 'cl2')
    #network.iperf((h3, h4))
    #network.iperf((h3, h4))
    #network.iperf((h3, h4))
    #network.iperf((h3, h4))
    #network.iperf((h3, h4))
    #network.iperf((h3, h4))
    #network.iperf((h3, h4))
    #network.iperf((h3, h4))
    #network.iperf((h3, h4))
    #network.iperf((h3, h4))

    CLI( network )
    for host in network.hosts:
        host.cmd( 'kill %' + cmd )
    network.stop()

if __name__ == '__main__':
    setLogLevel('info')
    #setLogLevel('debug')
    sshd( setupNetwork() )
