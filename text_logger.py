#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  Sergey Brazgin 05/2019
  sbrazgin@mail.ru
  Simple PostgreSql check
"""


class TextLogger(object):

    # -----------------------------------------------------------------------------------
    def __init__(self, out_file: str, name: str, logger):
        self.out_file = out_file
        self.logger = logger
        self._name = name

        self.logger.info(f'TEXT_SAVE [{self._name}] started, out_file = {self.out_file}')
        self.g_out_text_file = open(self.out_file, "w")

    # -----------------------------------------------------------------------------------
    def add_line(self, line: str):
        self.logger.debug(f"WRITE TO OUT LOG [{self._name}] : {line}")
        self.g_out_text_file.write(line+"\r")

    # -----------------------------------------------------------------------------------
    def close(self):
        self.g_out_text_file.close()
