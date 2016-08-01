from bookmakers.Bookmaker import GetSportPageException
from bookmakers.Sbobet import Sbobet
from bookmakers.Marathonbet import Marathonbet
from time import sleep

sb = Sbobet()
m = Marathonbet()

sbf = sb.get_scraping_urls()
mf = m.get_scraping_urls()

while True:
    for f in sbf:
        try:
            sb.download_events(f)
        except (IndexError, AttributeError, KeyError, GetSportPageException, sb._timeoutexception):
            pass

    for f in mf:
        try:
            m.download_events(f)
        except (IndexError, AttributeError, KeyError, GetSportPageException, m._timeoutexception):
            pass

    print("=========================")
    print("Delay 2 sec")
    print("=========================")
    sleep(1)

