# coding:utf-8

import pymysql.cursors


class DB:
    """
    :param host: Host where the database server is located
    :param user: Username to log in as
    :param password: Password to use.
    :param database: Database to use, None to not use a particular one.
    :param port: MySQL port to use, default is usually OK. (default: 3306)
    :param bind_address: When the client has multiple network interfaces, specify
        the interface from which to connect to the host. Argument can be
        a hostname or an IP address.
    :param unix_socket: Optionally, you can use a unix socket rather than TCP/IP.
    :param charset: Charset you want to use.
    :param sql_mode: Default SQL_MODE to use.
    :param read_default_file:
        Specifies  my.cnf file to read these parameters from under the [client] section.
    :param conv:
        Conversion dictionary to use instead of the default one.
        This is used to provide custom marshalling and unmarshaling of types.
        See converters.
    :param use_unicode:
        Whether or not to default to unicode strings.
        This option defaults to true for Py3k.
    :param client_flag: Custom flags to send to MySQL. Find potential values in constants.CLIENT.
    :param cursorclass: Custom cursor class to use.
    :param init_command: Initial SQL statement to run when connection is established.
    :param connect_timeout: Timeout before throwing an exception when connecting.
        (default: 10, min: 1, max: 31536000)
    :param ssl:
        A dict of arguments similar to mysql_ssl_set()'s parameters.
        For now the capath and cipher arguments are not supported.
    :param read_default_group: Group to read from in the configuration file.
    :param compress: Not supported
    :param named_pipe: Not supported
    :param autocommit: Autocommit mode. None means use server default. (default: False)
    :param local_infile: Boolean to enable the use of LOAD DATA LOCAL command. (default: False)
    :param max_allowed_packet: Max size of packet sent to server in bytes. (default: 16MB)
        Only used to limit size of "LOAD LOCAL INFILE" data packet smaller than default (16KB).
    :param defer_connect: Don't explicitly connect on contruction - wait for connect call.
        (default: False)
    :param auth_plugin_map: A dict of plugin names to a class that processes that plugin.
        The class will take the Connection object as the argument to the constructor.
        The class needs an authenticate method taking an authentication packet as
        an argument.  For the dialog plugin, a prompt(echo, prompt) method can be used
        (if no authenticate method) for returning a string from the user. (experimental)
    :param db: Alias for database. (for compatibility to MySQLdb)
    :param passwd: Alias for password. (for compatibility to MySQLdb)
    :param binary_prefix: Add _binary prefix on bytes and bytearray. (default: False)
    """

    def __init__(self, dbconfig):
        self._config = dbconfig

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    @config.deleter
    def config(self):
        del self._config

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
        connection = pymysql.connect(**self._config)
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
        connection = pymysql.connect(**self._config)
        cur = connection.cursor()
        try:
            cur.execute(sql)
            result = cur.fetchone()
            return result
        except Exception as e:
            raise e
        finally:
            connection.close()
