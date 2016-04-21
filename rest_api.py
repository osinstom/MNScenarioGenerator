#!/usr/bin/python
from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.link import TCLink
from topos import RingTopo
import json
import requests
# import sys

PORT = 8888
BASE_URL = 'http://localhost:8080/tee'

URL_FORMAT_KEY = 'url_format'
URL_EXAMPLE_KEY = 'url_example'
DESCRIPTION_KEY = 'description'
TYPE_KEY = 'type'

APIS = {
    'hosts': {DESCRIPTION_KEY: 'List of detected hosts.',
              TYPE_KEY: 'GET',
              URL_EXAMPLE_KEY: '{base_url}/hosts'.format(base_url=BASE_URL)
              },
    'links': {DESCRIPTION_KEY: 'List of links (edges).',
              TYPE_KEY: 'GET',
              URL_EXAMPLE_KEY: '{base_url}/links'.format(base_url=BASE_URL)
              },
    'devices': {DESCRIPTION_KEY: 'List of devices (nodes) - hosts and switches.',
                TYPE_KEY: 'GET',
                URL_EXAMPLE_KEY: '{base_url}/devices'.format(base_url=BASE_URL)
                },
    'flows': {DESCRIPTION_KEY: 'List of all logical flows.',
                TYPE_KEY: 'GET',
                URL_EXAMPLE_KEY: '{base_url}/flows'.format(base_url=BASE_URL)
                },
    'routes': {DESCRIPTION_KEY: 'List of k-shortest path for pair of hosts.',
               TYPE_KEY: 'GET',
               URL_FORMAT_KEY: '{base_url}/routes/{{srcIP}}/{{dstIP}}'.format(base_url=BASE_URL),
               URL_EXAMPLE_KEY: '{base_url}/routes/{srcIP}/{dstIP}'.format(base_url=BASE_URL, srcIP='10.0.0.1',
                                                                           dstIP='10.0.0.2')
               },
    'move': {DESCRIPTION_KEY: 'Move flow from one route to another by giving theirs IDs.',
             TYPE_KEY: 'GET',
             URL_FORMAT_KEY: '{base_url}/move/{{fromRoute}}/{{flow}}/{{toRoute}}'.format(base_url=BASE_URL),
             URL_EXAMPLE_KEY: 'GENERATE IN RUNTIME'
             }
}


def main():
    # Initialize mininet
    net = Mininet(topo=RingTopo(k=3, n=1, lopts={"bw": 50}), controller=RemoteController, switch=OVSSwitch,
                  link=TCLink, autoSetMacs=True)
    net.start()
    h1 = net.getNodeByName("h1")
    # sys.stdin.read(1)
    h1.cmd('ping -c 10 10.0.0.2')

    # Generate example of 'move' API request
    text = requests.get(APIS['routes'][URL_EXAMPLE_KEY]).text
    js = json.loads(text)
    r1 = js[0]
    r2 = js[1]
    if not js[0]['flows']:
        r1, r2 = r2, r1

    r1_id = r1['id']
    r2_id = r2['id']
    f1_id = r1['flows'][0]['id']
    APIS['move'][URL_EXAMPLE_KEY] = APIS['move'][URL_FORMAT_KEY].format(fromRoute=r1_id, flow=f1_id, toRoute=r2_id)

    # Print out documentation
    print """Interfaces of TEE northbound API (REST) with example input and output.
Base location {}/{{API_NAME}}/{{PARAMETERS}}, where localhost is address of running OpenDaylight controller.\n""".format(BASE_URL)

    print """Example topology:

                     S3
H1 - 10.0.0.1       /  \\
H2 - 10.0.0.2      /    \\
                  /      \\
        H1 ---- S1 ------ S2 --- H2

    """

    for i, api in enumerate(APIS.values(), start=1):
        print "{}. {}".format(i, api['description'])
        if URL_FORMAT_KEY in api:
            print "URL format: {}".format(api[URL_FORMAT_KEY])
        print "Example:"
        print "URL: {url} \nRequest type: {type}".format(url=api['url_example'], type=api['type'])
        if api['type'] == 'GET':
            r = requests.get(api['url_example'])
            print "Return code: {}".format(r.status_code)
            print "Result:"
            parsed = json.loads(r.text)
            print json.dumps(parsed, indent=4, sort_keys=True)

        elif api['type'] == 'PUT':
            r = requests.put(api['url_example'])
            print "Return code: {}".format(r.status_code)
        else:
            print "Request type not supported : {}".format(api['type'])
            exit(1)
        print ""

    net.stop()


if __name__ == "__main__":
    main()
