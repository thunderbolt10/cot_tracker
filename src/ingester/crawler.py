import datetime
import zipfile
import urllib.request
import src.common.program as program
import shutil
import logging
import os
import csv
import pathlib

class Crawler():
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def download_COT_file(self, download, filename, output_folder):
        self.log.debug('url: %s filename: %s', download['url'], filename)

        data = []
        local_filepath = ''
        tmp_path = ''
        csv_file = 'temp.csv'
        try:
            download_path = download['url'] + filename
            print (pathlib.PurePath(filename).suffix)
            if pathlib.PurePath(filename).suffix == '.zip':
                local_filepath = os.path.join(output_folder, filename)
            else:
                tmp_path = os.path.join(output_folder, 'tmp')
                shutil.rmtree(tmp_path, ignore_errors=True)
                os.makedirs(tmp_path, exist_ok=True)
                local_filepath = os.path.join(tmp_path, csv_file)

            with urllib.request.urlopen(download_path) as response, open(local_filepath, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)

            
            if pathlib.PurePath(filename).suffix == '.zip':
                data = self.extract_zip(filename, output_folder)
            else:
                data = self.import_file(tmp_path, csv_file, data)
        except urllib.error.HTTPError as h:
            self.log.error('%s for %s', h, download_path)
        except Exception as e:
            self.log.exception(e)

        return data

    def extract_zip(self, filename, output_folder):
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
                    data = self.import_file(unzip_path, name, data)
        except Exception as e:
            self.log.exception(e)
        return data 
        
    def import_file(self, folder, file_name, data):
        filepath = os.path.join(folder, file_name)

        try:
            with open(filepath, mode='r') as fh:
                csv_file = csv.DictReader(fh)
                for row in csv_file:     
                    data.append(row)
        
        except Exception as e:
            self.log.exception(e)

        return data
