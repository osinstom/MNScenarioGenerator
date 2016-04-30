#!/usr/bin/env python
"""@package util

Utilities for mininet tests.
@author Wiktor Kujawa (wkujawa@elka.pw.edu.pl)
"""
from subprocess import call, check_output, Popen
import re
import threading
import time
import os
import hashlib

DATA_DIR = 'data/'
FNULL = open(os.devnull, 'w')
F_SEP = '_'

TRAFFIC_TYPES = ['tcp', 'udp', 'random']
BITRATE_LEVELS = ['low', 'medium', 'high']

def validate_params(traffic_type, bitrate):
    if not (TRAFFIC_TYPES.__contains__(traffic_type.lower())) and BITRATE_LEVELS.__contains__(bitrate.lower()):
        print "Wrong traffic parameters!"
        print "Available TRAFFIC TYPES: "
        print TRAFFIC_TYPES
        print "Available BITRATE LEVELS: "
        print BITRATE_LEVELS
        exit(1)

def makeLegacySwitch(switch):
    """ Turn ovs switch into legacy mode (non-openflow).
        switch: name of switch to setup"""
    ret = call(["sudo", "ovs-vsctl", "set-fail-mode", switch, "standalone"])
    ret |= call(["sudo", "ovs-vsctl", "del-controller", switch])


def turnStp(switch):
    """ Turn on stp protocol.
        switch: name of switch to setup"""
    call(["sudo", "ovs-vsctl", "set", "bridge", switch, "stp_enable=true"])


def turn_legacy_on():
    """ Turn all switches into legacy mode (non-openflow)"""
    out = check_output(["ifconfig", "-a"])
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


def run_cmd(net, host_name, cmd_str):
    """ Run command in host. Execute process in host's network namespace.
        Uses 'mnexec' provided by mininet.
    """
    host = net.getNodeByName(host_name)
    cmd = 'mnexec -da {pid} {cmd}'.format(pid=host.pid, cmd=cmd_str)
#    print "Running '{}' from pid: {}".format(cmd, host.pid)
    ret = call(cmd.split(), stderr=FNULL, stdout=FNULL)
    if ret != 0:
        print "Got retcode {} from {}".format(ret, cmd)


def run_cmd_bg(net, host_name, cmd_str):
    """ Run command in host in background. Execute process in host's network namespace.
        Uses 'mnexec' provided by mininet.
    """
    host = net.getNodeByName(host_name)
    cmd = 'mnexec -da {pid} {cmd}'.format(pid=host.pid, cmd=cmd_str)
#    print "Running '{}' from pid: {}".format(cmd, host.pid)
    Popen(cmd.split(), stderr=FNULL, stdout=FNULL)


def launch_twistd_web(net, host_name):
    _launch_twistd(net, host_name, 'web')


def launch_twistd_ftp(net, host_name):
    _launch_twistd(net, host_name, 'ftp')


def _launch_twistd(net, host_name, service):
    pid_file = '/tmp/twistd.{}.{}.pid'.format(host_name, service)
    log_file = '/tmp/twistd.{}.{}.log'.format(host_name, service)
    more_args = ''
    if service == 'web':
        more_args = '--path '+DATA_DIR
    elif service == 'ftp':
        more_args = '--root '+DATA_DIR

    cmd = 'twistd  --pidfile {} --logfile {} -o {} {}'.format(pid_file, log_file, service, more_args)
    run_cmd(net, host_name, cmd)


def launch_iperf(net, host_name):
    cmd = 'iperf -s'
    run_cmd_bg(net, host_name, cmd)

OUT_DIR = "wget_tmp/"


def get_file_name(path):
    return path.split(F_SEP)[2]


def iperf(net, host_name, server_name, bitrate='50M'):
    server = net.getNodeByName(server_name)
    run_cmd(net, host_name, 'iperf -u -c {} -t 100000 -b {} &'.format(server.IP(), bitrate))


def wget(net, host_name, server_name, file_name='1MB', part_name='0'):
    server = net.getNodeByName(server_name)
    url = 'http://{}:8080/{}'.format(server.IP(), file_name)
    out_filename = host_name+F_SEP+server_name+F_SEP+file_name+F_SEP+str(part_name)+F_SEP+'.tmp'
    out = os.path.join(OUT_DIR, out_filename)
    print "Downloading "+url
    run_cmd(net, host_name, 'wget -O {} {}'.format(out, url))


def clean_dir(directory, suffix=''):
    if not os.path.exists(directory):
        print "Creating new dir: {}".format(directory)
        os.mkdir(directory, 0775)
        os.chmod(directory, 0775)
    else:
        print "Clearing {}.".format(directory)
        for f in os.listdir(directory):
            path = os.path.join(directory, f)
            if path.endswith(suffix):
                os.remove(path)


def rchmod(path, uid, guid):
    os.chown(path, uid, guid)
    for root, dirs, files in os.walk(path):
        for momo in dirs:
            os.chown(momo, uid, guid)
        for file in files:
            fname = os.path.join(root, file)
            os.chown(fname, uid, guid)


def test_init():
    print 'Killing twistd daemons.'
    call('pkill twistd'.split())
    print 'Killing iperf daemons.'
    call('pkill iperf'.split())
    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)
        os.chmod(OUT_DIR, 0666)
    else:
        print "Clearing {}.".format(OUT_DIR)
        for f in os.listdir(OUT_DIR):
            path = os.path.join(OUT_DIR, f)
            os.remove(path)


def md5sum(path):
    f = open(path, mode='rb')
    return hashlib.md5(f.read()).hexdigest()


def get_checksums():
    sums = dict()
    for f in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, f)
        s = md5sum(path)
        sums[f] = s
    return sums


def validate(checksums):
    print "Validating md5 sums of downloaded files:"
    valid = True
    for f in os.listdir(OUT_DIR):
        path = os.path.join(OUT_DIR, f)
        s = md5sum(path)
        res = 'PASSED'
        if s != checksums[get_file_name(f)]:
            res = 'FAILED'
            valid = False
        print '{}\t[{}]'.format(f, res)
    print '--------------------------------------'
    return valid


class HostThread(threading.Thread):
    def __init__(self, net, host_name):
        super(HostThread, self).__init__()
        self.net = net
        self.host_name = host_name
        self.actions = []

    def set_actions(self, actions):
        self.actions = actions

    def run(self):
        for i, action in enumerate(self.actions):
            action_type = action[0]
            target = action[1]
            args = action[2]

            if action_type == 'sleep':
                time.sleep(args)

            if action_type == 'wget':
                wget(self.net, self.host_name, target, args, part_name=i)

            if action_type == 'ftp':
                pass

            if action_type == 'iperf':
                iperf(self.net, self.host_name, target, args)