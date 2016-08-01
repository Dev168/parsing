import logging
import os
from datetime import datetime, timedelta
from settings import LOG_DIR

logger = None

def get_logger(name, suff):

    global logger

    if logger is not None:
        return logger

    time = datetime.utcnow() + timedelta(hours=3)
    logname = time.strftime("{0}%d.%m.%Y.log".format(suff))
    logpath = os.path.join(LOG_DIR, logname)

    handler = logging.FileHandler(logpath, "a",
                                  encoding="UTF-8")
    formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger