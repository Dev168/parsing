import pandas as pd
from parsing import resolve_participant_names
from db.database import create_handicaps


def download_handicaps(scraping_module):

    handicaps_df = pd.DataFrame(scraping_module.events()["handicap"])

    handicaps_df = resolve_participant_names(handicaps_df)

    create_handicaps(handicaps_df)