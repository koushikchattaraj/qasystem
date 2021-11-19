import logging
from logging import *

def logs():
    
    loggingformat='{lineno} *** {name} *** {asctime} *** {message}'
    logging.basicConfig(filename='LOGS/mylogger.log', filemode='w', style='{', level=DEBUG,format=loggingformat)
    logging.debug('This is a debug message')
    logging.info('This is an info message')
    logging.warning('This is a warning message')
    logging.error('This is an error message')
    logging.critical('This is a critical message')

logs()

