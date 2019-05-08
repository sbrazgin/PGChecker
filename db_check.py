import configparser

class DBcheck:

    def __init__(self, nameParamFile, logger):
        self.nameParamFile = nameParamFile
        self.logger = logger
        self.readParamFile()

    def setCheck(self):
        pass

    def readParamFile(self):
        config = configparser.ConfigParser()
        config.read(self.nameParamFile)
        self.sqlText = config['SQL']['check_sql']
        self.logger.debug("sqlText = "+self.sqlText)

        self.desc = config['check']['desc']
        self.column = config['check']['column']
        self.ok_min_value = config['check']['ok_min_value']
        self.ok_max_value = config['check']['ok_max_value']
        self.warning_min_value = config['check']['warning_min_value']
        self.warning_max_value = config['check']['warning_max_value']

        self.logger.debug("desc = "+self.desc)
        self.logger.debug("column = "+self.column)
        self.logger.debug("ok_min_value = "+self.ok_min_value)
        self.logger.debug("ok_max_value = "+self.ok_max_value)
        self.logger.debug("warning_min_value = "+self.warning_min_value)
        self.logger.debug("warning_max_value = "+self.warning_max_value)

    def checkValue(self,valueSql):
        if float(self.ok_min_value) <= valueSql and float(self.ok_max_value) >= valueSql:
            self.logger.info(self.desc+" OK")
        elif float(self.warning_min_value) <= valueSql and float(self.warning_max_value) >= valueSql:
            self.logger.info(self.desc+" Warning")
        else:
            self.logger.info(self.desc +" Error"+" Value="+str(valueSql))
