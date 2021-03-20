import src.common.settings as settings
import threading
import os
import logging
import logging.config
import datetime
import pathlib
import src.common.program as program
from src.ingester.ingester import Ingester
import time
import sched

class M_TimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    def __init__(self, filename):
        folder = program.get_base_dir('logs')
        os.makedirs(folder,  exist_ok=True)
        filename = os.path.join(folder, 'ingester.log')
        logging.handlers.TimedRotatingFileHandler.__init__(self, filename, when='S', interval=86400, backupCount=10, encoding=None)

class IngesterMain():
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()

    def setup_logging(self):
        try:    
            log_conf_file = program.get_base_dir('ing_logger.cfg')
            if os.path.isfile(log_conf_file):
                logging.config.fileConfig(log_conf_file)
                self.logger.disabled = False
            else:
                self.logger.error('log config file not found: %s', log_conf_file)
        except Exception as e:
            print(e)


    def run(self):
        self.logger.critical('\n')
        self.logger.critical('===========================================')
        self.logger.critical('Started COT Ingester')
        try:
            ingester = Ingester()
            ingester.run_cycle()
        except Exception as e:
            self.logger.exception(e)

        self.logger.info('SERVICE END')


if __name__ == "__main__":
    ing = IngesterMain()
    ing.run()