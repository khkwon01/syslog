import contextlib
import sqlite3
import json
import mysql.connector
import pprint


class SqliteProvider(object):

    def __init__(self, v_db_file_path):
        self.__Conn = sqlite3.connect(v_db_file_path)
        self.__Retries = 10

    def save_data_info(self, v_info):
        s_query = "insert into info values(?, ?, ?);"
        s_values = ('1', json.dumps(v_info), '2')

        self.execute_query(s_query, s_values)

    def execute_query(self, v_query, v_values=None):

        with contextlib.closing(self.__Conn.cursor()) as o_cursor:
            b_Clt = False
            i_counter = 0

            while i_counter < self.__Retries and not b_Clt:
                i_counter += 1

                try:
                    o_cursor.execute(v_query, v_values)
                    self.__Conn.commit()
                    b_Clt = True
                except Exception as e:
                    raise (e)


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
