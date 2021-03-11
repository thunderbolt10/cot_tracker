# cot_tracker
Commitments of Traders data tracker

This is a package written for python v3.


## Startup
### Setting up python first time
If you are new to python, it can be downloaded from [python.org](https://python.org/downloads).

### Installing required Python packages
In the package source you will find requirements.txt. These files contain a list of python packages that this project has dependencies on. The requirments.txt is used with the python command line program pip.
To use, goto your open your system Terminal/Command Prompt and type 
```
pip install -r requirements.txt
```


## Cot Ingester

This module is responsible for pulling down raw data files, processing, and storing the data.
It is designed to work with files downloaded from cftc.gov.
SQlite is used for persistant data storage.