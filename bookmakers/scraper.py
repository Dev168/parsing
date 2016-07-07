import sys
import time
sys.path.append("C:\\Users\\Vlad\\PycharmProjects\\BookmakerPlus")
from bookmakers.sbobet import Sbobet
from bookmakers.marathonbet import Marathonbet
from download import download_handicaps

if __name__ == "__main__":

    sb = Sbobet()
    mb = Marathonbet()

    while(True):

        try:
            download_handicaps(sb)
            download_handicaps(mb)
            print("Перерыв 5 секунд")
        except KeyboardInterrupt:
            del sb
            del mb
        except Exception:
            print("Произошла ошибка")
            print("Попытка будет возобновлена через 15 секунд")
        time.sleep(5)