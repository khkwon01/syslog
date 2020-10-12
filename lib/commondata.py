# -*- coding: utf-8 -*-

import  redis
from lib.commonutil import convert_to_epoch

class RedisData(object):
    """A redis based persistance to store and fetch data"""

    __o_Instance = None

    def __new__(cls, *args, **kwargs):
        if RedisData.__o_Instance is None:
            RedisData.__o_Instance = object.__new__(cls)

        return RedisData.__o_Instance

    def __init__(self, v_server, v_port, v_db, v_passwd):
        self._s_server = v_server
        self._i_port = v_port
        self._s_db = v_db
        self._s_passwd = v_passwd

        self._o_conn = redis.StrictRedis(host=self._s_server, port=self._i_port,
                                         db=self._s_db, password=self._s_passwd)

    def change_db(self, v_db):
        """ Change db connection"""
        self._s_db = v_db
        self._o_conn = redis.StrictRedis(host=self._s_server, port=self._i_port,
                                         db=self._s_db, password=self._s_passwd)

    def save_login(self, v_userid, v_timestamp, v_userinfo):
        """ Save user login data,
            v_userid (str) : user id
            v_timestamp (datetime) : The time of user login
            v_userinfo (object) : user information
        """

        o_data = {
            "logintime" : str(convert_to_epoch(v_timestamp)),
            "userinfo" : v_userinfo
        }


        self._o_conn.sadd(v_userid, o_data)
        self._o_conn.expire(v_userid, 60 * 60 * 2)

    def save_data(self, v_key, v_value, v_ttl=86400):
        """ Save common string data """

        if v_ttl > 0 :
            self._o_conn.set(v_key, v_value, ex=v_ttl)
        elif v_ttl == 0 :
            self._o_conn.set(v_key, v_value, keepttl=True)

    def save_alter_info(self, v_hashkey, v_message, v_timestamp):
        """ save alter message """

        o_pipe = self._o_conn.pipeline()
        s_epoch = str(convert_to_epoch(v_timestamp))

        if self._o_conn.hexists(v_hashkey, "message") :
            o_pipe.hset(v_hashkey, "lastdt", s_epoch)
            o_pipe.hincrby(v_hashkey, "count", 1)
        else :
            o_pipe.hset(v_hashkey, "message", v_message)
            o_pipe.hset(v_hashkey, "lastdt", s_epoch)
            o_pipe.hset(v_hashkey, "noti", 1)
            o_pipe.hset(v_hashkey, "count", 1)

        o_pipe.execute()
        self._o_conn.expire(v_hashkey, 60 * 60)