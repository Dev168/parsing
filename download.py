import pandas as pd
from parsing import resolve_participant_names
from db.database import create_handicaps


def download_handicaps(bookmaker):

    bookmaker_name = bookmaker.bookmaker_name

    bookmaker_id = bookmaker.bookmaker_id

    print(bookmaker_name + ": Начата загрузка данных с сайта")

    try:
        handicaps_df = pd.DataFrame(bookmaker.live_handicaps())
    except Exception:
        print("Произошли ошибки при парсинге данных")
        raise

    print(bookmaker_name + ": Данные успешно загружены с сайта")

    handicaps_df = resolve_sports(handicaps_df, bookmaker_id)

    handicaps_df = resolve_participant_names(handicaps_df, bookmaker_id)

    create_handicaps(handicaps_df, bookmaker_id)

    print(bookmaker_name + ": Работа успешно завершена")
