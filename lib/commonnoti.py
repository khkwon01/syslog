# -*- coding: utf-8 -*-

import abc
import httplib2
from lib.commonlog import Log

'''
    class : Noti
    description : interface for noti
'''


class Noti(object):
    __metaclass__ = abc.ABCMeta

    def send_msg(self, v_chankey, v_title, v_message): pass

    def add_channels(self, v_channel): pass

    def add_channel(self, v_key, v_value): pass


'''
    class : JandiNoti
    description : send message to jandi
'''


class JandiNoti(Noti):
    __o_Instance = None
    __o_JandiChannl = {}

    def __init__(self, v_logger, v_channel=None):
        self.o_logger = v_logger
        if v_channel is not None:
            self.__o_JandiChannl = v_channel

    def __new__(cls, *args, **kwargs):
        if JandiNoti.__o_Instance is None:
            JandiNoti.__o_Instance = object.__new__(cls)

        return JandiNoti.__o_Instance

    def add_channel(self, v_key, v_value):
        self.__o_JandiChannl[v_key] = v_value

    def add_channels(self, v_channel):
        self.__o_JandiChannl.update(v_channel)

    def send_msg(self, v_chankey, v_title, v_message):
        o_resp = None
        s_apiurl = None
        o_httpobj = httplib2.Http()

        s_headers = {'Accept': "application/vnd.tosslab.jandi-v2+json",
                     'Content-Type': "application/json", 'charset': "utf-8"}
        s_sendmsg = '{{ "body" : "notify", "connectColor" : "FAC11B", \
                            "connectInfo" : [{{ "title" : "{0}", "description" : "{1}" }}] }}'
        s_apiurl = self.__o_JandiChannl.get(v_chankey)

        try:
            o_resp, s_resmsg = o_httpobj.request(uri=s_apiurl,
                                                 method='POST',
                                                 headers=s_headers,
                                                 body=s_sendmsg.format(v_title, v_message))
            self.o_logger.write_log(Log.INFO, "Jandi api return code : " + str(s_resmsg))
        except Exception as e:
            self.o_logger.write_log(Log.ERROR, "Jandi api call error :" + str(e))


if __name__ == '__main__':
    s_logfile = "./"
    o_log = Log(s_logfile, "test.log", "DEBUG")
    o_noti = JandiNoti(o_log)
    o_noti.add_channel("test", "https://wh.jandi.com/connect-api/webhook/13352731/137ccd9dec67b319b34f6d67b2916095")

    o_noti.send_msg("test", "test", "kkkkkk")
