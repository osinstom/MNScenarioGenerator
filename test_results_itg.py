#!/usr/bin/python
__author__ = 'v1t3x'

from itg_utils import *
import os
import sys
import subprocess

DEFAULT_LOGS_PATH = os.path.join(TEST_DIR, OUTPUT_DIR)
LOG_SUMMARY_SUFFIX = ".summary.txt"
LOG_SUFFIX = ".log"

SECTION_SEPARATOR = '----------------------------------------------------------\n'
TOTAL_SECTION_SEPARATOR = '__________________________________________________________\n'
TOTAL_SECTION_HEADER = '****************  TOTAL RESULTS   ******************\n'
EMPTY_LOG_FILE = 'Empty log file\n'

KEY_NUMBER_OF_FLOWS = 'Number of flows'
KEY_TOTAL_TIME = 'Total time'
KEY_TOTAL_PACKETS = 'Total packets'
KEY_MINIMUM_DELAY = 'Minimum delay'
KEY_MAXIMUM_DELAY = 'Maximum delay'
KEY_AVERAGE_DELAY = 'Average delay'
KEY_AVERAGE_JITTER = 'Average jitter'
KEY_DELAY_STANDARD_DEVIATION = 'Delay standard deviation'
KEY_BYTES_RECEIVED = 'Bytes received'
KEY_AVERAGE_BITRATE = 'Average bitrate'
KEY_AVERAGE_PACKET_RATE = 'Average packet rate'
KEY_PACKETS_DROPPED = 'Packets dropped'
KEY_AVERAGE_LOSS_BURST_SIZE = 'Average loss-burst size'
KEY_ERROR_LINES = 'Error lines'

HEADERS_TO_PRINT = [KEY_NUMBER_OF_FLOWS, KEY_TOTAL_TIME+' (s)', KEY_TOTAL_PACKETS, KEY_MINIMUM_DELAY+' (s)', KEY_MAXIMUM_DELAY+' (s)',
                 KEY_AVERAGE_DELAY+' (s)', KEY_AVERAGE_JITTER+' (s)', KEY_DELAY_STANDARD_DEVIATION+' (s)', KEY_BYTES_RECEIVED,
                 KEY_AVERAGE_BITRATE+' (Kbit/s)', KEY_AVERAGE_PACKET_RATE+' (pkt/s)', KEY_PACKETS_DROPPED, KEY_AVERAGE_LOSS_BURST_SIZE+' (pkt)',
                 KEY_ERROR_LINES]
KEYS_TO_PRINT = [KEY_NUMBER_OF_FLOWS, KEY_TOTAL_TIME, KEY_TOTAL_PACKETS, KEY_MINIMUM_DELAY, KEY_MAXIMUM_DELAY,
                 KEY_AVERAGE_DELAY, KEY_AVERAGE_JITTER, KEY_DELAY_STANDARD_DEVIATION, KEY_BYTES_RECEIVED,
                 KEY_AVERAGE_BITRATE, KEY_AVERAGE_PACKET_RATE, KEY_PACKETS_DROPPED, KEY_AVERAGE_LOSS_BURST_SIZE,
                 KEY_ERROR_LINES]
VALUES_SEPARATOR = ';'


def parse_key_value(f, key, stats):
    line = f.readline()
    kv = map(str.strip, line.split('='))
    assert kv[0] == key
    stats[key] = kv[1].split()[0]


def parse_section(f):
    flow_number = f.readline().split(':')[1].strip()
    source = f.readline().split()[1]
    destination = f.readline().split()[1]
    assert f.readline() == SECTION_SEPARATOR

    while True:
        line = f.readline()
        if line != SECTION_SEPARATOR:
            # Ignoring flow stats
            pass
        else:
            return


def parse_total(f):
    assert f.readline() == TOTAL_SECTION_HEADER
    assert f.readline() == TOTAL_SECTION_SEPARATOR

    stats = parse_values(f)
    return stats


def parse_values(f):
    stats = dict()
    parse_key_value(f, KEY_NUMBER_OF_FLOWS, stats)
    parse_key_value(f, KEY_TOTAL_TIME, stats)
    parse_key_value(f, KEY_TOTAL_PACKETS, stats)
    parse_key_value(f, KEY_MINIMUM_DELAY, stats)
    parse_key_value(f, KEY_MAXIMUM_DELAY, stats)
    parse_key_value(f, KEY_AVERAGE_DELAY, stats)
    parse_key_value(f, KEY_AVERAGE_JITTER, stats)
    parse_key_value(f, KEY_DELAY_STANDARD_DEVIATION, stats)
    parse_key_value(f, KEY_BYTES_RECEIVED, stats)
    parse_key_value(f, KEY_AVERAGE_BITRATE, stats)
    parse_key_value(f, KEY_AVERAGE_PACKET_RATE, stats)
    parse_key_value(f, KEY_PACKETS_DROPPED, stats)
    parse_key_value(f, KEY_AVERAGE_LOSS_BURST_SIZE, stats)
    parse_key_value(f, KEY_ERROR_LINES, stats)
    return stats


def parse_summary(file_name):
    with open(file_name, 'r') as f:
        # HEADER - two lines with version and compile options
        for i in xrange(2):
            # Ignore header
            line = f.readline()

        # Sections parsing
        while True:
            line = f.readline()
            if line == EMPTY_LOG_FILE:
                return None
            elif line == SECTION_SEPARATOR:
                parse_section(f)
            elif line == '\n':
                assert f.readline() == TOTAL_SECTION_SEPARATOR
                break
            else:
                print "Parsing error, don't know how to handle:"+repr(line)

        return parse_total(f)


def decode_itg(logs_dir):
    files = os.listdir(logs_dir)
    for f in files:
        if f.endswith(LOG_SUFFIX):
            out_name = f+LOG_SUMMARY_SUFFIX
            if out_name in files:
                continue
            in_file = os.path.join(logs_dir, f)
            out_file = os.path.join(logs_dir, out_name)
            with open(out_file, 'w+') as fout:
                cmd = "ITGDec {infile}".format(infile=in_file)
                subprocess.call(cmd.split(), stdout=fout)


def main():
    if len(sys.argv) == 2:
        logs_dir = sys.argv[1]
    else:
        logs_dir = DEFAULT_LOGS_PATH

    # Decoding if needed
    files = os.listdir(logs_dir)
    decoded = [f for f in files if f.endswith(LOG_SUMMARY_SUFFIX)]
    if len(decoded)*2 < len(files):
        print "Decoding results (generating summary files).."
        decode_itg(logs_dir)

    print "Processing results.."
    print "--- Results CUT HERE ---"
    # Header
    print "Receiving host"+VALUES_SEPARATOR+VALUES_SEPARATOR.join(HEADERS_TO_PRINT)

    files = os.listdir(logs_dir)
    for f in files:
        if f.endswith(LOG_SUMMARY_SUFFIX) and is_receiving_log(f):
            host = get_hostname(f)
            stats = parse_summary(os.path.join(logs_dir, f))
            if stats:
                print host+VALUES_SEPARATOR+VALUES_SEPARATOR.join(map(lambda x: dict.get(stats, x), KEYS_TO_PRINT))
    print "--- Results CUT HERE ---"

if __name__ == "__main__":
    main()