from bookmakers.Bookmaker import GetSportPageException
from bookmakers.Sbobet import Sbobet
from bookmakers.Marathonbet import Marathonbet
from time import sleep

m = Marathonbet()
mf = m.get_scraping_urls()

while True:

    for f in mf:
        try:
            m.download_events(f)
        except (IndexError, AttributeError, KeyError, GetSportPageException, m._timeoutexception):
            pass

    print("=========================")
    print("Delay 1 sec")
    print("=========================")
    sleep(1)

