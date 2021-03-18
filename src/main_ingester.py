import src.common.settings as settings
import threading
import os
import logging
import logging.config
import datetime
import pathlib
import src.common.program as program
from src.ingester.crawler import Crawler
from src.ingester.importer import Importer

class M_TimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    def __init__(self, filename):
        folder = program.get_base_dir('logs')
        os.makedirs(folder,  exist_ok=True)
        filename = os.path.join(folder, 'ingester.log')
        logging.handlers.TimedRotatingFileHandler.__init__(self, filename, when='S', interval=86400, backupCount=10, encoding=None)

class Ingester():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        #self.shutdown_event = threading.Event()
        self.keepalive = True
        self.settings = settings.Settings()
        self.folders={
            'zip': program.get_base_dir('store\\zip'),
            'db': program.get_base_dir('store')
        }

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

    def create_folders(self):
        for folder in self.folders:
            self.logger.info('folder %s : %s', folder, self.folders[folder])
            os.makedirs(self.folders[folder],  exist_ok=True)


    def run(self):
        self.logger.critical('\n')
        self.logger.critical('===========================================')
        self.logger.critical('Started COT Ingester')
        try:
            self.settings.load(program.get_base_dir('settings.json'))
            self.create_folders()
    
            for source_name in self.settings.config['cot source']:
                source = self.settings.config['cot source'][source_name]
                today = datetime.datetime.now()

                if source['disabled'] == 'True':
                    self.logger.warning('Skipping import for source profile: %s', source['description'])
                    continue

                # Search our zip folder for missing files by year
                for year in range(int(source['start year']), today.year + 1):
                    file_complete = False

                    filename = source['download']['file prefix'] + str(year) + source['download']['file suffix']
                    
                    fpath = pathlib.Path(os.path.join(self.folders['zip'], filename))

                    # If a file for a year is found then check the modified date is later than the year of the file
                    # to verify if the full year has been downloaded
                    if fpath.exists() and fpath.is_file():
                        mod_time = datetime.datetime.fromtimestamp(fpath.stat().st_mtime)
                        if mod_time.year > year:
                            file_complete = True
                    
                    if not file_complete:
                        crawler = Crawler()

                        # Downloading and extracting COT files
                        # Returns an array of data (the cot file contents) unfiltered
                        data = crawler.download_COT_file( source, 
                                                filename, 
                                                self.folders['zip']
                                                )
                                                
                        imp = Importer(self.folders['db'], source)        
                        imp.import_data(data)

        except Exception as e:
            self.logger.exception(e)

        self.logger.info('SERVICE END')

    def shutdown(self):
        pass

if __name__ == "__main__":
    ing = Ingester()
    ing.run()