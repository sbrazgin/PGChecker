'''
  Sergey Brazgin 05/2019
  sbrazgin@mail.ru
  Simple PostgreSql check
'''
import logging
import logging.config
import sys
from db_connect import DBconnect
from db_check import DBcheck

def one_check(db1,check1):
    resultSql = db1.runSql(check1.sqlText)
    logger.debug("resultSql="+str(resultSql))
    check1.checkValue(resultSql)

# -----------------------------------------------------------------------------------
# MAIN proc
def main(argv):
    global logger

    # -------------------
    # create logger
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger()
    logger.info('Started')

    # -------------------
    # read input params

    # -------------------
    list_db = []
    db_connect = DBconnect('db_1.ini',logger)
    db_connect.connect()
    list_db.append(db_connect)


    # -------------------
    list_check = []
    db_check = DBcheck('check_1.ini',logger)
    list_check.append(db_check)

    # -------------------
    for db1 in list_db:
        for check1 in list_check:
            one_check(db1,check1)

    # -------------------
    for db1 in list_db:
        db1.close()

if __name__ == "__main__":
    print(sys.argv)
    main(sys.argv[1:])

