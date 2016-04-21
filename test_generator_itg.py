#!/usr/bin/python
__author__ = 'v1t3x'

import random
import os
import shutil

OUTPUT_DIR = 'generated_test'

# Parameters that need to be filled to generate test
CLIENTS = 6
MIN_HOST = 1
MAX_HOST = 9
MAX_FLOW_PER_HOST = 5
DURATION = (1 * 10*3, 120 * 10**3)      # in ms (1s, 2min)
DELAY = (0, 2 * 60 * 10**3)             # in ms (0, 2 min)
FLOW_TYPES = ['UDP', 'TCP']
# default packet size 512 bytes
CONSTANT_RATE = (10**3, 20 * 10**3)     # (4mbits - 80 mbits)
# TODO ports src dst params

FILE_FORMAT = OUTPUT_DIR+"/{host}.ditgs"


def gen_params(dst_ip, flow_type):
    delay = random.randint(DELAY[0], DELAY[1])
    duration = random.randint(DURATION[0], DURATION[1])
    const_rate = random.randint(CONSTANT_RATE[0], CONSTANT_RATE[1])
    return "-a {} -d {} -t {} -C {} -T {}".format(dst_ip, delay, duration, const_rate, flow_type)


def get_ip(host_num):
    return "10.0.0.{}".format(host_num)


def get_hostname(host_num):
    return "h{}".format(host_num)


def main():
    random.seed()
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.mkdir(OUTPUT_DIR)
    os.chmod(OUTPUT_DIR, 0775)

    hosts = set(range(MIN_HOST, MAX_HOST+1))
    print hosts
    for host_number in random.sample(hosts, CLIENTS):
        file_name = FILE_FORMAT.format(host=get_hostname(host_number))
        f = open(file_name, mode='w')
        print "Generating host {} traffic".format(host_number)
        for flow_number in xrange(random.randint(1, MAX_FLOW_PER_HOST)):
            flow_type = random.choice(FLOW_TYPES)
            server_number = random.choice(list(hosts - {host_number}))
            dst_ip = get_ip(server_number)
            print "Generating flow {}: {} to {}".format(flow_number, flow_type, dst_ip)
            parameters = gen_params(dst_ip, flow_type)
            print "Params: {}".format(parameters)
            f.write(parameters+'\n')
        f.close()

if __name__ == '__main__':
    main()
