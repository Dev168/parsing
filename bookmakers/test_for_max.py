import requests
from multiprocessing.dummy import Pool as ThreadPool
import time
from bookmakers.Marathonbet import Marathonbet
from bookmakers.Sbobet import Sbobet
from subprocess import Popen, PIPE
from bookmakers.Bookmaker import Bookmaker
from bookmakers.Bookmaker import GetSportPageException




list = []
list.append("sbo")
list.append("marathonbet")



def get_pages(bookmaker):


    if(bookmaker == "sbo"):

        pool = ThreadPool(5)
        s = Sbobet()
        s_pages = pool.map(s._get_page, s.get_scraping_urls())
        pool.close()
        pool.join()
        return s_pages
    else:

        pool = ThreadPool(5)
        m = Marathonbet()
        m_pages = pool.map(m._get_page, m.get_scraping_urls1())
        pool.close()
        pool.join()
        del m
        return m_pages
def get_both_pages():
    pool = ThreadPool(5)
    pages = pool.map(get_pages,list)
    pool.close()
    pool.join()
    return pages




def save_to_DB(bookmaker):
    if(bookmaker == "sbo"):

        pool = ThreadPool(5)
        s = Sbobet()
        pool.map(s.download_events_by_page, get_both_pages()[0])
        pool.close()
        pool.join()
    else:
        pool = ThreadPool(5)

        m =Marathonbet()
        pool.map(m.download_events_by_page,get_both_pages()[1])
        pool.close()
        pool.join()


def save():
    pool = ThreadPool(5)
    pool.map(save_to_DB, list)
    pool.close()
    pool.join()

t1 = time.time()
save()
t2 = time.time()

