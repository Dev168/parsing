import scraping.sbobet as scraping_module
import scraping.mar1 as scraping_module2
from download import download_handicaps

download_handicaps(scraping_module)
download_handicaps(scraping_module2)