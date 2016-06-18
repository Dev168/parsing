import pandas as pd
from parsing import resolve_participant_names
from db.database import create_handicaps


def download_handicaps(scraping_module):

    handicaps_df = pd.DataFrame(scraping_module.events()["handicap"])

    handicaps_df = resolve_participant_names(handicaps_df, scraping_module.bookmaker_id())

    create_handicaps(handicaps_df)