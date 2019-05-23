import configparser
from typing import List

class DBcheck:

    DEFAULT_ROLE = 'unknown'

    # -----------------------------------------------------------------------------------
    def __init__(self, nameParamFile, logger):
        self._nameParamFile = nameParamFile
        self._logger = logger

        self.desc = ''
        self.type = ''
        self.version = 0
        self.role = DBcheck.DEFAULT_ROLE

        self.__readParamFile__()

    # -----------------------------------------------------------------------------------
    def __readParamFile__(self) -> None:
        self._logger.debug("--------")
        self._logger.debug("nameParamFile=" + self._nameParamFile)

        config = configparser.ConfigParser()
        config.read(self._nameParamFile)
        opt_par = config['SQL']
        self.sqlText = opt_par.get('check_sql')

        opt_par = config['check']
        self.desc = opt_par.get('desc')
        self.type = opt_par.get('type')

        if self.type == 'check_float' or self.type == 'check_int':
            #self._column = config['check']['column']
            self._ok_min_value = config['check']['ok_min_value']
            self._ok_max_value = config['check']['ok_max_value']
            self._warning_min_value = config['check']['warning_min_value']
            self._warning_max_value = config['check']['warning_max_value']

            #self._logger.debug("column = " + self._column)
            self._logger.debug("ok_min_value = " + self._ok_min_value)
            self._logger.debug("ok_max_value = " + self._ok_max_value)
            self._logger.debug("warning_min_value = " + self._warning_min_value)
            self._logger.debug("warning_max_value = " + self._warning_max_value)

        if self.type == 'check_str':
            #self._column = opt_par.get('column', '')
            self._ok_value = opt_par.get('ok_value', '')
            #self._logger.debug("column = " + self._column)
            self._logger.debug("ok_value = " + self._ok_value)


        # optional
        if 'DB_OPTIONS' in config.sections():
            opt_par = config['DB_OPTIONS']
            self.version = int(opt_par.get('version',0))
            self.role = opt_par.get('role','unknown')

        # debug
        self._logger.debug("sqlText = " + self.sqlText)
        self._logger.debug("desc = " + self.desc)
        self._logger.debug("type = " + self.type)

        self._logger.debug("version=" + str(self.version))
        self._logger.debug("role=" + self.role)


    # -----------------------------------------------------------------------------------
    # if type = check_float
    def checkFloatValue(self,valueSql) -> List:
        result=[self.desc, valueSql]
        if float(self._ok_min_value) <= valueSql and float(self._ok_max_value) >= valueSql:
            result.append("OK")
        elif float(self._warning_min_value) <= valueSql and float(self._warning_max_value) >= valueSql:
            result.append("Warning")
        else:
            result.append("Error")
        return result

    # -----------------------------------------------------------------------------------
    # if type = check_str
    def checkStrValue(self, valueSql: str) -> List:
        result = [self.desc, valueSql]
        if self._ok_value == '':
            result.append("")
        elif self._ok_value == valueSql :
            result.append("OK")
        else:
            result.append("Error")
        return result

    # -----------------------------------------------------------------------------------
    # if type = check_int
    def checkIntValue(self,valueSql: int) -> List:
        result=[self.desc, valueSql]
        if int(self._ok_min_value) <= valueSql and int(self._ok_max_value) >= valueSql:
            result.append("OK")
        elif int(self._warning_min_value) <= valueSql and int(self._warning_max_value) >= valueSql:
            result.append("Warning")
        else:
            result.append("Error")
        return result
