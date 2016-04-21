import os
from itg_utils import get_logname
import abc
import Queue
from subprocess import call
import threading
import time


class TestTool:
    def __init__(self, net, log_dir):
        self.net = net
        self.log_dir = log_dir
        self.q = Queue.Queue()
        self.server_threads = list()
        self.client_threads = list()

    @abc.abstractmethod
    def run_server(self, host_name):
        pass

    @abc.abstractmethod
    def run_client(self, host_name, config_file):
        pass

    @abc.abstractmethod
    def is_server(self, cmd):
        pass

    @abc.abstractmethod
    def kill_all(self,):
        pass

    def run_cmd(self, host_name, cmd, type, delay=0):
        t = threading.Thread(target=self.run_cmd_thread, args=(host_name, cmd, type, delay))
        if type == "server":
            self.server_threads.append(t)
        elif type == "client":
            self.client_threads.append(t)
        else:
            print "Wrong client name"
        t.start()

    def run_cmd_thread(self, host_name, cmd_str, proc_type, delay):
        """ Run command in host. Execute process in host's network namespace.\n
        Uses 'mnexec' provided by mininet.\n
        :param host_name:
        :param cmd_str:
        :param proc_type:
        :param log_dir: """
        host = self.net.getNodeByName(host_name)
        if delay:
            time.sleep(float(delay))
        cmd = 'mnexec -da {pid} {cmd}'.format(pid=host.pid, cmd=cmd_str)
        if self.log_dir is None:
            log_dir = './'
        else:
            log_dir = self.log_dir
        ret = call(cmd.split(), stderr=open(os.path.join(log_dir, host_name+'.'+proc_type+'.stderr'), mode='w+'), stdout=open(os.path.join(log_dir, host_name+'.'+proc_type+'.stdout'), mode='w+'))
        self.q.put((cmd, ret, host_name))

    def wait_for_end(self):
        while [True for t in self.client_threads if t.is_alive()]:
            ret = self.q.get()
            print "Return from {} on {}: {}".format(ret[0], ret[2], ret[1])
            cmd = ret[0]

            if self.is_server(cmd):
                print "ERROR CRITICAL {} server is down".format(ret[2])
                self.kill_all()
                return 1
            elif ret[1] != 0:
                print "WARNING client on {} exited with {}".format(ret[2], ret[1])
        return 0

    def get_queue(self):
        return self.q


class TestToolITG(TestTool):
    def run_server(self, host_name):
        if self.log_dir:
            cmd = 'ITGRecv -l '+os.path.join(self.log_dir, get_logname(host_name, False))
        else:
            cmd = 'ITGRecv'
        print "{} {}".format(host_name, cmd)
        self.run_cmd(host_name, cmd, 'server')

    def run_client(self, host_name, config_file):
        cmd = 'ITGSend {script}'.format(script=config_file)
        if self.log_dir:
            cmd += ' -l {logfile}'.format(logfile=os.path.join(self.log_dir, get_logname(host_name, True)))
        print "{} {}".format(host_name, cmd)
        self.run_cmd(host_name, cmd, 'client')

    def is_server(self, cmd):
        if "ITGRecv" in cmd:
            return True
        elif "ITGSend" in cmd:
            return False
        else:
            raise ValueError("It is not valid ITG command: "+cmd)

    def kill_all(self):
        os.system('pkill ITGRecv')
        os.system('pkill ITGSend')


class TestToolIperf(TestTool):
    def run_server(self, host_name):
        self.run_cmd(host_name, "iperf -s", 'server')
        self.run_cmd(host_name, "iperf -u -s", 'server')

    def run_client(self, host_name, config_file):
        parser = ITGParser(config_file)
        params_list = parser.parse()
        for params in params_list:
            print "DEBUG: {} : {}".format(host_name, params)
            cmd = 'iperf -c {} -t {}'.format(params['target'], int(params['duration']) / 1000)
            type = params['type']
            if type and type.lower() == "udp":
                cmd += ' -u'

                u_size = params['u_size']
                c_rate = params['c_rate']
                if u_size:
                    packet_size = sum(map(int, u_size.split()))/2
                else:
                    packet_size = 512
                if c_rate:
                    rate = int(c_rate)
                rate *= packet_size  # in bits/s
                cmd += ' -b {}'.format(rate)

            delay = params['delay']
            if delay:
                delay = float(delay) / 1000

            self.run_cmd(host_name, cmd, 'client', delay)

    def is_server(self, cmd):
        if 'iperf' not in cmd:
            raise ValueError("It is not valid iperf command: "+cmd)
        if '-s' in cmd:
            return True
        else:
            return False

    def kill_all(self):
        os.system('pkill -9 iperf')


class ITGParser:
    def __init__(self, path):
        self.args_list = []
        self.file = open(path, 'r')

    def parse_value(self, line, name, key, params):
        line += '-'
        value = line.partition(name)[2].partition('-')[0].strip()
        if not value:
            value = None
        params[key] = value

    def parse_line(self, line):
        params = dict()
        self.parse_value(line, '-a', 'target', params)
        self.parse_value(line, '-d', 'delay', params)
        self.parse_value(line, '-t', 'duration', params)
        self.parse_value(line, '-C', 'c_rate', params)
        self.parse_value(line, '-u', 'u_size', params)
        self.parse_value(line, '-T', 'type', params)
        return params

    def parse(self):
        for l in self.file.readlines():
            self.args_list.append(self.parse_line(l))
        return self.args_list
