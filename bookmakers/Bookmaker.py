import sys
import os
from datetime import datetime, timedelta
from abc import abstractmethod, ABCMeta
from settings import LOG_DIR, LOAD_WAIT_TIME


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

    _default_url = "https://www.sbobet.com/euro/football"

    @abstractmethod
    def _get_page(self, url):
        pass

    @abstractmethod
    def _scrape_page(self, page):
        pass

    def events(self, url=None, debug_page=None):

        if url is None:
            url = self._default_url

        try:

            if debug_page is None:
                page = self._get_page(url)
            else:
                page = debug_page

        except self._timeoutexception:
            self._debug_timeout_exception()
            raise

        try:

            return self._scrape_page(page)

        except (IndexError, AttributeError, Exception):
            self._debug_scraping_error(page, sys.exc_info())
            raise

    def live_handicaps(self, url=None):
        try:
            return self.events(url)["handicap"]
        except self._timeoutexception:
            raise

    def _debug_scraping_error(self, page):

        time = datetime.utcnow() + timedelta(hours=3)

        dname = time.strftime("%Y-%m-%d_%H-%M-%S") + " scrap error"
        dpath = os.path.join(self.bookmaker_log_dir, dname)

        os.makedirs(dpath)

        with open(dpath + "/page.html", "w+", encoding="utf8") as f:
            f.write(page)

        with open(dpath + "/info.txt", "w+", encoding="utf8") as f:
            f.write("Произошла ошибка парсинга")

    def _debug_timeout_exception(self):

        time = datetime.utcnow() + timedelta(hours=3)

        dname = time.strftime("%Y-%m-%d_%H-%M-%S") + " load page error"
        dpath = os.path.join(self.bookmaker_log_dir, dname)

        os.makedirs(dpath)

        with open(dpath + "/info.txt", "w+", encoding="utf8") as f:
            f.write("Превышен таймаут соединения")
