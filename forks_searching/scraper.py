import sys
import time
sys.path.append("C:\\Users\\Administrator\\PycharmProjects\\BookmakerPlus")

if __name__ == "__main__":
    while(True):
        import scraping.sbobet as scraping_module
        import scraping.mar1 as scraping_module2
        from download import download_handicaps

        download_handicaps(scraping_module)
        download_handicaps(scraping_module2)
        print("Перерыв 5 секунд")
        time.sleep(5)