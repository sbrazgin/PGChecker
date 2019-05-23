import psycopg2
import configparser
from typing import List



class DBconnect(object):

    DEFAULT_ROLE = 'standalone'
    # -----------------------------------------------------------------------------------
    def __init__(self, nameParamFile: str, logger):
        self._nameParamFile = nameParamFile
        self._logger = logger

        self._is_connected = False
        self._error_desc = ""

        self.version = 0
        self.role = DBconnect.DEFAULT_ROLE

        self.__readParamFile__()

    # -----------------------------------------------------------------------------------
    def __readParamFile__(self) -> None:
        config = configparser.ConfigParser()
        config.read(self._nameParamFile)

        # mandatory
        self._hostName   = config['DB']['hostName']
        self._portNumber = config['DB']['portNumber']
        self._database = config['DB']['database']
        self._username = config['DB']['username']
        self._password = config['DB']['password']


        # optional
        if 'DB_OPTIONS' in config.sections():
            opt_par = config['DB_OPTIONS']
            self.version = int(opt_par.get('version', 0))
            self.role = opt_par.get('role', 'unknown')

        # debug info
        self._logger.debug("hostName=" + self._hostName)
        self._logger.debug("portNumber=" + self._portNumber)
        self._logger.debug("database=" + self._database)
        self._logger.debug("username=" + self._username)
        self._logger.debug("password=" + self._password)
        self._logger.debug("version=" + str(self.version))
        self._logger.debug("role=" + self.role)

    # -----------------------------------------------------------------------------------
    def getDescDatabase(self) -> str:
        return f'host={self._hostName}, port={self._portNumber}, database={self._database}, role={self.role}'

    # -----------------------------------------------------------------------------------
    def getDescDatabase2(self) -> str:
        return self.getDescDatabase() + ', user=' + self._username + ', password=' + self._password

    # -----------------------------------------------------------------------------------
    def getError(self) -> str:
        return self._error_desc

    # -----------------------------------------------------------------------------------
    def connect(self) -> None:
        self._is_connected = False
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
            self._logger.error('Params to connect: ' + self.getDescDatabase2())
            self._logger.error('---------------------------------------')
        else:
            self._logger.debug("Connected!")
            self._is_connected = True

    # -----------------------------------------------------------------------------------
    def is_connect(self) -> bool:
        return self._is_connected

    # -----------------------------------------------------------------------------------
    def close(self) -> None:
        self.conn.close()

    # -----------------------------------------------------------------------------------
    def runSqlFloat(self, sqlText: str) -> float:
        cursor = self.conn.cursor()

        cursor.execute(sqlText)
        records = cursor.fetchall()

        result = 0.0
        for row in records:
            result = float(row[0])
            self._logger.debug("result=" + str(result))

        cursor.close()
        return result

    # -----------------------------------------------------------------------------------
    def runSqlInt(self, sqlText: str) -> int:
        cursor = self.conn.cursor()

        cursor.execute(sqlText)
        records = cursor.fetchall()

        result = 0.0
        for row in records:
            result = int(row[0])
            self._logger.debug("result=" + str(result))

        cursor.close()
        return result

    # -----------------------------------------------------------------------------------
    def runSqlStr(self, sqlText: str) -> str:
        cursor = self.conn.cursor()

        cursor.execute(sqlText)
        records = cursor.fetchall()

        result = ''
        for row in records:
            result = str(row[0])
            self._logger.debug("result=" + result)

        cursor.close()
        return result

    # -----------------------------------------------------------------------------------
    def runSqlTable(self, sqlText: str) -> List:
        cursor = self.conn.cursor()

        cursor.execute(sqlText)
        records = cursor.fetchall()
        result = []
        for row in records:
            str1 = str(row[0])
            result.append(str1)
            self._logger.debug("result next string=" + str1)

        cursor.close()
        return result

    # -----------------------------------------------------------------------------------
