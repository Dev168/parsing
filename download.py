import pandas as pd
from parsing import resolve_participant_names
from db.database import create_handicaps


def download_handicaps(scraping_module):

    bookmaker_name = scraping_module.bookmaker_name()

    bookmaker_id = scraping_module.bookmaker_id()

    print(bookmaker_name + ": Начата загрузка данных с сайта")

    handicaps_df = pd.DataFrame(scraping_module.live_handicaps())

    print(bookmaker_name + ": Данные успешно загружены с сайта")

    handicaps_df = resolve_participant_names(handicaps_df, bookmaker_id)

    create_handicaps(handicaps_df, bookmaker_id)

    print(bookmaker_name + ": Работа успешно завершена")
