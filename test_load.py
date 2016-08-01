from bookmakers.Bookmaker import GetSportPageException
from bookmakers.Sbobet import Sbobet
from bookmakers.Marathonbet import Marathonbet
from time import sleep

sb = Sbobet()


sbf = sb.get_scraping_urls()


while True:
    for f in sbf:
        try:
            sb.download_events(f)
        except (IndexError, AttributeError, KeyError, GetSportPageException, sb._timeoutexception):
            pass


    print("=========================")
    print("Delay 1 sec")
    print("=========================")
    sleep(1)

