__author__ = 'v1t3x'

TEST_DIR = 'generated_test'
OUTPUT_DIR = 'logs'

LOG_FORMAT = OUTPUT_DIR+"/{host}.{direction}.log"
FILENAME_SEPARATOR = '.'

INITIALIZATION_DELAY = 20
LEGACY_INITIALIZATION_DELAY = 30


def get_hostname(file_name):
    return file_name.split('.')[0]


def is_sending_log(file_name):
    return file_name.split('.')[1] == 'send'


def is_receiving_log(file_name):
    return file_name.split('.')[1] == 'recv'


def get_logname(host_name, is_send):
    return host_name+FILENAME_SEPARATOR+('send' if is_send else 'recv')+FILENAME_SEPARATOR+'log'
