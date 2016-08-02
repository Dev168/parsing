from bookmakers.Bookmaker import GetSportPageException
from bookmakers.Marathonbet import Marathonbet
from time import sleep
import random
from datetime import datetime, timedelta

m = Marathonbet()
mf = m.get_scraping_urls()

while True:

    for f in mf:
        try:
            m.download_events(f)
        except GetSportPageException:
            pass
        except (IndexError, AttributeError, KeyError, m._timeoutexception):
            timelapse = random.randint(30, 180)
            timez = (datetime.utcnow() + timedelta(hours=3)).strftime("%H:%M:%S: ")
            print(timez + "Сервер забанил нас. Сделаем паузу {0} секунд".format(timelapse))
            sleep(timelapse)

    timelapse = random.randint(1, 3)
    timez = (datetime.utcnow() + timedelta(hours=3)).strftime("%H:%M:%S: ")
    print(timez + "Delay {0} sec".format(timelapse))
    sleep(timelapse)

