# -*- coding: utf-8 -*-

import httplib2
import pprint
from lib.commonlog import Log
from json import loads, dumps

'''
    class : Sms
    description : send message to mobile phone
'''

class Sms(object):
    def __init__(self, v_logger, v_smsconf):
        self.__o_Logger = v_logger
        self.__o_SmsConf = v_smsconf
        self.__o_MsgObj = {}

        self.__o_Logger.write_log(Log.DEBUG, pprint.saferepr(v_smsconf))

    def __check_config(self):
        s_msg = None

        if self.__o_SmsConf['api'] is None:
            s_msg = "Missed value for api url"

        if self.__o_SmsConf['cmpgroup'] is None:
            self.__o_MsgObj['cmp_msg_group_id'] = 4
        else :
            self.__o_MsgObj['cmp_msg_group_id'] = self.__o_SmsConf['cmpgroup']

        if self.__o_SmsConf['userid'] is None:
            self.__o_MsgObj['user_id'] = "db"
        else :
            self.__o_MsgObj['user_id'] = self.__o_SmsConf['userid']

        if self.__o_SmsConf['sndphnid'] is None:
            self.__o_MsgObj['snd_phn_id'] = "010-7777-7777"
        else:
            self.__o_MsgObj['snd_phn_id'] = self.__o_SmsConf['sndphnid']

        if self.__o_SmsConf['rcvphnid'] is None:
            s_msg = "Missed value for reciver number"
        else:
            self.__o_MsgObj['rcv_phn_id'] = self.__o_SmsConf['rcvphnid']

        return s_msg

    def send_msg(self, v_message, v_recv_number=None):
        o_resp = {}
        o_httpobj = httplib2.Http()
        o_resp['status'] = 499

        s_msg = self.__check_config()

        if s_msg is None:
            if v_recv_number is not None:
                self.__o_MsgObj['rcv_phn_id'] = v_recv_number
            self.__o_MsgObj['snd_msg'] = v_message
            s_recv_number = self.__o_MsgObj['rcv_phn_id']

            for self.__o_MsgObj['rcv_phn_id'] in s_recv_number.strip().split(","):
                self.__o_Logger.write_log(Log.INFO, "sms message sent : " + self.__o_MsgObj['rcv_phn_id'])
                try:
                    o_resp, s_resmsg = o_httpobj.request( uri = self.__o_MsgObj['api'],
                                                          method = 'POST',
                                                          headers = {"Content-Type" : "application/json", "charset" : "utf-8"},
                                                          body = dumps(self.__o_MsgObj) )
                    self.__o_Logger.write_log(Log.INFO, "sms : " + dumps(self.__o_MsgObj) + "\n")
                    self.__o_Logger.write_log(Log.INFO, "sms return code : " + s_resmsg + "\n")
                except Exception as e:
                    self.__o_Logger.write_log(Log.ERROR, "sms api call error : " + str(e))
        else:
            self.__o_Logger.write_log(Log.DEBUG, s_msg)

        return o_resp['status']


if __name__ == '__main__':
    s_logfile = "./"
    o_log = Log(s_logfile, "test.log", "DEUBG")
    o_sms = Sms(o_log, None)

    try :
        o_sms.send_msg("test...")
    except Exception as e:
        print(str(e))