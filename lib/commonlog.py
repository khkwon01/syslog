# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers


class Log(object):
    __o_Instance = None
    ERROR, INFO, WARN, DEBUG, CRIT = range(5)

    def __init__(self, v_logdir, v_logname=None, v_appname='root', v_loglevel='DEBUG'):
        self.i_level = 0
        self.o_Logger = None
        self.s_LogDir = v_logdir
        self.s_LogName = '/client.log'
        self.s_AppName = v_appname
        self.s_Loglevel = v_loglevel

        if v_logname is not None:
            self.s_LogName = v_logname
        if not os.path.exists(v_logdir):
            raise Exception("log directory is not exist : " + v_logdir)

        self.setup_logenv()
        self.set_loglevel(v_loglevel)

    def __new__(cls, *args, **kwargs):
        if Log.__o_Instance is None:
            Log.__o_Instance = object.__new__(cls)

        return Log.__o_Instance

    def set_loglevel(self, v_loglevel='INFO'):
        if v_loglevel == 'DEBUG':
            self.i_level = logging.DEBUG
        elif v_loglevel == 'CRITICAL':
            self.i_level = logging.CRITICAL
        elif v_loglevel == 'WARN':
            self.i_level = logging.WARNING
        elif v_loglevel == 'ERROR':
            self.i_level = logging.INFO

    def get_loglevel(self):
        return self.s_Loglevel

    def setup_logenv(self):
        self.o_Logger = logging.getLogger(self.s_AppName)
        o_logformatter = logging.Formatter('[%(asctime)s %(pathname)s %(lineno)d] : %(levelname)s %(message)s')
        o_logfandler = logging.handlers.TimedRotatingFileHandler(
            os.path.abspath(self.s_LogDir) + "/" + self.s_LogName, when='midnight', interval=1, backupCount=7)
        o_logfandler.setFormatter(o_logformatter)
        self.o_Logger.addHandler(o_logfandler)

    def write_log(self, v_loglevel, v_message):
        if v_loglevel == self.DEBUG:
            self.o_Logger.debug(v_message)
        elif v_loglevel == self.WARN:
            self.o_Logger.warning(v_message)
        elif v_loglevel == self.ERROR:
            self.o_Logger.error(v_message)
        elif v_loglevel == self.CRIT:
            self.o_Logger.critical(v_message)
        else:
            self.o_Logger.info(v_message)
