import pandas as pd
from parsing import resolve_participant_names
from db.database import create_handicaps


def download_handicaps(scraping_module):

    bookmaker_id = scraping_module.bookmaker_id()

    handicaps_df = pd.DataFrame(scraping_module.live_handicaps())

    handicaps_df = resolve_participant_names(handicaps_df, bookmaker_id)

    create_handicaps(handicaps_df, bookmaker_id)

    print("Загрузка данных для " + scraping_module.bookmaker_name() + " успешно завершена")
