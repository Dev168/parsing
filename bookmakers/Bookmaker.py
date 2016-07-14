import os
from datetime import datetime, timedelta
from abc import abstractmethod, ABCMeta
from settings import LOG_DIR
from db.database import create_handicaps, create_moneylines
from new_resolver import resolve_all_links
import traceback
import logging


class GetSportPageException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class Bookmaker(object):

    __metaclass__ = ABCMeta

    def __init__(self):

        bookmaker_log_dir = os.path.join(LOG_DIR, self.bookmaker_name)

        self.bookmaker_log_dir = bookmaker_log_dir

        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)

        if not os.path.exists(bookmaker_log_dir):
            os.makedirs(bookmaker_log_dir)

    bookmaker_id = 999

    bookmaker_name = "Default"

    bookmaker_log_dir = None

    _timeoutexception = Exception

    @abstractmethod
    def _get_page(self, url):
        pass

    @abstractmethod
    def _scrape_page(self, page):
        pass

    @abstractmethod
    def get_scraping_urls(self):
        pass

    def events(self, url=None, debug_page=None):

        logger = logging.getLogger(__name__)

        try:
            if debug_page is None:
                logger.info("{0}: Начало загрузки страницы {1} с сайта".format(self.bookmaker_name, url))
                page = self._get_page(url)
            else:
                logger.info("{0}: Работа будет произведена с отладочной страницей".format(self.bookmaker_name))
                page = debug_page

        except self._timeoutexception:
            self._debug_timeout_exception()
            raise

        except GetSportPageException:
            logger.error("{0}: Невозможно получить страницу".format(self.bookmaker_name))
            raise

        try:
            logger.info("{0}: Начало парсинга страницы".format(self.bookmaker_name))
            result = self._scrape_page(page)

        except (IndexError, AttributeError, Exception):
            self._debug_scraping_error(page)
            raise

        return result

    def _debug_scraping_error(self, page):

        logger = logging.getLogger(__name__)

        time = datetime.utcnow() + timedelta(hours=3)

        dname = time.strftime("%Y-%m-%d_%H-%M-%S") + " scrap error"
        dpath = os.path.join(self.bookmaker_log_dir, dname)

        os.makedirs(dpath)

        error_msg = "{0}: Ошибки при парсинге страницы\n".format(self.bookmaker_name)
        error_msg += traceback.format_exc()
        logger.error(error_msg)

        with open(dpath + "/page.html", "w+", encoding="utf8") as f:
            f.write(page)

        with open(dpath + "/info.txt", "w+", encoding="utf8") as f:
            f.write(traceback.format_exc())

        raise

    def _debug_timeout_exception(self):

        logger = logging.getLogger(__name__)

        time = datetime.utcnow() + timedelta(hours=3)

        dname = time.strftime("%Y-%m-%d_%H-%M-%S") + " load page error"
        dpath = os.path.join(self.bookmaker_log_dir, dname)

        os.makedirs(dpath)

        error_msg = "{0}: Превышен таймаут соединения\n".format(self.bookmaker_name)
        error_msg += traceback.format_exc()
        logger.error(error_msg)

        with open(dpath + "/info.txt", "w+", encoding="utf8") as f:
            f.write("Превышен таймаут соединения")

    def download_events(self, scraping_url=None, debug_page=None):

        time = datetime.utcnow()
        logname = time.strftime("%d.%m.%Y.log")
        logpath = os.path.join(LOG_DIR, logname)
        logging.basicConfig(filename=logpath, level=logging.INFO, format='%(asctime)s - %(threadName)s - '
                                                                          '%(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)

        bookmaker_name = self.bookmaker_name
        logger.info("{0}: Начало загрузки данных".format(bookmaker_name))

        try:
            events = self.events(scraping_url, debug_page)
            logger.info("{0}: События успешно получены".format(bookmaker_name))
        except:
            logger.error("{0}: Не удалось получить события".format(bookmaker_name))
            raise

        # Костыли, TODO: убрать!!!
        handicaps = events["handicap"]
        moneylines = events["moneyline"]

        for h in handicaps:
            h["bookmaker"] = self.bookmaker_id
            h["oddsdate"] = datetime.utcnow()
            h["actual"] = True

        for m in moneylines:
            m["bookmaker"] = self.bookmaker_id
            m["oddsdate"] = datetime.utcnow()
            m["actual"] = True
        # Костыли, конец

        if len(handicaps) > 0:
            logger.info("{0}: Начало разрешения ссылок в гандикапах".format(bookmaker_name))
            handicaps = resolve_all_links(handicaps)
            create_handicaps(handicaps)
        else:
            logger.info("{0}: Гандикапы на странице {1} отсутствуют".format(bookmaker_name, scraping_url))

        if len(moneylines) > 0:
            logger.info("{0}: Начало разрешения ссылок в манилайнах".format(bookmaker_name))
            moneylines = resolve_all_links(moneylines)
            create_moneylines(moneylines)
        else:
            logger.info("{0}: Манилайны на странице {1} отсутствуют".format(bookmaker_name, scraping_url))

        logger.info("{0}: Загрузка со страницы {1} завершена".format(bookmaker_name, scraping_url))


