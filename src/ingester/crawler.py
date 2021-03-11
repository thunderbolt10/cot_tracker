import datetime
import zipfile
import urllib.request
import program as program
import shutil

def download_COT_file(url, file_name):
    print('url: ', url)
    print('filename: ', file_name)
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
        
def read_cot_zip(zip_file):
    with zipfile.ZipFile(zip_file) as zf:
        archive_files = zf.namelist()
        for name in archive_files:
            with zf.open(name) as fh:
                for line in fh.readlines():
                    print(line)



# Downloading and extracting COT files
today = datetime.datetime.now()
year = today.year
base_url = 'https://www.cftc.gov/files/dea/history/'
filename = 'fut_disagg_txt_' + str(year) + '.zip'
download_path = base_url + '/' + filename

temp_file = program.get_base_dir('temp.zip')
download_COT_file(download_path, temp_file)
read_cot_zip(temp_file)