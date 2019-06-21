#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  Sergey Brazgin 05/2019
  sbrazgin@mail.ru
  Simple PostgreSql check
"""

import psycopg2
import configparser
from typing import List


class DbConnect(object):

    DEFAULT_ROLE = 'standalone'
    DEFAULT_VERSION = 0

    # -----------------------------------------------------------------------------------
    def __init__(self, file_name: str, logger):
        self._nameParamFile = file_name
        self._logger = logger

        self._is_connected = False
        self._error_desc = ""

        self._version = DbConnect.DEFAULT_VERSION
        self._role = DbConnect.DEFAULT_ROLE

        config = configparser.ConfigParser()
        config.read(self._nameParamFile)

        # mandatory
        self._hostName = config['DB']['hostName']
        self._portNumber = config['DB']['portNumber']
        self._database = config['DB']['database']
        self._username = config['DB']['username']
        self._password = config['DB']['password']

        # optional
        if 'DB_OPTIONS' in config.sections():
            opt_par = config['DB_OPTIONS']
            self._version = int(opt_par.get('version', 0))
            self._role = opt_par.get('role', 'unknown')

        # debug info
        self._logger.debug("DB par load: host=" + self._hostName +
                           ", port=" + self._portNumber +
                           ", database=" + self._database +
                           ", username=" + self._username +
                           ", password=" + self._password +
                           ", version=" + str(self.version) +
                           ", role=" + self._role)

        try:
            self.conn = psycopg2.connect(dbname=self._database,
                                         user=self._username,
                                         password=self._password,
                                         host=self._hostName)
        except psycopg2.OperationalError as e:
            self._error_desc = str(e)
            self._logger.error('---------------------------------------')
            self._logger.error("Unable to connect! ")
            self._logger.error(self._error_desc)
            self._logger.error('Params to connect: ' + self.desc_ext)
            self._logger.error('---------------------------------------')
        else:
            self._logger.debug("Connected!")
            self._is_connected = True

    # -- public -------------------------------------------------------------------------
    @property
    def version(self):
        return self._version

    @property
    def role(self):
        return self._role

    @property
    def desc(self):
        return f'host={self._hostName}, port={self._portNumber}, database={self._database}, role={self._role}'

    @property
    def desc_ext(self):
        return self.desc + ', user=' + self._username + ', password=' + self._password

    @property
    def error_desc(self):
        return self._error_desc

    @property
    def is_connect(self):
        return self._is_connected

    # -----------------------------------------------------------------------------------
    def close(self) -> None:
        self.conn.close()

    # -----------------------------------------------------------------------------------
    def run_sql_float(self, sql_text: str) -> float:
        cursor = self.conn.cursor()

        cursor.execute(sql_text)
        records = cursor.fetchall()

        result = 0.0
        for row in records:
            result = float(row[0])
            self._logger.debug("result=" + str(result))

        cursor.close()
        return result

    # -----------------------------------------------------------------------------------
    def run_sql_int(self, sql_text: str) -> int:
        cursor = self.conn.cursor()

        cursor.execute(sql_text)
        records = cursor.fetchall()

        result = 0
        for row in records:
            result = int(row[0])
            self._logger.debug("result=" + str(result))

        cursor.close()
        return result

    # -----------------------------------------------------------------------------------
    def run_sql_str(self, sql_text: str) -> str:
        cursor = self.conn.cursor()

        cursor.execute(sql_text)
        records = cursor.fetchall()

        result = ''
        for row in records:
            result = str(row[0])
            self._logger.debug("result=" + result)

        cursor.close()
        return result

    # -----------------------------------------------------------------------------------
    def run_sql_table(self, sql_text: str) -> List:
        cursor = self.conn.cursor()

        cursor.execute(sql_text)
        records = cursor.fetchall()
        result = []
        for row in records:
            str1 = str(row[0])
            result.append(str1)
            self._logger.debug("result next string=" + str1)

        cursor.close()
        return result

    # -----------------------------------------------------------------------------------
