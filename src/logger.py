# Logger.py ise used for :- 1.) Debugging of errors
                          #  2.) Progress Tracking
                         #   3.) RealTime monitoring

import logging
import os
from datetime import datetime

LOGS_DIR = 'logs'
os.makedirs(LOGS_DIR , exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR , f"log_{datetime.now().strftime('%Y-%m-%d')}.log") # Isse current date time ki file ban jaegi..... ex - 2024-02-14.log

logging.basicConfig(
    filename=LOG_FILE, # filename LOG_FILE se connect kardega
    format = "%(asctime)s - %(levelname)s - %(message)s", 
    level = logging.INFO # only error and warning will be logged according to heirarchy

)

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
