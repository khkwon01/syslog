# -*- coding: utf-8 -*-

import os
import traceback


from flask import Flask, jsonify, Config
#from flask_wtf.csrf import CSRFProtect
from flask_babel import Babel
#from celery import Celery        # batch job execution
import logging
from logging.handlers import TimedRotatingFileHandler
import lib.commonhttpcode as http_status
from lib.web.base import base


""" debugging, break point : import pdb; pdb.set_trace()  """

class Api:
        __o_Instance = None
        __o_ApiServer = Flask(__name__)
        __o_Logger = None
        __o_Babel = None

        def __new__(cls, *args, **kwargs):
            if Api.__o_Instance is None:
                Api.__o_Instance = object.__new__(cls)

            return Api.__o_Instance

        def __init__(self, v_config_file=None):
            try :
                """ read config for env """
                self.__o_ApiServer.config.from_pyfile(v_config_file, silent=True)
                self.s_env = self.__o_ApiServer.config['ENV']

                """ initialize log object """
                self.s_servicename = self.__o_ApiServer.config['SERVICE_NAME']
                self.s_logdir = self.__o_ApiServer.config['LOG_PATH']
                self.s_loglevel = self.__o_ApiServer.config['LOG_LEVEL']
                self.__o_ApiServer.secret_key = self.__o_ApiServer.config['SERVICE_SECRET_KEY']

                """ initalize log info"""
                o_LogFormatter = logging.Formatter('[%(asctime)s %(pathname)s %(lineno)d] : %(levelname)s %(message)s')
                o_LogHandler = TimedRotatingFileHandler(os.path.abspath(self.s_logdir) + \
                                "/" + self.s_servicename + ".log", when='midnight', interval=1, backupCount=7)
                o_LogHandler.setFormatter(o_LogFormatter)
                self.__o_ApiServer.logger.setLevel(self.s_loglevel)
                self.__o_ApiServer.logger.addHandler(o_LogHandler)

                if self.s_env == "dev":
                        self.print_config(self.__o_ApiServer.config.items())
                        self.__o_ApiServer.logger.setLevel(10)        # debug

                """ support to multilanguage """
                self.__o_Babel = Babel(self.__o_ApiServer)

                """ register web application """
                self.__o_ApiServer.register_blueprint(base)

                self.__o_ApiServer.logger.info(self.s_servicename + " web service start...")

            except Exception as e:
                s_trackmsg = traceback.format_exc()
                if self.__o_ApiServer.logger != None:
                        self.__o_ApiServer.logger.error("Err :" + str(e) + "\n" + s_trackmsg)
                else:
                        print("Err :" + e.message['desc'] + "\n" + s_trackmsg)

        """ handle global http error of 404 """
        @__o_ApiServer.errorhandler(404)
        def http_error_pagenotfound(v_error):
            return jsonify( { 'code' : http_status.HTTP_404_NOT_FOUND, \
                                  'Desc' : str(v_error)  } ), 404

        """ handle global http error of 500 """
        @__o_ApiServer.errorhandler(500)
        def http_error_internalerr(v_error):
            return jsonify( { 'code' : http_status.HTTP_500_INTERNAL_SERVER_ERROR, \
                                  'desc' : str(v_error)  } ), 500
        def get_api(self):
            return self.__o_ApiServer

        def get_babel(self):
                return self.__o_Babel

        def print_config(self, v_config):
                print('===================================')
                print('         config setting            ')
                print('===================================')
                for s_key, s_value in v_config:
                        print('%s : %s' % (s_key, s_value))
                print('===================================')


if __name__ == '__main__':

        o_Api = Api("conf/config.conf")
        o_app = o_Api.get_api()

        o_app.run(debug=False, port=8080)