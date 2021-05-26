import contextlib
import sqlite3
import json

class SqliteProvider(object):

    def __init__(self, v_db_file_path):
        self.__Conn = sqlite3.connect(v_db_file_path)
        self.__Retries = 10

    def save_data_info(self, v_info):
        s_query = "insert into info values(?, ?, ?);"
        s_values = ('1', json.dumps(v_info), '2' )

        self.execute_query(s_query, s_values)

    def execute_query(self, v_query, v_values=None):

        with contextlib.closing(self.__Conn.cursor()) as o_cursor:
            b_Clt = False
            i_counter = 0

            while i_counter < self.__Retries and not b_Clt :
                i_counter += 1

                try:
                        o_cursor.execute(v_query, v_values)
                        self.__Conn.commit()
                        b_Clt = True
                except Exception as e:
                    raise (e)