import os
from datetime import datetime, timedelta
from bookmakers.Bookmaker import GetSportPageException
from bookmakers.Sbobet import Sbobet
from bookmakers.Marathonbet import Marathonbet
from time import sleep
import logging

from settings import PROJECT_PATH

sb = Sbobet()
m = Marathonbet()

sbf = sb.get_scraping_urls()
mf = m.get_scraping_urls()
logpath = os.path.join(PROJECT_PATH, "pages", "log.txt")
logging.basicConfig(filename=logpath, level=logging.INFO, format='%(asctime)s - %(threadName)s - '
                                                                 '%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

mardir = os.path.join(PROJECT_PATH, "pages", "marathonbet")
sbodir = os.path.join(PROJECT_PATH, "pages", "sbobet")

while True:
    for url in sbf:


        try:
            logger.info("{0}: Начало загрузки страницы {1} с сайта".format(sb.bookmaker_name, url))
            page = sb._get_page(url)
            time = datetime.utcnow() + timedelta(hours=3)
            with open(os.path.join(sbodir, time.strftime("%Y-%m-%d_%H-%M-%f.html")), "w", encoding="utf8") as f:
                f.write(page)

        except sb._timeoutexception:
            sb._debug_timeout_exception()

        except GetSportPageException:
            logger.error("{0}: Невозможно получить страницу".format(sb.bookmaker_name))

    for url in mf:
        try:
            logger.info("{0}: Начало загрузки страницы {1} с сайта".format(m.bookmaker_name, url))
            page = m._get_page(url)
            time = datetime.utcnow() + timedelta(hours=3)
            with open(os.path.join(mardir, time.strftime("%Y-%m-%d_%H-%M-%f.html")), "w", encoding="utf8") as f:
                f.write(page)

        except m._timeoutexception:
            m._debug_timeout_exception()

        except GetSportPageException:
            logger.error("{0}: Невозможно получить страницу".format(m.bookmaker_name))


    print("Delay 1800 sec")
    sleep(1800)