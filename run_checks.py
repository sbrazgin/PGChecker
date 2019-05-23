'''
  Sergey Brazgin 05/2019
  sbrazgin@mail.ru
  Simple PostgreSql check
'''
import logging
import logging.config
import sys
import glob
import configparser

from db_connect import DBconnect
from db_check import DBcheck
from text_logger import textLogger


# -----------------------------------------------------------------------------------
# MAIN proc
def main(argv):
    global g_logger
    global g_list_db
    global g_list_check
    global text_logger
    global text_logger2

    # -----------------------------------------------------------------------------------
    def one_check(db1, check1):
        global g_logger
        g_logger.debug('--- one_check started: '+ check1.desc)
        g_logger.debug('db1.version='+str(db1.version)+' check1.version='+str(check1.version))
        if check1.version > 0:
            if db1.version != check1.version:
                g_logger.debug('version not equals, exit')
                return
        g_logger.debug('db1.role='+str(db1.role)+' check1.role='+str(check1.role))
        if check1.role != DBconnect.DEFAULT_ROLE and check1.role != DBcheck.DEFAULT_ROLE:
            if db1.role != check1.role:
                g_logger.debug('role not equals, exit')
                return

        text_logger.add_line(' ')
        text_logger.add_line('-------------------------------------------------------' )
        text_logger.add_line('-- ' + check1.desc)
        text_logger.add_line('-------------------------------------------------------' )

        str_short_result = ''
        if check1.type == 'info':
            # print all table to out
            result_sql_value = db1.runSqlTable(check1.sqlText)
            for str1 in result_sql_value:
                text_logger.add_line(str1)


        if check1.type == 'check_float':
            # check and print one value
            result_sql_value = db1.runSqlFloat(check1.sqlText)
            g_logger.debug("resultSql = " + str(result_sql_value))
            result_check_value = check1.checkFloatValue(result_sql_value)

            #str1 = 'Check: "'+result_check_value[0] +'" Result:'+ str(result_check_value[1]) +' '+ result_check_value[2]
            str1 = 'Value : '+ str(result_check_value[1]) +' '+ result_check_value[2]
            str_short_result = result_check_value[0] +' '+ str1

            text_logger.add_line(str1)

        if check1.type == 'check_int':
            # check and print one value
            result_sql_value = db1.runSqlInt(check1.sqlText)
            g_logger.debug("resultSql = " + str(result_sql_value))
            result_check_value = check1.checkIntValue(result_sql_value)

            #str1 = 'Check: "'+result_check_value[0] +'" Result:'+ str(result_check_value[1]) +' '+ result_check_value[2]
            str1 = 'Value : '+ str(result_check_value[1]) +' '+ result_check_value[2]
            str_short_result = result_check_value[0] +' '+ str1

            text_logger.add_line(str1)

        if check1.type == 'check_str':
            # check and print one value
            result_sql_value = db1.runSqlStr(check1.sqlText)
            g_logger.debug("resultSql = " + result_sql_value)
            result_check_value = check1.checkStrValue(result_sql_value)

            str1 = 'Value : '+ str(result_check_value[1]) +' '+ result_check_value[2]
            str_short_result = result_check_value[0] +' '+ str1

            text_logger.add_line(str1)

        if str_short_result != '':
            text_logger2.add_line(str_short_result)


    # -----------------------------------------------------------------------------------
    # load list of database connects
    def load_db_connects():
        global g_list_db
        g_list_db = []

        for file in glob.glob("db*.ini"):
            g_logger.debug('db ini file = ' + file)

            db_connect = DBconnect(file, g_logger)
            db_connect.connect()
            if db_connect.is_connect():
                g_list_db.append(db_connect)
            else:
                text_logger.add_line('=====================================================================================')
                text_logger.add_line('Database: ' + db_connect.getDescDatabase())
                text_logger.add_line('ERROR TO CONNECT !');
                text_logger.add_line(db_connect.getError());
                text_logger.add_line('=====================================================================================')

    # -----------------------------------------------------------------------------------
    # load list of checks
    def load_db_checks():
        global g_list_check
        g_list_check = []

        for file in glob.glob("check*.ini"):
            g_logger.debug('check ini file = ' + file)

            db_check = DBcheck(file, g_logger)
            g_list_check.append(db_check)

    # ================= MAIN ================
    # -------------------
    # create logger
    logging.config.fileConfig('logging.conf')
    g_logger = logging.getLogger()
    g_logger.info('Started')

    # -------------------
    # read input params
    config = configparser.ConfigParser()
    config.read('config.ini')
    out_file = config['REPORT']['log_file']
    text_logger = textLogger(out_file,'full', g_logger)

    out_file2 = config['REPORT']['log_file2']
    text_logger2 = textLogger(out_file2,'short',g_logger)

    # -------------------
    # read list of databases, connect
    load_db_connects()

    # -------------------
    # read list of checks
    load_db_checks()

    # -------------------
    # run checks
    i = 1
    for db1 in g_list_db:
        if i > 1:
            text_logger.add_line(' ');
            text_logger.add_line(' ');
            text_logger2.add_line(' ');

        text_logger.add_line('=====================================================================================')
        text_logger.add_line(f'== Database: {db1.getDescDatabase()}')
        text_logger.add_line('=====================================================================================')
        text_logger2.add_line('=====================================================================================')
        text_logger2.add_line(f'== Database: {db1.getDescDatabase()}')
        text_logger2.add_line('=====================================================================================')
        for check1 in g_list_check:
            one_check(db1,check1)
        i = i + 1

    # -------------------
    # close connections
    for db1 in g_list_db:
        db1.close()

    # -------------------
    text_logger.close()

# -----------------------------------------------------------------------------------
if __name__ == "__main__":
    print(sys.argv)
    main(sys.argv[1:])

