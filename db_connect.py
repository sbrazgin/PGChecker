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
        self.error_desc = ""


    # -----------------------------------------------------------------------------------
    def getDescDatabase(self):
        return "hostName="+self.hostName+", "+"portNumber="+self.portNumber+", database="+self.database

    def getDescDatabase2(self):
        return self.getDescDatabase() + ', user='+self.username+', password='+self.password

    def getError(self):
        return self.error_desc

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
            self.error_desc = str(e)
            self.logger.error(self.error_desc)
            self.logger.error('Params to connect: ' + self.getDescDatabase2())
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

    def runSqlTable(self, sqlText):
        cursor = self.conn.cursor()

        cursor.execute(sqlText)
        records = cursor.fetchall()
        result = []
        for row in records:
            str1=str(row[0])
            result.append( str1 )
            self.logger.debug("result next string="+str1)

        cursor.close()
        return result
