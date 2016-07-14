from bookmakers.Sbobet import Sbobet
from settings import PROJECT_PATH
import os.path as path
from os import listdir

sb = Sbobet()
sbobet_page_dir = path.join(PROJECT_PATH, "pages", "sbobet")

for filename in listdir(sbobet_page_dir):
    if filename.endswith(".html"):
        with open(
                path.join(sbobet_page_dir, filename), encoding="utf8"
        ) as f:
            page = f.read()
            print("Начало загрузки страницы {0}".format(filename))
            sb.download_events(debug_page=page)