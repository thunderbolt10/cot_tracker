import src.common.settings as settings
import os
import logging
import datetime
import pathlib
import src.common.program as program
from src.ingester.crawler import Crawler
from src.ingester.importer import Importer

class Ingester():
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.keepalive = True
        self.settings = settings.Settings()
        self.folders={
            'zip': program.get_base_dir('store/zip'),
            'db': program.get_base_dir('store')
        }

    def create_folders(self):
        for folder in self.folders:
            self.logger.info('folder %s : %s', folder, self.folders[folder])
            os.makedirs(self.folders[folder],  exist_ok=True)


    def run_cycle(self):
        self.logger.info('\n')
        self.logger.info('===========================================')
        self.logger.info('Started COT Ingester Cycle')
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

        self.logger.info('Ended COT Ingester Cycle')
        

if __name__ == "__main__":
    ing = Ingester()
    ing.run_cycle()