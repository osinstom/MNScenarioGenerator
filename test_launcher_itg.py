#!/usr/bin/python
from test_tool import TestToolITG, TestToolIperf

__author__ = 'v1t3x'

import os
import sys
import util
import re
import imp
from mininet.net import Mininet, CLI
from mininet.node import CPULimitedHost
from mininet.node import OVSSwitch, RemoteController
from mininet.link import TCLink
from topos import RingTopo, topos, topos_info
import threading
import time
from distutils import spawn
from itg_utils import *
import argparse
import Queue
import importlib
from mininet.topo import Topo
from subprocess import call
from topo_parser import generate
from traffic_generator_itg import generate_traffic

# TODO LIST
# - in case of repeats logs will be overridden

FNULL = open(os.devnull, 'w')

SCENARIO_PREFIX = "scenario_"
TRAFFIC_FILE_SUFFIX = ".traffic"

EPILOG = """
Topologies:
-----------
Topologies are located in topos.py. They must be also added to topo and topo_info dictionaries.

Scenarios:
----------
Each scenario should be in separate dir. Named in convention {scenario_prefix}[name]_[number_of_hosts].
Scenario dir contains files named [host_name]{itg_script_suffix} which are input for ITGSend.

Example usage:
--------------
Run scenario s1 (scenarios/scenario_s1_10) on abilene topology:
    sudo {script_name} -t abilene -d scenarios
List topologies:
    sudo {script_name} -lt
List scenarios in current dir:
    sudo {script_name} -ls
List scenarios in current scenarios_dir:
    sudo {script_name} -ls -d scenarios_dir

""".format(scenario_prefix=SCENARIO_PREFIX, itg_script_suffix=TRAFFIC_FILE_SUFFIX,
           script_name=sys.argv[0])

def import_from(module, name):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)

def get_scenarios(path):
    scenarios = []
    for f in os.listdir(path):
        scenario_path = os.path.join(path, f)
        if os.path.isdir(scenario_path) and f.startswith(SCENARIO_PREFIX):
            if scenario_sanity_check(scenario_path):
                scenarios.append(f)
    return scenarios


def scenario_sanity_check(path):
    """
    Check if scenario does not consist more hosts than suggested in scenario name
    :param path:
    :return: scenario is valid or not
    """
    return True    # TODO implement logic

def isGenerated(topology, hosts, distribution):
    topology = "gen_" + topology + "_" + distribution + "_" + str(hosts)
    for t in get_generated_topologies():
        if t == topology:
            return True
    return False

def get_generated_topologies():
    topologies = []
    for f in os.listdir("topologies"):
        topology_path = os.path.join("topologies", f)
        if not os.path.isdir(topology_path) and f.startswith("gen_"):
            topologies.append(f.replace(".py", ""))
    return topologies

def get_zoo_topologies():
    topos = []
    for f in os.listdir("topologies/zoo-dataset"):
        topo_path = os.path.join("topologies/zoo-dataset", f)
        ext = os.path.splitext(f)[-1].lower()
        if ext == ".graphml":
             topos.append(f.replace(".graphml", "").lower())
    return topos

def generate_topology(topo, hosts, distribution, bandwidth):
    arg = []
    arg.append("-f")
    arg.append("topologies/zoo-dataset/" + topo.title() + ".graphml") # Path to graphML file
    arg.append("-o")
    arg.append("topologies/gen_" + topo + "_" + distribution + "_" + str(hosts) + ".py") # Output file name
    arg.append("-H")
    arg.append(hosts)
    if distribution == 'random':
        arg.append("-r")
    arg.append("--bw")
    arg.append(bandwidth)
    print "BW=" + str(bandwidth)
    generate(arg)
    print "Topology {} generated.".format(topo)
    return 0

def create_scenario_name(traffic_type, c_min, c_max, clients, flows, topology, distribution, hosts):
    return "scenario_" + traffic_type + "-rate[" + c_min + ":" + c_max + "]-" + str(clients) + "-" + str(flows) + "_" + topology + "-" + distribution + "-" + str(hosts)
    
def main():
    original_dir = os.getcwd()
    
    parser = argparse.ArgumentParser(description="Launches D-ITG test scenario in mininet.", epilog=EPILOG,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-l", "--store_logs", action="store_true", default=False,
                        help="store logs (default: logs are discarded)")
    parser.add_argument("-t", "--topology", help="name of topology to run")
    parser.add_argument("-B", "--bandwidth", default=1, help="Bandwidth of links in Mbit/s (default: 1 Mbit/s)")
    parser.add_argument("-lt", "--list-topologies", action="store_true", help="list available topologies")
    parser.add_argument("-ls", "--list-scenarios", action="store_true", help="list available scenarios")
#     parser.add_argument("-s", "--scenario", help="select test scenario - dir name or just scenario name")
    parser.add_argument("-d", "--scenarios-dir", help="directory with scenarios (default: current directory)")
    parser.add_argument("-H", "--hosts", default=1, help="Number of hosts in network ('per switch' for uniform distribution)")
    parser.add_argument("-dr", "--random-distribution", action="store_true", default=False, 
                        help="Random hosts distribution in network (default: uniform)")
    parser.add_argument("-stp", "--stp-switch", action="store_true",
                        help="Run with STP switches. Disconnects from controller.")
    parser.add_argument("-o", "--logs-dir",
                        help="directory for storing logs (default: logs/ in scenario directory). Implies storing logs")
    parser.add_argument("-r", "--repeat", type=int, default=1,
                        help="number of test case repeats (-1 for infinite). Warning: Logs will be overridden")
    parser.add_argument("--tool", default='iperf',
                        help="Traffic generation tool: iperf, ditg")
    parser.add_argument("-T", "--traffic-type", help="Type of generated traffic")
    parser.add_argument("--c_min", help="Minimum bitrate of generated traffic")
    parser.add_argument("--c_max", help="Maximum bitrate of generated traffic")
    parser.add_argument("-g", "--clients", help="Number of clients generating traffic")
    parser.add_argument("-f", "--flows", help="Number of flows per client")
    
    args = parser.parse_args()

    if not (args.list_scenarios or args.list_topologies) and not (args.topology):
        print "Wrong parameters: Need to set topology. Or just list topologies or scenarios."
        print ""
        parser.print_help()
        exit(1)
    
    if args.tool and args.tool == 'iperf':
        if not (args.traffic_type and args.c_min and args.c_max and args.clients and args.flows):
            print "Not enough traffic parameters!"
            print ""
            parser.print_help()
            exit(1)
        else:
            util.validate_params(args.traffic_type)
    elif args.tool and args.tool == 'ditg':
        print "ditg full support not implemented yet"
        exit(1)

    if args.list_topologies:
        print "Topologies ([name] s=[no. switches]) h=[no. hosts]:"
        for t in topos_info:
            print "{} s={} h={}".format(t, topos_info[t][0], topos_info[t][1])
        return 0

    scenarios_dir = original_dir
    if args.scenarios_dir:
        scenarios_dir = args.scenarios_dir

    if args.list_scenarios:
        print "Scenarios ([name] ):"
        for s in get_scenarios(scenarios_dir):
            print s
        return 0
    
    
    
    distribution = ''
    if(args.random_distribution):
        distribution = "random"
    else:
        distribution = "uniform"
    
    traffic_generation = False
    scenario = create_scenario_name(args.traffic_type, args.c_min, args.c_max, args.clients, args.flows, args.topology, distribution, args.hosts)
    print scenario
    all_scenarios = get_scenarios(scenarios_dir)
    scenario_dir = None
    if scenario in all_scenarios:
        scenario_dir = os.path.join(scenarios_dir, scenario)
    else:
        os.mkdir(scenarios_dir + '/' + scenario)
        scenario_dir = os.path.join(scenarios_dir, scenario)
        traffic_generation = True

    # Get topology
    topology = args.topology
    if isGenerated(topology, args.hosts, distribution):
        print "Topology {}-{}-{} exists".format(topology, distribution, args.hosts)
    else:
        if topology in get_zoo_topologies():
            generate_topology(topology, args.hosts, distribution, args.bandwidth)    
        else:
            print "Wrong topology name: "+topology
            print "Available generated: "   
            print get_generated_topologies()
            print "Available to generate: "
            print get_zoo_topologies()
            exit(1)
    
    topology = "gen_" + topology + "_" + distribution + "_" + str(args.hosts)
    
    # Check if scenario can be run on topology
    #topology_hosts = topos_info[topology][1]
    #scenario_hosts = int(scenario_dir.split('_')[-1])
    #if scenario_hosts > topology_hosts:
    #    print "Cannot run scenario {} ({} hosts) on topology {} ({} hosts). Too many hosts in scenario.".format(scenario, scenario_hosts, topology, topology_hosts)
    #    exit(4)
#     print scenario_dir
#     if not os.path.exists(scenario_dir):
#         print "Not found generated test dir: {}. Please run ./test_generator_itg.py first.".format(scenario_dir)
#         exit(4)

    os.chdir(scenario_dir)

    log_dir = None
    # Log dir implies storing logs
    if args.logs_dir:
        args.store_logs = True

    if args.store_logs:
        if args.logs_dir:
            if os.path.isabs(args.logs_dir):
                log_dir = args.logs_dir
            else:
                # Logs path relative to CWD
                log_dir = os.path.join(original_dir, args.logs_dir)
        else:
            log_dir = OUTPUT_DIR

        # Create or clean directory for logs
        util.clean_dir(log_dir, suffix=".log")
        print "Storing logs in: {}".format(os.path.join(os.getcwd(), log_dir))
    else:
        print "Not storing logs."
        
    print "Topology: {} Scenario: {}".format(topology, scenario)
    
    os.chdir(original_dir)
    
    #topo = importlib.import_module("gen_{}".format(topology))

    #Change comments to load a fixed topology   
    #f, filename, desc = imp.find_module('gen_bteurope', [os.path.abspath(os.getcwd()) + '/topologies'])
    #topo = imp.load_module('gen_bteurope', f, filename, desc)
    
    
    f, filename, desc = imp.find_module("{}".format(topology) , [os.path.abspath(os.getcwd()) + '/topologies'])
    topo = imp.load_module("{}".format(topology) , f, filename, desc)
    
    print "Launching Mininet.."
    net = Mininet(topo=topo.GeneratedTopo(), controller=RemoteController, switch=OVSSwitch, host=CPULimitedHost,
                  link=TCLink, autoSetMacs=True)

    # Start network
    print "Starting network.."
    net.start()
    
    #if(traffic_generation):
    generate_traffic(net.hosts, scenario_dir, args.clients, args.flows, args.traffic_type, args.c_min, args.c_max)
    
    if args.stp_switch:
        util.turn_legacy_on()
        print "Waiting {} s ...".format(LEGACY_INITIALIZATION_DELAY)
        time.sleep(LEGACY_INITIALIZATION_DELAY)

    print "Waiting {} s for initialization of mininet and controller...".format(INITIALIZATION_DELAY)
    time.sleep(INITIALIZATION_DELAY)

    # Preparing TestTool #TODO choosing various tools based on config
    if args.tool == 'iperf':
        print "Using iperf"
        test_tool = TestToolIperf(net, log_dir)
    elif args.tool == 'ditg':
        print "Using ditg"
        test_tool = TestToolITG(net, log_dir)
    else:
        print "ERROR Unknown tool: {}".format(args.tool)
        net.stop()
        sys.exit(3)
       
    os.chdir(scenario_dir)
     
    # Run servers
    hosts = net.hosts
    print "Starting servers..."
    for host in hosts:
        host_name = host.name
        test_tool.run_server(host_name)

    iterations = args.repeat
    
    if iterations != 1:
        start_time = time.time()
    i = 0
    while i != iterations:
        if iterations != 1:
            print "Iteration: {} / {}".format(i+1, iterations)
        iteration_start_time = time.time()
        # Run ITGSends per host config
        threads = []
        for f in os.listdir(os.path.curdir):
            if os.path.isfile(f) and f.endswith(TRAFFIC_FILE_SUFFIX):
                host_name = get_hostname(f)
                test_tool.run_client(host_name, f)

        # CLI(net)    # DEBUG
        print "Waiting for test end.."
        retcode = test_tool.wait_for_end()

        end_time = time.time()
        print "Testing time: {:0.2f} s".format(end_time-iteration_start_time)
        i += 1
    if iterations != 1:
        print "Total testing time: {:0.2f} s".format(end_time-start_time)
    print "Stopping network.."
    net.stop()
    s = os.stat('.')
    if args.store_logs:
        util.rchmod(log_dir, s.st_uid, s.st_gid)
    os.chdir(original_dir)
    print "Killing all test tool processes."
    test_tool.kill_all()

    if retcode == 2:
        print "END Test finished with WARNINGS"
        sys.exit(2)
    elif retcode == 1:
        print "ERROR CRITICAL server went down during test"
        sys.exit(1)
    else:
        print "END Test finished successfully"
        sys.exit(0)


def is_ditg_installed():
    return bool(spawn.find_executable('ITGSend'))


if __name__ == '__main__':
    if not is_ditg_installed():
        print "Please install D-IGT (http://traffic.comics.unina.it/software/ITG/download.php)"
        exit(1)

    main()
