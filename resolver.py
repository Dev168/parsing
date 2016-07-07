from sqlalchemy import create_engine
import pandas as pd
from bookmakers.Sbobet import Sbobet

from common.distance import distance
import db.database as db
from settings import DB_HOST, DB_USER, DB_PASSWD, DB_NAME, LIVENSHTAIN_MIN


def get():
    sb = Sbobet()
    with open("test.html", encoding="utf8") as page:
        events = sb.events(debug_page=page)
        handicaps = events["handicap"]
        return handicaps

def resolve_sports(events_df):
    df = get()


def get_sports_id(sport_names, bookmaker_id):

    sql_request =   "SELECT Name, Sport FROM sportnames "\
                    "WHERE Bookmaker = %s "\
                    "AND SPORT IS NOT NULL "\
                    "AND Name IN %s"

    engine = create_engine('mysql://root:1234@localhost/betsdb'

    return pd.read_sql(sql_request, con=engine, params=(bookmaker_id, sport_names))


