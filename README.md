Content
=======
Scripts related to mininet.

Files:
------
* topos.py - custom topologies  
* util.py - helper functions, like configuring Open vSwtich  
* makeNonOpenflow.py - script disconnect switches named "s%d" from controller, make to work as regular switch with STP protocol  

Topologies:
-----------
* loop - 3 switches connected one to each other and one host per switch
* test - custom topology described in comment of TestTopo class.

How to run:
-----------
// Ring topology  
sudo mn --custom topos.py  --topo ring  [other options]

// Test topology  
sudo mn --custom topos.py  --topo test [other options]

Usefull [other options]:
* --link tc,bw=100
* --switch ovsk,protocols=OpenFlow13
* --controller remote,ip=192.168.1.1


TODO
----
* Implement test scenarios
* Passing parameter to RingTopo (topos dict)

