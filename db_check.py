#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  Sergey Brazgin 05/2019
  sbrazgin@mail.ru
  Simple PostgreSql check
"""

import configparser
from typing import List


class DbCheck:

    DEFAULT_ROLE = 'unknown'
    DEFAULT_VER = 0

    # -----------------------------------------------------------------------------------
    def __init__(self, file_name, logger):
        self._file_name = file_name
        self._logger = logger
        self._logger.debug('db ini file = ' + file_name)

        self.desc = ''
        self.type = ''
        self.version = DbCheck.DEFAULT_VER
        self.role = DbCheck.DEFAULT_ROLE

        self._logger.debug("--------")
        self._logger.debug("Load check: nameFile=" + self._file_name)

        config = configparser.ConfigParser()
        config.read(self._file_name)
        opt_par = config['SQL']
        self.sqlText = opt_par.get('check_sql')

        opt_par = config['check']
        self.desc = opt_par.get('desc')
        self.type = opt_par.get('type')

        self._logger.debug("sqlText = " + self.sqlText)
        self._logger.debug("desc = " + self.desc)
        self._logger.debug("type = " + self.type)

        if self.type == 'check_float' or self.type == 'check_int':
            self._ok_min_value = config['check']['ok_min_value']
            self._ok_max_value = config['check']['ok_max_value']
            self._warning_min_value = config['check']['warning_min_value']
            self._warning_max_value = config['check']['warning_max_value']

            self._logger.debug("ok_min_value = " + self._ok_min_value)
            self._logger.debug("ok_max_value = " + self._ok_max_value)
            self._logger.debug("warning_min_value = " + self._warning_min_value)
            self._logger.debug("warning_max_value = " + self._warning_max_value)

        elif self.type == 'check_str':
            self._ok_value = opt_par.get('ok_value', '')
            self._logger.debug("ok_value = " + self._ok_value)

        # optional
        if 'DB_OPTIONS' in config.sections():
            opt_par = config['DB_OPTIONS']
            self.version = int(opt_par.get('version', 0))
            self.role = opt_par.get('role', 'unknown')

        self._logger.debug("version=" + str(self.version))
        self._logger.debug("role=" + self.role)

    # -----------------------------------------------------------------------------------
    def check_float_value(self, value) -> List:
        result = [self.desc, value]
        o1 = float(self._ok_min_value)
        o2 = float(self._ok_max_value)
        w1 = float(self._warning_min_value)
        w2 = float(self._warning_max_value)
        if o1 <= value <= o2:
            result.append("OK")
        elif w1 <= value <= w2:
            result.append("Warning")
        else:
            result.append("Error")
        return result

    # -----------------------------------------------------------------------------------
    def check_str_value(self, value: str) -> List:
        result = [self.desc, value]
        if self._ok_value == '':
            result.append("")
        elif self._ok_value == value:
            result.append("OK")
        else:
            result.append("Error")
        return result

    # -----------------------------------------------------------------------------------
    def check_int_value(self, value: int) -> List:
        result = [self.desc, value]
        o1 = int(self._ok_min_value)
        o2 = int(self._ok_max_value)
        w1 = int(self._warning_min_value)
        w2 = int(self._warning_max_value)
        if o1 <= value <= o2:
            result.append("OK")
        elif w1 <= value <= w2:
            result.append("Warning")
        else:
            result.append("Error")
        return result
