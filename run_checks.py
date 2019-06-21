#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  Sergey Brazgin 05/2019
  sbrazgin@mail.ru
  Simple PostgreSql check
"""
import logging
import logging.config
import sys
import glob
import configparser

from db_connect import DbConnect
from db_check import DbCheck
from text_logger import TextLogger


# -----------------------------------------------------------------------------------
# MAIN
def main():

    # -----------------------------------------------------------------------------------
    def one_check(db_connect, check_element):
        g_logger.debug('--- one_check started: ' + check_element.desc)
        g_logger.debug('db1.version=' + str(db_connect.version) + ' check1.version=' + str(check_element.version))
        if check_element.version != DbCheck.DEFAULT_VER:
            if db_connect.version != check_element.version:
                g_logger.debug('version not equals, exit')
                return

        g_logger.debug('db1.role=' + str(db_connect.role) + ' check1.role=' + str(check_element.role))
        if check_element.role != DbConnect.DEFAULT_ROLE and check_element.role != DbCheck.DEFAULT_ROLE:
            if db_connect.role != check_element.role:
                g_logger.debug('role not equals, exit')
                return

        text_logger.add_line(' ')
        text_logger.add_line('-------------------------------------------------------')
        text_logger.add_line('-- ' + check_element.desc)
        text_logger.add_line('-------------------------------------------------------')

        str_short_result = ''
        if check_element.type == 'info':
            # print all table to out
            result_sql_value = db_connect.run_sql_table(check_element.sqlText)
            for str1 in result_sql_value:
                text_logger.add_line(str1)

        elif check_element.type == 'check_float':
            # check and print one value
            result_sql_value = db_connect.run_sql_float(check_element.sqlText)
            g_logger.debug("resultSql = " + str(result_sql_value))
            result_check_value = check_element.check_float_value(result_sql_value)

            str1 = 'Value : ' + str(result_check_value[1]) + ' ' + result_check_value[2]
            str_short_result = result_check_value[0] + ' ' + str1

            text_logger.add_line(str1)

        elif check_element.type == 'check_int':
            # check and print one value
            result_sql_value = db_connect.run_sql_int(check_element.sqlText)
            g_logger.debug("resultSql = " + str(result_sql_value))
            result_check_value = check_element.check_int_value(result_sql_value)

            str1 = 'Value : ' + str(result_check_value[1]) + ' ' + result_check_value[2]
            str_short_result = result_check_value[0] + ' ' + str1

            text_logger.add_line(str1)

        elif check_element.type == 'check_str':
            # check and print one value
            result_sql_value = db_connect.run_sql_str(check_element.sqlText)
            g_logger.debug("resultSql = " + result_sql_value)
            result_check_value = check_element.check_str_value(result_sql_value)

            str1 = 'Value : ' + str(result_check_value[1]) + ' ' + result_check_value[2]
            str_short_result = result_check_value[0] + ' ' + str1

            text_logger.add_line(str1)

        if str_short_result != '':
            text_logger2.add_line(str_short_result)

    # -----------------------------------------------------------------------------------
    # load list of database connects
    def load_db_connects():
        for file in glob.glob("db*.ini"):
            db_connect = DbConnect(file, g_logger)
            if db_connect.is_connect:
                g_list_db.append(db_connect)
            else:
                text_logger.add_line('===============================================')
                text_logger.add_line('Database: ' + db_connect.desc)
                text_logger.add_line('ERROR TO CONNECT !')
                text_logger.add_line(db_connect.error_desc)
                text_logger.add_line('===============================================')

    # -----------------------------------------------------------------------------------
    # load list of checks
    def load_db_checks():
        for file in glob.glob("check*.ini"):
            db_check = DbCheck(file, g_logger)
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
    text_logger = TextLogger(out_file, 'full', g_logger)

    out_file2 = config['REPORT']['log_file2']
    text_logger2 = TextLogger(out_file2, 'short', g_logger)

    # -------------------
    # read list of databases, connect
    g_list_db = []
    load_db_connects()

    # -------------------
    # read list of checks
    g_list_check = []
    load_db_checks()

    # -------------------
    # run checks
    i = 1
    for db1 in g_list_db:
        if i > 1:
            text_logger.add_line(' ')
            text_logger.add_line(' ')
            text_logger2.add_line(' ')

        text_logger.add_line('=====================================================================================')
        text_logger.add_line(f'== Database: {db1.desc}')
        text_logger.add_line('=====================================================================================')
        text_logger2.add_line('=====================================================================================')
        text_logger2.add_line(f'== Database: {db1.desc}')
        text_logger2.add_line('=====================================================================================')
        for check1 in g_list_check:
            one_check(db1, check1)
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
    main()

