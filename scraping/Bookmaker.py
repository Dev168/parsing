import bs4
from selenium import webdriver
from settings import PROXY
import sys
import os
from datetime import datetime
import re
import json
import linecache


class Bookmaker:

    bookmaker_id = None

    bookmaker_name = "Default"

    _live_handicaps_url = None

    def live_handicaps(self):

        page = self._get_page(self._live_handicaps_url)

        try:
            data = self._scrape_data(page)
        except(IndexError, AttributeError, Exception):
            print("При загрузке данных с сайта произошли ошибки")
            self._debug_log(page, sys.exc_info())
            return {}


        return data

    def _get_page(self, url):
        raise NotImplementedError

    def _scrape_data(self, page):
        raise NotImplementedError

    def _debug_log(self, page, info):

        dname = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        dpath = "scraping/sbobet_logs/{0}".format(dname)
        os.makedirs(dpath)

        with open(dpath+"/page.html", "w+", encoding="utf8") as f:
            f.write(page)

        game = json.dumps(info[2].tb_frame.f_locals["game"], indent=4)

        with open(dpath + "/f_locals.json", "w+", encoding="utf8") as f:
            f.write(game)

        with open(dpath + "/line_error.txt", "w+", encoding="utf8") as fl:
            exc_type, exc_obj, tb = info
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            text = 'EXCEPTION IN ({0}, LINE {1} "{2}"): {3}'.format(filename, lineno, line.strip(), exc_obj)
            fl.write(text)

        raise Exception
