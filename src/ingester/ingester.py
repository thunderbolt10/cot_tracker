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

                for download in source['download']:
                    if download['type'] == "cot":
                        self.download_cot_data(source, download, int(source['start year']), today.year + 1)
                    elif download['type'] == 'com price':
                        self.download_cot_price(source, download, int(source['start year']), today)

        except Exception as e:
                self.logger.exception(e)

        self.logger.info('Ended COT Ingester Cycle')
        
    def download_cot_data(self, source, download, start_year, end_year):
        try:
            # Search our zip folder for missing files by year
            for year in range(start_year, end_year):
                file_complete = False

                filename = download['file prefix'] + str(year) + download['file suffix']
                
                fpath = pathlib.Path(os.path.join(self.folders['zip'], filename))

                # If a file for a year is found then check the modified date is later than the year of the file
                # to verify if the full year has been downloaded
                if fpath.exists() and fpath.is_file():
                    mod_time = datetime.datetime.fromtimestamp(fpath.stat().st_mtime)
                    if mod_time.year > year:
                        file_complete = True
                
                if not file_complete:
                    crawler = Crawler(None)

                    # Downloading and extracting COT files
                    # Returns an array of data (the cot file contents) unfiltered
                    data = crawler.download_COT_file( download, 
                                            filename, 
                                            self.folders['zip']
                                            )
                                            
                    imp = Importer(self.folders['db'], source)        
                    imp.import_cot_data(data)

        except Exception as e:
            self.logger.exception(e)


    def unix_time_seconds(self, dt):
        epoch = datetime.datetime.utcfromtimestamp(0)
        return (dt - epoch).total_seconds()

    def download_cot_price(self, source, download, start_year, today):
        try:
            api_key = None

            if 'quandl api key' in self.settings.config:
                api_key = self.settings.config['quandl api key']

            crawler = Crawler(api_key)

            for item in source['items']:
                imp = Importer(self.folders['db'], source) 
                last_year = imp.get_year_of_last_price(item)
                if last_year is None:
                    last_year = start_year       
                start_date = datetime.datetime(last_year, 1, 1, 0, 0, 0, 0)
                end_date = today.replace(hour=0, minute=0, second=0)
                if 'quandl price code' in item:
                    data = crawler.download_quandl_price(
                                item['quandl price code'], 
                                start_date.strftime('%Y-%m-%d'), 
                                end_date.strftime('%Y-%m-%d'))
                else:

                    start_period = self.unix_time_seconds(start_date)
                    end_period = self.unix_time_seconds(end_date)
                    #start_period = 963792000
                    #end_period = 1616371200
                    filename = '%s=F?period1=%d&period2=%d&%s' % \
                                (item['symbol'], \
                                    start_period, end_period, download['file suffix'])

                    # Downloading and extracting COT files
                    # Returns an array of data (the cot file contents) unfiltered
                    data = crawler.download_COT_file( download, 
                                            filename, 
                                            self.folders['zip']
                                            )
                                            
                imp.import_commodity_price(item, data)

        except Exception as e:
            self.logger.exception(e)

        

if __name__ == "__main__":
    ing = Ingester()
    ing.run_cycle()