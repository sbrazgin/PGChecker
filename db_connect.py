import psycopg2
import configparser
import decimal


class DBconnect:

    def readParamFile(self):
        config = configparser.ConfigParser()
        config.read(self.nameParamFile)

        self.hostName = config['DB']['hostName']
        self.portNumber = config['DB']['portNumber']
        self.database = config['DB']['database']
        self.username = config['DB']['username']
        self.password = config['DB']['password']

        self.logger.debug("hostName="+self.hostName)
        self.logger.debug("portNumber="+self.portNumber)
        self.logger.debug("database="+self.database)
        self.logger.debug("username="+self.username)
        self.logger.debug("password="+self.password)

    def __init__(self, nameParamFile, logger):
        self.nameParamFile = nameParamFile
        self.logger = logger
        self.readParamFile()


    def connect(self):
        self.conn = psycopg2.connect(dbname=self.database,
                                user=self.username,
                                password=self.password,
                                host=self.hostName)


    def close(self):
        self.conn.close()

    def runSql(self, sqlText):
        cursor = self.conn.cursor()

        cursor.execute(sqlText)
        records = cursor.fetchall()

        result = 0.0
        for row in records:
            #print(row)
            #result = "{0:0.6f}".format(decimal.Decimal(row))
            result = float(row[0])
            self.logger.debug("result="+str(result))

        cursor.close()
        return result