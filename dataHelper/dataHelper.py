# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time   : 2019/4/8 18:24
# @Author : WuZe
# @Desc   :
# ==================================================

import os
import configparser
import pymysql.cursors


class DataHelper:
    def __init__(self, filepath='config/db.ini'):
        self.config = {}
        curpath = os.path.realpath(filepath)
        self.__get_config(curpath)

    @classmethod
    def instance(cls, filepath='config/db.ini'):
        return cls(filepath)

    def __get_config(self, filepath):
        conf = configparser.ConfigParser()
        conf.read(filepath, encoding="utf-8")
        items = conf.items("DATABASE")
        varitems = "host,user,password,database,port,unix_socket,charset,sql_mode,read_default_file,conv,use_unicode,client_flag,cursorclass,init_command,connect_timeout,ssl,read_default_group,compress,named_pipe,autocommit,db,passwd,local_infile,max_allowed_packet,defer_connect,auth_plugin_map,read_timeout,write_timeout,bind_address,binary_prefix,program_name,server_public_key"
        varitems = varitems.split(',')
        for item in items:
            if item[0] in varitems:
                self.config[item[0].lower()] = item[1]
        if 'port' in self.config:
            self.config['port'] = int(self.config['port'])
        if 'client_flag' in self.config:
            self.config['client_flag'] = int(self.config['client_flag'])
        if 'connect_timeout' in self.config:
            self.config['connect_timeout'] = int(self.config['connect_timeout'])
        if 'max_allowed_packet' in self.config:
            self.config['max_allowed_packet'] = int(self.config['max_allowed_packet'])
        if 'auth_plugin_map' in self.config:
            self.config['auth_plugin_map'] = int(self.config['auth_plugin_map'])
        if 'autocommit' in self.config:
            self.config['autocommit'] = self.config['autocommit'] == str(True)
        if 'local_infile' in self.config:
            self.config['local_infile'] = self.config['local_infile'] == str(True)
        if 'defer_connect' in self.config:
            self.config['defer_connect'] = self.config['defer_connect'] == str(True)
        if 'binary_prefix' in self.config:
            self.config['binary_prefix'] = self.config['binary_prefix'] == str(True)

    def transaction(self, sqlList):
        """
        执行事务
        :param sqlList: sql集合
        :return: 影响行数
        """
        i = 0
        connection = pymysql.connect(**self.config)
        cur = connection.cursor()
        try:
            for sql in sqlList:
                cur.execute(sql)
                i = i + 1
            connection.commit()
        except Exception as e:
            print('error:', sqlList[i])
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
        connection = pymysql.connect(**self.config)
        cur = connection.cursor()
        try:
            num = cur.execute(sql)
            connection.commit()
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
        # print(cls.config)
        connection = pymysql.connect(**self.config)
        cur = connection.cursor()
        try:
            cur.execute(sql)
            _ = cur.fetchall()
            fields = cur.description
            result = []
            for row in range(cur.rowcount):
                data = {}
                for col, field in enumerate(fields):
                    data[field[0]] = _[row][col]
                result.append(data)
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
            _ = cur.fetchone()
            fields = cur.description
            result = {}
            for col, field in enumerate(fields):
                result[field[0]] = _[col]
            return result
        except Exception as e:
            raise e
        finally:
            connection.close()

    def callproc(self, procname, args=()):
        """
        执行存储过程
        :param procname: 存储过程名称
        :param args: 参数
        :return: 结果
        """
        connection = pymysql.connect(**self.config)
        cur = connection.cursor()
        try:
            result = list()
            cur.callproc(procname, args)
            while True:
                _ = cur.fetchall()
                data = []
                fields = cur.description
                if cur.rowcount == 0:
                    data = None
                else:
                    for row in range(cur.rowcount):
                        data_ = {}
                        for col, field in enumerate(fields):
                            data_[field[0]] = _[row][col]
                        data.append(data_)
                result.append(data)
                if not cur.nextset():
                    break
            return result
        except Exception as e:
            raise e
        finally:
            connection.close()
