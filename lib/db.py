# coding:utf-8

import pymysql.cursors


class DB:
    config = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "root",
        "db": "base",
        "charset": "utf8"
    }

    def __init__(self):
        self.version = '1.0'

    def doTrans(self, sqlList):
        """
        执行事务
        :param sqlList: sql集合
        :return: 影响行数
        """
        i = 0
        connection = pymysql.connect(**self._config)
        cur = connection.cursor()
        try:
            for sql in sqlList:
                cur.execute(sql)
                i = i + 1
            connection.commit()
        except Exception as e:
            i = 0
            connection.rollback()
            raise e
        finally:
            connection.close()
        return i

    def execute(self, sql):
        """
        执行一条sql
        :param sql: 需要执行的sql
        :return: 影响行数
        """
        connection = pymysql.connect(**self._config)
        cur = connection.cursor()
        try:
            num = cur.execute(sql)
        except Exception as e:
            num = 0
            connection.rollback()
            raise e
        finally:
            connection.close()
        return num

    def fetchall(self, sql):
        """
        根据sql返回集合
        :param sql: 需要执行的sql
        :return: 集合
        """
        print self.config
        connection = pymysql.connect(**self.config)
        cur = connection.cursor()
        try:
            cur.execute(sql)
            result = cur.fetchall()
            return result
        except Exception as e:
            raise e
        finally:
            connection.close()

    def fetchone(self, sql):
        """
        根据sql返回第一个
        :param sql: 需要执行的sql
        :return: 结果
        """
        connection = pymysql.connect(**self.config)
        cur = connection.cursor()
        try:
            cur.execute(sql)
            result = cur.fetchone()
            return result
        except Exception as e:
            raise e
        finally:
            connection.close()
