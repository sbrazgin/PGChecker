class textLogger(object):

    # -----------------------------------------------------------------------------------
    def __init__(self, out_file, logger):
        self.out_file = out_file
        self.logger = logger

        self.logger.info('out_file = ' + self.out_file)
        self.g_out_text_file = open(self.out_file, "w")

    def add_line(self,line):
        self.logger.debug("WRITE TO OUT LOG: "+line)
        self.g_out_text_file.write(line+"\r")

    def close(self):
        self.g_out_text_file.close()