from bookmakers.Bookmaker import GetSportPageException
from bookmakers.Sbobet import Sbobet
from time import sleep
import random
from datetime import datetime, timedelta

sb = Sbobet()


sbf = sb.get_scraping_urls()


while True:
    for f in sbf:
        try:
            sb.download_events(f)
        except GetSportPageException:
            pass
        except (IndexError, AttributeError, KeyError, sb._timeoutexception):
            timelapse = random.randint(30, 180)
            timez = (datetime.utcnow() + timedelta(hours=3)).strftime("%H:%M:%S: ")
            print(timez + "Server banned us. Waiting {0} seconds".format(timelapse))
            sleep(timelapse)

    timelapse = random.randint(1, 3)

    timez = (datetime.utcnow() + timedelta(hours=3)).strftime("%H:%M:%S: ")
    print(timez + "Delay {0} sec".format(timelapse))

    sleep(timelapse)

