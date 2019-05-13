import psycopg2
import configparser
import decimal


class DBconnect(object):

    # -----------------------------------------------------------------------------------
    def __init__(self, nameParamFile, logger):
        self.nameParamFile = nameParamFile
        self.logger = logger
        self.readParamFile()
        self.is_connected = False

    # -----------------------------------------------------------------------------------
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


    # -----------------------------------------------------------------------------------
    def getDescDatabase(self):
        return "hostName="+self.hostName+", "+"portNumber="+self.portNumber+", "+ "database="+self.database

    # -----------------------------------------------------------------------------------
    def connect(self):
        self.is_connected = False
        try:
            self.conn = psycopg2.connect(dbname=self.database,
                                         user=self.username,
                                         password=self.password,
                                         host=self.hostName)
        except psycopg2.OperationalError as e:
        #except psycopg2.Error as e:
            self.logger.error('---------------------------------------')
            self.logger.error("Unable to connect! ")
            self.logger.error(str(e))
            self.logger.error('Params to connect: dbname='+self.database+',user='+self.username+',password='+self.password+'host='+self.hostName)
            self.logger.error('---------------------------------------')
        else:
            self.logger.debug("Connected!")
            self.is_connected = True


    # -----------------------------------------------------------------------------------
    def is_connect(self):
        return self.is_connected

    # -----------------------------------------------------------------------------------
    def close(self):
        self.conn.close()

    # -----------------------------------------------------------------------------------
    def runSqlFloat(self, sqlText):
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