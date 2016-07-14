from bookmakers.Marathonbet import Marathonbet
from settings import PROJECT_PATH
import os.path as path
from os import listdir

m = Marathonbet()
marathon_page_dir = path.join(PROJECT_PATH, "pages", "marathonbet")

for filename in listdir(marathon_page_dir):
    if filename.endswith(".html"):
        with open(
                path.join(marathon_page_dir, filename), encoding="utf8"
        ) as f:
            page = f.read()
            print("Начало загрузки страницы {0}".format(filename))
            m.download_events(debug_page=page)