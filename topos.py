#!/usr/bin/env python
"""@package topos

Collection of network topologies.

@author Wiktor Kujawa (wkujawa@elka.pw.edu.pl)
"""

from mininet.topo import Topo


class RingTopo(Topo):
    """Ring topology with k switches and n host per switch."""

    def __init__(self, k=3, n=1, **opts):
        """Init.
            k: number of switches
            n: number of hosts per switch
            hconf: host configuration options
            lconf: link configuration options"""

        super(RingTopo, self).__init__(**opts)

        self.k = k
        self.n = n

        if n == 1:
            genHostName = lambda i, j: 'h%s' % i
        else:
            genHostName = lambda i, j: 'h%s.%s' % (i, j)

        lastSwitch = None
        firstSwitch = None
        for i in range(1, k + 1):
            # Add switch
            switch = self.addSwitch('s%s' % i)
            # Add hosts to switch
            for j in range(1, n + 1):
                host = self.addHost(genHostName(i, j))
                self.addLink(host, switch)
            if lastSwitch:
                self.addLink(switch, lastSwitch)
            if i == 1:
                firstSwitch = switch
            lastSwitch = switch
        if k > 1:
            self.addLink(lastSwitch, firstSwitch)


class TestTopo(Topo):
    """3x3 switch grid with adidtional overal X cross conection.

            S1- S6- S7---- HS1 (server)
            | \ | / | \`-- HS2 (server)
        H1- S2- S5- S8 `-- HS3 (server)
            | / | \ |
            S3- S4- S9
            |	|
            H2  H3
    """

    def __init__(self, **opts):
        """Init.
            hconf: host configuration options
            lconf: link configuration options"""

        super(TestTopo, self).__init__(**opts)

        # Add switches
        s3 = self.addSwitch('s3')
        s6 = self.addSwitch('s6')
        s9 = self.addSwitch('s9')
        s5 = self.addSwitch('s5')
        s2 = self.addSwitch('s2')
        s1 = self.addSwitch('s1')
        s8 = self.addSwitch('s8')
        s7 = self.addSwitch('s7')
        s4 = self.addSwitch('s4')

        # Add hosts
        h2 = self.addHost('h2')
        h1 = self.addHost('h1')
        h3 = self.addHost('h3')

        # Add server hosts
        hs1 = self.addHost('hs1')
        hs2 = self.addHost('hs2')
        hs3 = self.addHost('hs3')

        # Add links
        self.addLink(s1, s2)
        self.addLink(s1, s6)
        self.addLink(s6, s5)
        self.addLink(s3, s2)
        self.addLink(s4, s3)
        self.addLink(s4, s9)
        self.addLink(s9, s8)
        self.addLink(s8, s7)
        self.addLink(s7, s6)
        self.addLink(s5, s4)
        self.addLink(s2, s5)
        self.addLink(s5, s8)
        self.addLink(s1, s5)
        self.addLink(s3, s5)
        self.addLink(s9, s5)
        self.addLink(s7, s5)
        self.addLink(h1, s2)
        self.addLink(s3, h2)
        self.addLink(s4, h3)
        self.addLink(s7, hs1)
        self.addLink(s7, hs2)
        self.addLink(s7, hs3)


class TestTopo2(Topo):
    """3x3 switch grid with adidtional overal X cross conection.

                 H6
                 |
        H1- S1- S6- S7 - H7
            | \ | /H5|
        H2- S2- S5- S8 -H8
            | / | \  |
        H3- S3- S4- S9 -H9
                |
                H4
    """

    def __init__(self, **opts):
        """Init.
            hconf: host configuration options
            lconf: link configuration options"""

        super(TestTopo2, self).__init__(**opts)

        # Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        s7 = self.addSwitch('s7')
        s8 = self.addSwitch('s8')
        s9 = self.addSwitch('s9')

        # Add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')
        h7 = self.addHost('h7')
        h8 = self.addHost('h8')
        h9 = self.addHost('h9')

        # Add links
        self.addLink(s1, s2)
        self.addLink(s1, s6)
        self.addLink(s6, s5)
        self.addLink(s3, s2)
        self.addLink(s4, s3)
        self.addLink(s4, s9)
        self.addLink(s9, s8)
        self.addLink(s8, s7)
        self.addLink(s7, s6)
        self.addLink(s5, s4)
        self.addLink(s2, s5)
        self.addLink(s5, s8)
        self.addLink(s1, s5)
        self.addLink(s3, s5)
        self.addLink(s9, s5)
        self.addLink(s7, s5)

        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(h4, s4)
        self.addLink(h5, s5)
        self.addLink(h6, s6)
        self.addLink(h7, s7)
        self.addLink(h8, s8)
        self.addLink(h9, s9)


class AgisTopo( Topo ):
    "AGIS topology. 1 host per switch. http://www.topology-zoo.org/dataset.html"

    def __init__( self, **opts ):
        "Create a topology."

        # Initialize Topology
        Topo.__init__( self, **opts )

        # add nodes, switches first...
        Miami = self.addSwitch( 's1' )
        Houston = self.addSwitch( 's2' )
        Washington_DC = self.addSwitch( 's3' )
        Atlanta = self.addSwitch( 's4' )
        MexicoCity = self.addSwitch( 's5' )
        Phoenix = self.addSwitch( 's6' )
        Dallas = self.addSwitch( 's7' )
        StLouis = self.addSwitch( 's8' )
        SanDiego = self.addSwitch( 's9' )
        LosAngeles = self.addSwitch( 's10' )
        SantaClara = self.addSwitch( 's11' )
        Stockton = self.addSwitch( 's12' )
        Sacramento = self.addSwitch( 's13' )
        Fresno = self.addSwitch( 's14' )
        SanFrancisco = self.addSwitch( 's15' )
        NewYork = self.addSwitch( 's16' )
        Boston = self.addSwitch( 's17' )
        Seattle = self.addSwitch( 's18' )
        SaltLakeCity = self.addSwitch( 's19' )
        Chicago = self.addSwitch( 's20' )
        Minneapolis = self.addSwitch( 's21' )
        Detroit = self.addSwitch( 's22' )
        Pittsburg = self.addSwitch( 's23' )
        Philadelphia = self.addSwitch( 's24' )
        Pennsauken = self.addSwitch( 's25' )

        # ... and now hosts
        Miami_host = self.addHost( 'h1' )
        Houston_host = self.addHost( 'h2' )
        Washington_DC_host = self.addHost( 'h3' )
        Atlanta_host = self.addHost( 'h4' )
        MexicoCity_host = self.addHost( 'h5' )
        Phoenix_host = self.addHost( 'h6' )
        Dallas_host = self.addHost( 'h7' )
        StLouis_host = self.addHost( 'h8' )
        SanDiego_host = self.addHost( 'h9' )
        LosAngeles_host = self.addHost( 'h10' )
        SantaClara_host = self.addHost( 'h11' )
        Stockton_host = self.addHost( 'h12' )
        Sacramento_host = self.addHost( 'h13' )
        Fresno_host = self.addHost( 'h14' )
        SanFrancisco_host = self.addHost( 'h15' )
        NewYork_host = self.addHost( 'h16' )
        Boston_host = self.addHost( 'h17' )
        Seattle_host = self.addHost( 'h18' )
        SaltLakeCity_host = self.addHost( 'h19' )
        Chicago_host = self.addHost( 'h20' )
        Minneapolis_host = self.addHost( 'h21' )
        Detroit_host = self.addHost( 'h22' )
        Pittsburg_host = self.addHost( 'h23' )
        Philadelphia_host = self.addHost( 'h24' )
        Pennsauken_host = self.addHost( 'h25' )

        # add edges between switch and corresponding host
        self.addLink( Miami , Miami_host )
        self.addLink( Houston , Houston_host )
        self.addLink( Washington_DC , Washington_DC_host )
        self.addLink( Atlanta , Atlanta_host )
        self.addLink( MexicoCity , MexicoCity_host )
        self.addLink( Phoenix , Phoenix_host )
        self.addLink( Dallas , Dallas_host )
        self.addLink( StLouis , StLouis_host )
        self.addLink( SanDiego , SanDiego_host )
        self.addLink( LosAngeles , LosAngeles_host )
        self.addLink( SantaClara , SantaClara_host )
        self.addLink( Stockton , Stockton_host )
        self.addLink( Sacramento , Sacramento_host )
        self.addLink( Fresno , Fresno_host )
        self.addLink( SanFrancisco , SanFrancisco_host )
        self.addLink( NewYork , NewYork_host )
        self.addLink( Boston , Boston_host )
        self.addLink( Seattle , Seattle_host )
        self.addLink( SaltLakeCity , SaltLakeCity_host )
        self.addLink( Chicago , Chicago_host )
        self.addLink( Minneapolis , Minneapolis_host )
        self.addLink( Detroit , Detroit_host )
        self.addLink( Pittsburg , Pittsburg_host )
        self.addLink( Philadelphia , Philadelphia_host )
        self.addLink( Pennsauken , Pennsauken_host )

        # add edges between switches
        self.addLink( Miami , Atlanta)
        self.addLink( Houston , Dallas)
        self.addLink( Washington_DC , Atlanta)
        self.addLink( Washington_DC , Philadelphia)
        self.addLink( Atlanta , Dallas)
        self.addLink( Atlanta , NewYork)
        self.addLink( MexicoCity , Dallas)
        self.addLink( Phoenix , LosAngeles)
        self.addLink( Phoenix , Dallas)
        self.addLink( Dallas , StLouis)
        self.addLink( StLouis , Chicago)
        self.addLink( SanDiego , LosAngeles)
        self.addLink( LosAngeles , SantaClara)
        self.addLink( LosAngeles , Sacramento)
        self.addLink( LosAngeles , Chicago)
        self.addLink( LosAngeles , Pennsauken)
        self.addLink( SantaClara , Stockton)
        self.addLink( SantaClara , Sacramento)
        self.addLink( SantaClara , Fresno)
        self.addLink( SantaClara , SanFrancisco)
        self.addLink( SanFrancisco , Seattle)
        self.addLink( NewYork , Boston)
        self.addLink( NewYork , Philadelphia)
        self.addLink( Seattle , SaltLakeCity)
        self.addLink( Seattle , Chicago)
        self.addLink( Chicago , Detroit)
        self.addLink( Chicago , Minneapolis)
        self.addLink( Detroit , Pittsburg)
        self.addLink( Pittsburg , Philadelphia)
        self.addLink( Philadelphia , Pennsauken)


class Agis2Topo( Topo ):
    "AGIS topology. 2 hosts per switch. http://www.topology-zoo.org/dataset.html"

    def __init__( self, **opts ):
        "Create a topology."

        # Initialize Topology
        Topo.__init__( self, **opts )

        # add nodes, switches first...
        Miami = self.addSwitch( 's1' )
        Houston = self.addSwitch( 's2' )
        Washington_DC = self.addSwitch( 's3' )
        Atlanta = self.addSwitch( 's4' )
        MexicoCity = self.addSwitch( 's5' )
        Phoenix = self.addSwitch( 's6' )
        Dallas = self.addSwitch( 's7' )
        StLouis = self.addSwitch( 's8' )
        SanDiego = self.addSwitch( 's9' )
        LosAngeles = self.addSwitch( 's10' )
        SantaClara = self.addSwitch( 's11' )
        Stockton = self.addSwitch( 's12' )
        Sacramento = self.addSwitch( 's13' )
        Fresno = self.addSwitch( 's14' )
        SanFrancisco = self.addSwitch( 's15' )
        NewYork = self.addSwitch( 's16' )
        Boston = self.addSwitch( 's17' )
        Seattle = self.addSwitch( 's18' )
        SaltLakeCity = self.addSwitch( 's19' )
        Chicago = self.addSwitch( 's20' )
        Minneapolis = self.addSwitch( 's21' )
        Detroit = self.addSwitch( 's22' )
        Pittsburg = self.addSwitch( 's23' )
        Philadelphia = self.addSwitch( 's24' )
        Pennsauken = self.addSwitch( 's25' )

        # ... and now hosts
        Miami_host_0 = self.addHost( 'h1' )
        Miami_host_1 = self.addHost( 'h2' )
        Houston_host_0 = self.addHost( 'h3' )
        Houston_host_1 = self.addHost( 'h4' )
        Washington_DC_host_0 = self.addHost( 'h5' )
        Washington_DC_host_1 = self.addHost( 'h6' )
        Atlanta_host_0 = self.addHost( 'h7' )
        Atlanta_host_1 = self.addHost( 'h8' )
        MexicoCity_host_0 = self.addHost( 'h9' )
        MexicoCity_host_1 = self.addHost( 'h10' )
        Phoenix_host_0 = self.addHost( 'h11' )
        Phoenix_host_1 = self.addHost( 'h12' )
        Dallas_host_0 = self.addHost( 'h13' )
        Dallas_host_1 = self.addHost( 'h14' )
        StLouis_host_0 = self.addHost( 'h15' )
        StLouis_host_1 = self.addHost( 'h16' )
        SanDiego_host_0 = self.addHost( 'h17' )
        SanDiego_host_1 = self.addHost( 'h18' )
        LosAngeles_host_0 = self.addHost( 'h19' )
        LosAngeles_host_1 = self.addHost( 'h20' )
        SantaClara_host_0 = self.addHost( 'h21' )
        SantaClara_host_1 = self.addHost( 'h22' )
        Stockton_host_0 = self.addHost( 'h23' )
        Stockton_host_1 = self.addHost( 'h24' )
        Sacramento_host_0 = self.addHost( 'h25' )
        Sacramento_host_1 = self.addHost( 'h26' )
        Fresno_host_0 = self.addHost( 'h27' )
        Fresno_host_1 = self.addHost( 'h28' )
        SanFrancisco_host_0 = self.addHost( 'h29' )
        SanFrancisco_host_1 = self.addHost( 'h30' )
        NewYork_host_0 = self.addHost( 'h31' )
        NewYork_host_1 = self.addHost( 'h32' )
        Boston_host_0 = self.addHost( 'h33' )
        Boston_host_1 = self.addHost( 'h34' )
        Seattle_host_0 = self.addHost( 'h35' )
        Seattle_host_1 = self.addHost( 'h36' )
        SaltLakeCity_host_0 = self.addHost( 'h37' )
        SaltLakeCity_host_1 = self.addHost( 'h38' )
        Chicago_host_0 = self.addHost( 'h39' )
        Chicago_host_1 = self.addHost( 'h40' )
        Minneapolis_host_0 = self.addHost( 'h41' )
        Minneapolis_host_1 = self.addHost( 'h42' )
        Detroit_host_0 = self.addHost( 'h43' )
        Detroit_host_1 = self.addHost( 'h44' )
        Pittsburg_host_0 = self.addHost( 'h45' )
        Pittsburg_host_1 = self.addHost( 'h46' )
        Philadelphia_host_0 = self.addHost( 'h47' )
        Philadelphia_host_1 = self.addHost( 'h48' )
        Pennsauken_host_0 = self.addHost( 'h49' )
        Pennsauken_host_1 = self.addHost( 'h50' )

        # add edges between switch and corresponding host
        self.addLink( Miami , Miami_host_0 )
        self.addLink( Miami , Miami_host_1 )
        self.addLink( Houston , Houston_host_0 )
        self.addLink( Houston , Houston_host_1 )
        self.addLink( Washington_DC , Washington_DC_host_0 )
        self.addLink( Washington_DC , Washington_DC_host_1 )
        self.addLink( Atlanta , Atlanta_host_0 )
        self.addLink( Atlanta , Atlanta_host_1 )
        self.addLink( MexicoCity , MexicoCity_host_0 )
        self.addLink( MexicoCity , MexicoCity_host_1 )
        self.addLink( Phoenix , Phoenix_host_0 )
        self.addLink( Phoenix , Phoenix_host_1 )
        self.addLink( Dallas , Dallas_host_0 )
        self.addLink( Dallas , Dallas_host_1 )
        self.addLink( StLouis , StLouis_host_0 )
        self.addLink( StLouis , StLouis_host_1 )
        self.addLink( SanDiego , SanDiego_host_0 )
        self.addLink( SanDiego , SanDiego_host_1 )
        self.addLink( LosAngeles , LosAngeles_host_0 )
        self.addLink( LosAngeles , LosAngeles_host_1 )
        self.addLink( SantaClara , SantaClara_host_0 )
        self.addLink( SantaClara , SantaClara_host_1 )
        self.addLink( Stockton , Stockton_host_0 )
        self.addLink( Stockton , Stockton_host_1 )
        self.addLink( Sacramento , Sacramento_host_0 )
        self.addLink( Sacramento , Sacramento_host_1 )
        self.addLink( Fresno , Fresno_host_0 )
        self.addLink( Fresno , Fresno_host_1 )
        self.addLink( SanFrancisco , SanFrancisco_host_0 )
        self.addLink( SanFrancisco , SanFrancisco_host_1 )
        self.addLink( NewYork , NewYork_host_0 )
        self.addLink( NewYork , NewYork_host_1 )
        self.addLink( Boston , Boston_host_0 )
        self.addLink( Boston , Boston_host_1 )
        self.addLink( Seattle , Seattle_host_0 )
        self.addLink( Seattle , Seattle_host_1 )
        self.addLink( SaltLakeCity , SaltLakeCity_host_0 )
        self.addLink( SaltLakeCity , SaltLakeCity_host_1 )
        self.addLink( Chicago , Chicago_host_0 )
        self.addLink( Chicago , Chicago_host_1 )
        self.addLink( Minneapolis , Minneapolis_host_0 )
        self.addLink( Minneapolis , Minneapolis_host_1 )
        self.addLink( Detroit , Detroit_host_0 )
        self.addLink( Detroit , Detroit_host_1 )
        self.addLink( Pittsburg , Pittsburg_host_0 )
        self.addLink( Pittsburg , Pittsburg_host_1 )
        self.addLink( Philadelphia , Philadelphia_host_0 )
        self.addLink( Philadelphia , Philadelphia_host_1 )
        self.addLink( Pennsauken , Pennsauken_host_0 )
        self.addLink( Pennsauken , Pennsauken_host_1 )

        # add edges between switches
        self.addLink( Miami , Atlanta)
        self.addLink( Houston , Dallas)
        self.addLink( Washington_DC , Atlanta)
        self.addLink( Washington_DC , Philadelphia)
        self.addLink( Atlanta , Dallas)
        self.addLink( Atlanta , NewYork)
        self.addLink( MexicoCity , Dallas)
        self.addLink( Phoenix , LosAngeles)
        self.addLink( Phoenix , Dallas)
        self.addLink( Dallas , StLouis)
        self.addLink( StLouis , Chicago)
        self.addLink( SanDiego , LosAngeles)
        self.addLink( LosAngeles , SantaClara)
        self.addLink( LosAngeles , Sacramento)
        self.addLink( LosAngeles , Chicago)
        self.addLink( LosAngeles , Pennsauken)
        self.addLink( SantaClara , Stockton)
        self.addLink( SantaClara , Sacramento)
        self.addLink( SantaClara , Fresno)
        self.addLink( SantaClara , SanFrancisco)
        self.addLink( SanFrancisco , Seattle)
        self.addLink( NewYork , Boston)
        self.addLink( NewYork , Philadelphia)
        self.addLink( Seattle , SaltLakeCity)
        self.addLink( Seattle , Chicago)
        self.addLink( Chicago , Detroit)
        self.addLink( Chicago , Minneapolis)
        self.addLink( Detroit , Pittsburg)
        self.addLink( Pittsburg , Philadelphia)
        self.addLink( Philadelphia , Pennsauken)


class AbileneTopo( Topo ):
    "Abilene topology. 2 hosts per switch. http://www.topology-zoo.org/dataset.html"

    def __init__( self, **opts ):
        "Create a topology."

        # Initialize Topology
        Topo.__init__( self, **opts )

        # add nodes, switches first...
        NewYork = self.addSwitch( 's1' )
        Chicago = self.addSwitch( 's2' )
        WashingtonDC = self.addSwitch( 's3' )
        Seattle = self.addSwitch( 's4' )
        Sunnyvale = self.addSwitch( 's5' )
        LosAngeles = self.addSwitch( 's6' )
        Denver = self.addSwitch( 's7' )
        KansasCity = self.addSwitch( 's8' )
        Houston = self.addSwitch( 's9' )
        Atlanta = self.addSwitch( 's10' )
        Indianapolis = self.addSwitch( 's11' )

        # ... and now hosts
        NewYork_host_0 = self.addHost( 'h1' )
        NewYork_host_1 = self.addHost( 'h2' )
        Chicago_host_0 = self.addHost( 'h3' )
        Chicago_host_1 = self.addHost( 'h4' )
        WashingtonDC_host_0 = self.addHost( 'h5' )
        WashingtonDC_host_1 = self.addHost( 'h6' )
        Seattle_host_0 = self.addHost( 'h7' )
        Seattle_host_1 = self.addHost( 'h8' )
        Sunnyvale_host_0 = self.addHost( 'h9' )
        Sunnyvale_host_1 = self.addHost( 'h10' )
        LosAngeles_host_0 = self.addHost( 'h11' )
        LosAngeles_host_1 = self.addHost( 'h12' )
        Denver_host_0 = self.addHost( 'h13' )
        Denver_host_1 = self.addHost( 'h14' )
        KansasCity_host_0 = self.addHost( 'h15' )
        KansasCity_host_1 = self.addHost( 'h16' )
        Houston_host_0 = self.addHost( 'h17' )
        Houston_host_1 = self.addHost( 'h18' )
        Atlanta_host_0 = self.addHost( 'h19' )
        Atlanta_host_1 = self.addHost( 'h20' )
        Indianapolis_host_0 = self.addHost( 'h21' )
        Indianapolis_host_1 = self.addHost( 'h22' )

        # add edges between switch and corresponding host
        self.addLink( NewYork , NewYork_host_0 )
        self.addLink( NewYork , NewYork_host_1 )
        self.addLink( Chicago , Chicago_host_0 )
        self.addLink( Chicago , Chicago_host_1 )
        self.addLink( WashingtonDC , WashingtonDC_host_0 )
        self.addLink( WashingtonDC , WashingtonDC_host_1 )
        self.addLink( Seattle , Seattle_host_0 )
        self.addLink( Seattle , Seattle_host_1 )
        self.addLink( Sunnyvale , Sunnyvale_host_0 )
        self.addLink( Sunnyvale , Sunnyvale_host_1 )
        self.addLink( LosAngeles , LosAngeles_host_0 )
        self.addLink( LosAngeles , LosAngeles_host_1 )
        self.addLink( Denver , Denver_host_0 )
        self.addLink( Denver , Denver_host_1 )
        self.addLink( KansasCity , KansasCity_host_0 )
        self.addLink( KansasCity , KansasCity_host_1 )
        self.addLink( Houston , Houston_host_0 )
        self.addLink( Houston , Houston_host_1 )
        self.addLink( Atlanta , Atlanta_host_0 )
        self.addLink( Atlanta , Atlanta_host_1 )
        self.addLink( Indianapolis , Indianapolis_host_0 )
        self.addLink( Indianapolis , Indianapolis_host_1 )

        # add edges between switches
        self.addLink( NewYork , Chicago)
        self.addLink( NewYork , WashingtonDC)
        self.addLink( Chicago , Indianapolis)
        self.addLink( WashingtonDC , Atlanta)
        self.addLink( Seattle , Sunnyvale)
        self.addLink( Seattle , Denver)
        self.addLink( Sunnyvale , LosAngeles)
        self.addLink( Sunnyvale , Denver)
        self.addLink( LosAngeles , Houston)
        self.addLink( Denver , KansasCity)
        self.addLink( KansasCity , Houston)
        self.addLink( KansasCity , Indianapolis)
        self.addLink( Houston , Atlanta)
        self.addLink( Atlanta , Indianapolis)


class BteuropeTopo( Topo ):
    "BTEurope topology. 2 hosts per switch. http://www.topology-zoo.org/dataset.html"

    def __init__( self, **opts ):
        "Create a topology."

        # Initialize Topology
        Topo.__init__( self, **opts )

        # add nodes, switches first...
        Budapest = self.addSwitch( 's1' )
        Munich = self.addSwitch( 's2' )
        Prague = self.addSwitch( 's3' )
        Vienna = self.addSwitch( 's4' )
        Dusseldorf = self.addSwitch( 's5' )
        Frankfurt = self.addSwitch( 's6' )
        Zurich = self.addSwitch( 's7' )
        Paris = self.addSwitch( 's8' )
        Milan = self.addSwitch( 's9' )
        Barcelona = self.addSwitch( 's10' )
        Goonhilly = self.addSwitch( 's11' )
        NewYork = self.addSwitch( 's12' )
        Washington = self.addSwitch( 's13' )
        Madrid = self.addSwitch( 's14' )
        Helsinki = self.addSwitch( 's15' )
        Copenhagen = self.addSwitch( 's16' )
        London = self.addSwitch( 's17' )
        London = self.addSwitch( 's18' )
        Madley = self.addSwitch( 's19' )
        Dublin = self.addSwitch( 's20' )
        Brussels = self.addSwitch( 's21' )
        Amsterdam = self.addSwitch( 's22' )
        Gothenburg = self.addSwitch( 's23' )
        Stockholm = self.addSwitch( 's24' )

        # ... and now hosts
        Budapest_host = self.addHost( 'h1' )
        Munich_host = self.addHost( 'h2' )
        Prague_host = self.addHost( 'h3' )
        Vienna_host = self.addHost( 'h4' )
        Dusseldorf_host = self.addHost( 'h5' )
        Frankfurt_host = self.addHost( 'h6' )
        Zurich_host = self.addHost( 'h7' )
        Paris_host = self.addHost( 'h8' )
        Milan_host = self.addHost( 'h9' )
        Barcelona_host = self.addHost( 'h10' )
        Goonhilly_host = self.addHost( 'h11' )
        NewYork_host = self.addHost( 'h12' )
        Washington_host = self.addHost( 'h13' )
        Madrid_host = self.addHost( 'h14' )
        Helsinki_host = self.addHost( 'h15' )
        Copenhagen_host = self.addHost( 'h16' )
        London_host = self.addHost( 'h17' )
        London_host = self.addHost( 'h18' )
        Madley_host = self.addHost( 'h19' )
        Dublin_host = self.addHost( 'h20' )
        Brussels_host = self.addHost( 'h21' )
        Amsterdam_host = self.addHost( 'h22' )
        Gothenburg_host = self.addHost( 'h23' )
        Stockholm_host = self.addHost( 'h24' )

        # add edges between switch and corresponding host
        self.addLink( Budapest , Budapest_host )
        self.addLink( Munich , Munich_host )
        self.addLink( Prague , Prague_host )
        self.addLink( Vienna , Vienna_host )
        self.addLink( Dusseldorf , Dusseldorf_host )
        self.addLink( Frankfurt , Frankfurt_host )
        self.addLink( Zurich , Zurich_host )
        self.addLink( Paris , Paris_host )
        self.addLink( Milan , Milan_host )
        self.addLink( Barcelona , Barcelona_host )
        self.addLink( Goonhilly , Goonhilly_host )
        self.addLink( NewYork , NewYork_host )
        self.addLink( Washington , Washington_host )
        self.addLink( Madrid , Madrid_host )
        self.addLink( Helsinki , Helsinki_host )
        self.addLink( Copenhagen , Copenhagen_host )
        self.addLink( London , London_host )
        self.addLink( London , London_host )
        self.addLink( Madley , Madley_host )
        self.addLink( Dublin , Dublin_host )
        self.addLink( Brussels , Brussels_host )
        self.addLink( Amsterdam , Amsterdam_host )
        self.addLink( Gothenburg , Gothenburg_host )
        self.addLink( Stockholm , Stockholm_host )

        # add edges between switches
        self.addLink( Budapest , London)
        self.addLink( Budapest , Frankfurt)
        self.addLink( Munich , Dusseldorf)
        self.addLink( Munich , Frankfurt)
        self.addLink( Prague , London)
        self.addLink( Prague , Frankfurt)
        self.addLink( Vienna , Frankfurt)
        self.addLink( Vienna , Amsterdam)
        self.addLink( Dusseldorf , Frankfurt)
        self.addLink( Dusseldorf , Amsterdam)
        self.addLink( Frankfurt , Zurich)
        self.addLink( Frankfurt , Milan)
        self.addLink( Frankfurt , London)
        self.addLink( Frankfurt , Amsterdam)
        self.addLink( Zurich , London)
        self.addLink( Paris , London)
        self.addLink( Paris , Amsterdam)
        self.addLink( Milan , London)
        self.addLink( Barcelona , Madrid)
        self.addLink( Barcelona , Amsterdam)
        self.addLink( Goonhilly , London)
        self.addLink( NewYork , London)
        self.addLink( Washington , London)
        self.addLink( Madrid , London)
        self.addLink( Helsinki , Stockholm)
        self.addLink( Copenhagen , Stockholm)
        self.addLink( London , London)
        self.addLink( London , Amsterdam)
        self.addLink( London , Stockholm)
        self.addLink( London , Madley)
        self.addLink( London , Dublin)
        self.addLink( London , Brussels)
        self.addLink( London , Amsterdam)
        self.addLink( Dublin , Amsterdam)
        self.addLink( Amsterdam , Gothenburg)
        self.addLink( Amsterdam , Stockholm)
        self.addLink( Gothenburg , Stockholm)


# topos names and theirs constructors
topos = {'ring': (lambda k=3, n=1, **opts: RingTopo(k, n, **opts)), 'test': (lambda **opts: TestTopo(**opts)),
         'test2': (lambda **opts: TestTopo2(**opts)), 'agis': (lambda **opts: AgisTopo(**opts)),
         'agis2': (lambda **opts: Agis2Topo(**opts)), 'abilene': (lambda **opts: AbileneTopo(**opts)),
         'bteurope': (lambda **opts: BteuropeTopo(**opts))}

# topos names and (number of switches, number of hosts)
topos_info = {'ring': (3, 3), 'test': (9, 6),
         'test2': (9, 9), 'agis': (25, 25), 'agis2': (25, 50),
         'abilene': (11, 22), 'bteurope': (24, 24)}