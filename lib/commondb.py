# -*- coding: utf-8 -*-


import contextlib
import sqlite3
import redis
import json
import mysql.connector
from lib.commonutil import convert_to_epoch


class Sqlite3db(object):
   def __init__(self, v_db_path):
      self.__Conn = sqlite3.connect(v_db_path, check_same_thread=False)
      self.__Retries = 10

   def execute_sql(self, v_query, v_values=None):
      o_result = None

      with contextlib.closing(self.__Conn.cursor()) as o_cursor:
          b_Clt = False
          i_counter = 0

          while i_counter < self.__Retries and not b_Clt:
             i_counter += 1

             try:
                if v_values is None:
                    o_cursor.execute(v_query)
                else :
                    o_cursor.execute(v_query, v_values)
                self.__Conn.commit()
                b_Clt = True
             except Exception as e:
                raise (e)

          o_result = o_cursor.fetchall()

      return o_result

   def disconnect(self):
      if self.__Conn is not None :  self.__Conn.close()


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


class MySQLProvider(object):
    def __init__(self, v_host='localhost', v_port='3306', v_database='test', v_user='', v_password=''):
        self.o_mysqlconn = None
        self.o_cursor = None
        self.s_sql = None

        try:
            self.o_mysqlconn = mysql.connector.connect(user=v_user, password=v_password,
                                                       host=v_host, port=v_port, database=v_database)
            self.o_cursor = self.o_mysqlconn.cursor(buffered=True, dictionary=True)

            print(f'connect : { self.o_mysqlconn.is_connected() }')
            self.s_sql = "select connection_id();"
            o_result = self.execute_sql(self.s_sql)
            print(f'connection id : { o_result["connection_id()"] }')

        except mysql.connector.Error as e:
            print(f'error : {e}')
            raise e

    def execute_sql(self, v_sql, v_params=None):
        self.o_result = None

        self.o_cursor.execute(v_sql, v_params)

        if v_sql.lower().find("select") >= 0:
            if self.o_cursor.rowcount < 2:
                self.o_result = self.o_cursor.fetchone()
            else:
                self.o_result = self.o_cursor.fetchall()
        else:
            self.o_result = self.o_cursor.lastrowid

        return self.o_result

    def disconnect(self):

        if self.o_cursor is not None:
            self.o_cursor.close()

        if self.o_mysqlconn is not None:
            self.o_mysqlconn.disconnect()


if __name__ == '__main__':
    s_host = '10.22.0.12'
    s_port = '3306'
    s_db = 'mysql'
    s_user = 'dbadmin@qa-gasp-admin-db01'
    s_pass = '1tksdbok@#'
    s_sql = "select * from mysql.user"

    o_db = MySQLProvider(s_host, s_port, s_db, s_user, s_pass)
    o_result = o_db.execute_sql(s_sql)
    for o_item in o_result:
        print(f'{ o_item["Host"], o_item["User"] }')
    o_db.disconnect()
