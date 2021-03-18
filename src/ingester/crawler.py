import datetime
import zipfile
import urllib.request
import src.common.program as program
import shutil
import logging
import os
import csv

class Crawler():
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def download_COT_file(self, source, filename, output_folder):
        self.log.debug('url: %s filename: %s', source['download']['url'], filename)

        data = []
        try:
            download_path = source['download']['url'] + '/' + filename
            local_filepath = os.path.join(output_folder, filename)

            with urllib.request.urlopen(download_path) as response, open(local_filepath, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)

            data = self.extract_zip(source, filename, output_folder)
        except Exception as e:
            self.log.exception(e)

        return data

    def extract_zip(self, source, filename, output_folder):
        z_file  = os.path.join(output_folder, filename)
        unzip_path = os.path.join(output_folder, 'tmp')
        shutil.rmtree(unzip_path, ignore_errors=True)
        os.makedirs(unzip_path, exist_ok=True)
        data = []
        try:
            with zipfile.ZipFile(z_file) as zf:
                archive_files = zf.namelist()
                for name in archive_files:
                    zf.extract(name, unzip_path)
                    data = self.import_file(source, unzip_path, name, data)
        except Exception as e:
            self.log.exception(e)
        return data 
        
    def import_file(self, source, folder, file_name, data):
        filepath = os.path.join(folder, file_name)

        try:
            
            with open(filepath, mode='r') as fh:
                csv_file = csv.DictReader(fh)
                for row in csv_file:     
                    data.append(row)
        
        except Exception as e:
            self.log.exception(e)

        return data
