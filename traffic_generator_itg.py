#!/usr/bin/python
__author__ = 'v1t3x'

import random
import os
import shutil

# Parameters that need to be filled to generate test

DURATION = (1 * 10*3, 120 * 10**3)      # in ms (1s, 2min)
DELAY = (0, 2 * 60 * 10**3)             # in ms (0, 2 min)
FLOW_TYPES = ['UDP', 'TCP']
TCP = ['TCP']
UDP = ['UDP']
# default packet size 512 bytes
CONSTANT_RATE = (10**3, 20 * 10**3)     # (4mbits - 80 mbits)
# TODO ports src dst params


def gen_params(dst_ip, flow_type):
    delay = random.randint(DELAY[0], DELAY[1])
    duration = random.randint(DURATION[0], DURATION[1])
    const_rate = random.randint(CONSTANT_RATE[0], CONSTANT_RATE[1])
    return "-a {} -d {} -t {} -C {} -T {}".format(dst_ip, delay, duration, const_rate, flow_type)

def get_hostname(host_num):
    return "{}".format(host_num)

def isTheSameSwitch(host1, host2):
    s1 = host1.__getattribute__('name').rsplit('_', 1)[1]
    s2 = host2.__getattribute__('name').rsplit('_', 1)[1]
    if(s1 == s2):
        return True
    else:
        return False
    
def generate_traffic(hosts, OUTPUT_DIR, CLIENTS, MAX_FLOW_PER_HOST, traffic_type, bitrate):
    random.seed()
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
        
    os.chmod(OUTPUT_DIR, 0775)
    
    FILE_FORMAT = OUTPUT_DIR+"/{host}.traffic" # traffic description file
    hosts_set = set(range(1, hosts.__len__()))
    
    for host_number in random.sample(hosts_set, int(CLIENTS)):
        file_name = FILE_FORMAT.format(host=get_hostname(hosts[host_number].__getattribute__('name')))
        f = open(file_name, mode='w')
        print "Generating host {} traffic".format(hosts[host_number].__getattribute__('name'))
        for flow_number in xrange(random.randint(1, int(MAX_FLOW_PER_HOST))):
            flow_type = ''
            if traffic_type == 'random':
                flow_type = random.choice(FLOW_TYPES)
                print "random traffic: " + flow_type
            
            server_number = 0
            
            while (True):
                server_number = random.choice(list(hosts_set - {host_number}))
                if not (isTheSameSwitch(hosts[host_number], hosts[server_number])):
                    break;
                
            dst_ip = hosts[server_number].IP()
            print "Generating flow {}: {} to {}".format(flow_number, flow_type.upper(), dst_ip)
            parameters = gen_params(dst_ip, flow_type)
            print "Params: {}".format(parameters)
            f.write(parameters+'\n')
        f.close()

if __name__ == '__main__':
    main()
