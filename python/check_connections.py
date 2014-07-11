#!/usr/bin/python

import socket
import logging
import subprocess
from multiprocessing import Pool

number_of_workers = 1
control_type = "socket"
timeout = 2

DEBUG = False
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

if "check_output" not in dir(subprocess):
    def f(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError(
                'stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE,
                                   *popenargs,
                                   **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd)
        return output
    subprocess.check_output = f


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def colorize(status, string):
    return "%s%s%s" % (status, string, bcolors.ENDC)


class Connection(object):
    NETCAT_CMD = "nc %(timeout)s -%(type)svz %(ip)s %(port)s > /dev/null 2>&1"

    def __init__(self, connection_type, ip, port, description):
        self.type = connection_type
        self.ip = ip
        self.description = description
        self.port = port

    def check(self):
        logging.info("Trying to connect: %r" % self)
        try:
            if control_type in ["netcat"]:
                if self.type in ["udp"]:
                    if self.port in ["53"]:
                        logging.debug("dig dns port: %s" % self.ip)
                        cmd = "dig www.kartaca.com @%s +time=%d" % (
                            self.ip, timeout)
                    elif self.port in ["123"]:
                        logging.debug("check ntp host: %s" % self.ip)
                        cmd = "/usr/lib/nagios/plugins/check_ntp -H %s" % self.ip
                else:
                    timeout_param = "" # no timeout in UDP
                    if self.type in ["tcp"]:
                        timeout_param = "-w %d" % timeout
                    cmd = Connection.NETCAT_CMD % {
                        "type": self.type[0], "ip": self.ip, "port": self.port, "timeout": timeout_param}
                logging.debug("Running command: %s" % cmd)
                out = subprocess.check_output(cmd, shell=True)
                logging.info("cmd out: %r" % out)
                return True
            else:
                if self.type in ["udp"]:
                    sock_proto = socket.SOCK_DGRAM
                else:
                    sock_proto = socket.SOCK_STREAM
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex(
                    (socket.gethostbyname(self.ip), int(self.port)))
                sock.close()
                if result != 0:
                    return False
            return True
        except subprocess.CalledProcessError, e:
            logging.warn("Connection to %s on port %s failed: %s" %
                         (self.ip, self.port, e))
            if control_type != "netcat":
                sock.close()
        return False

    def __repr__(self):
        return ",".join([self.ip, self.type, self.port, self.description])


def check_prettier(conn):
    if conn.check():
        status = colorize(bcolors.OKGREEN, "OK")
    else:
        status = colorize(bcolors.FAIL, "NOK")

    print "%s,%s" % (conn, status)


def main():
    list_of_conns = [
        Connection("tcp", "2.2.2.2", "5667", "desc"),
    ]

    workers = min(number_of_workers, len(list_of_conns))
    if workers > 1:
        p = Pool(workers)
        results = p.map(check_prettier, list_of_conns)
    else:
        map(check_prettier, list_of_conns)


if __name__ == "__main__":
    main()
