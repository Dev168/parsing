import sys
import time
sys.path.append("C:\\Users\\Administrator\\PycharmProjects\\BookmakerPlus")
from bookmakers.Sbobet import Sbobet
from bookmakers.Marathonbet import Marathonbet
from download import download_handicaps

if __name__ == "__main__":

    sb = Sbobet()
    mb = Marathonbet()

    while(True):

        try:
            download_handicaps(sb)
            download_handicaps(mb)
            print("Перерыв 15 секунд")
        except Exception:
            print("Попытка будет возобновлена через 15 секунд")
        time.sleep(15)