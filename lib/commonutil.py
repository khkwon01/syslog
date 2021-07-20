# -*- coding: utf-8 -*-
import argparse
import datetime
import os
import signal
import sys
import threading
import time
import traceback
import yaml

# import pprint
# import uuid
# import json


def convert_to_epoch(v_timestamp):
    o_timestamp = v_timestamp.replace(tzinfo=None)
    o_diff = (v_timestamp - datetime(1970, 1, 1))
    o_seconds = o_diff.total_seconds()

    return o_seconds

class CustomThread(threading.Thread):
    def __init__(self, v_sleeptime):
        threading.Thread.__init__(self)
        self.__Stop = threading.Event()
        self.__Sleep = v_sleeptime

    def stop(self):
        self.__Stop.set()

    def run(self):

        while not self.__Stop.is_set():

            try:
                i_stime = time.time()
                print('test...')
                i_est_time = round(time.time() - i_stime, 2)
                print('time gap: ', i_est_time)
                time.sleep(self.__Sleep)
            except Exception as e:
                _, _, o_tb = sys.exc_info()
                o_trace = traceback.format_tb(o_tb)
                raise (o_trace)


class DaemonApp:
    __o_Config = None
    __s_Homedir = None
    __o_Threads = []
    __b_Stop = False
    __b_Quiet = False

    def __init__(self, v_quiet, v_homedir):
        self.__b_Quiet = v_quiet
        self.__s_Homedir = v_homedir


    def run(self):
        '''
            o_th = CustomThread(10)
            self.__o_Threads.append(o_th)
            o_th.setDaemon(True)
            o_th.start()
        '''

        try:
            while not self.__b_Stop:
                print('test')
                self.check_threads()
                time.sleep(5)

        except Exception as e:
            self.__b_Stop = True
            o_tb = traceback.format_exc()
            self.print_msg("Err, " + str(e) + "\n" + o_tb)
            sys.exit(2)

    def signal(self, v_signum, v_frame):
        self.print_msg("Daemon is stopping...")
        self.print_msg('Arriaved signal :' + v_signum)
        self.__b_Stop = True
        self.print_msg("Daemon stopped")

    def check_threads(self):

        for o_th in self.__o_Threads:
            if o_th.isAlive() != True:
                o_th.join(10)

    def print_msg(self, v_msg):
        s_time = time.strftime("[%Y%m%d %H:%M:%S] ", time.localtime(time.time()))
        print(s_time + " : " + v_msg)
        sys.stdout.flush()

if __name__ == '__main__':
    o_parser = argparse.ArgumentParser(description='daemon process...')
    o_parser.add_argument('--quiet',
                          help='whether stdout use or not',
                          required=False,
                          action='store_true')
    o_parser.add_argument('-p', '--pid',
                          type=str,
                          help='name of pid file',
                          required=False,
                          default='daemon.pid')
    o_parser.add_argument('--home',
                          help='location of home directory',
                          required=False,
                          default='./')
    o_args = o_parser.parse_args()

    s_pid = str(os.getpid())
    o_file = open(o_args.pid, 'w')
    o_file.write(s_pid)
    o_file.close()

    o_mon = DaemonApp(o_args.quiet, o_args.home)
    signal.signal(signal.SIGTERM, o_mon.signal)
    o_mon.run()
