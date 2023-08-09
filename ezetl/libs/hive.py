from pyhive import hive
import pandas as pd


class HiveClient(object):
    def __init__(self, **kwargs):
        """
        host
        port
        username
        password
        database
        """
        self._conn = hive.Connection(**kwargs)

    def create_database(self, database):
        '''
        创建数据库
        '''
        sql = f"create database {database}"
        curosr = self._conn.cursor()
        curosr.execute(sql)
        self._conn.close()

    def get_list_database(self):
        '''
        获取数据库列表
        '''
        cursor = self._conn.cursor()
        cursor.execute('show databases')
        result = cursor.fetchall()
        return result

    def get_tables(self):
        '''
        获取数据库中的表
        '''
        cursor = self._conn.cursor()
        cursor.execute('show databases')
        result = cursor.fetchall()
        return result

    def drop_table(self, table):
        '''
        删除数据库中的表
        '''
        sql = f'''drop table if exists {table}'''
        print(sql)
        cursor = self._conn.cursor()
        cursor.execute(sql)
        self._conn.close()

    def execute(self, sql):
        """
        执行sql
        """
        cursor = self._conn.cursor()
        cursor.execute(sql)
        cursor.execute(sql)
        self._conn.close()

    def query(self, sql):
        """
        返回查询结果列表
        时间默认为秒返回
        """
        cursor = self._conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    def query_as_df(self, sql):
        """
        返回查询结果列表
        时间默认为秒返回
        """
        cursor = self._conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        df = pd.DataFrame(result)
        return df



