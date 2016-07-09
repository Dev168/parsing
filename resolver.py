from sqlalchemy import create_engine
import MySQLdb as mysql
from settings import DB_HOST, DB_USER, DB_PASSWD, DB_NAME
from test1 import *
from parsing import resolve_participant_names

def resolve_sports(events_df, bookmaker_id):

    sport_names = events_df["sport"].unique().tolist()
    sportdf = get_sports_id(sport_names, bookmaker_id)

    events_df = events_df.merge(sportdf, how="left", left_on="sport", right_on="Name")

    not_founded_sports = events_df[events_df.Name.isnull()]["sport"].unique().tolist()

    events_df = events_df.drop(["sport", "Name"], 1)

    events_df = events_df.rename(columns={"Sport": "sport"})

    create_sportnames(not_founded_sports, bookmaker_id)

    return events_df


def create_sportnames(sportnames, bookmaker_id):

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')
    cursor = conn.cursor()
    params_values = [(sportname, bookmaker_id) for sportname in sportnames]

    sql_request = "INSERT INTO sportnames (`Name`, `Bookmaker`) VALUES (%s, %s)"

    cursor.executemany(sql_request, params_values)

    conn.commit()

    conn.close()


def get_sports_id(sport_names, bookmaker_id):

    sql_request = "SELECT Sport, Name FROM sportnames "\
                  "WHERE Bookmaker = %s "\
                  "AND Name IS NOT NULL "\
                  "AND Name IN %s"

    engine = create_engine('mysql://root:1234@localhost/betsdb')

    return pd.read_sql(sql_request, con=engine, params=(bookmaker_id, sport_names))


def resolve_leagues(events_df, bookmaker_id):

    league_names = events_df["league"].unique().tolist()

    leagues_id = get_leagues_id(league_names, bookmaker_id)

    events_df = events_df.merge(leagues_id, how="left", left_on="league", right_on="Name")

    # Записать на диск лиги, которых у нас нет
    not_founded_leagues = events_df[events_df.Name.isnull()][["sport", "league"]].drop_duplicates()
    not_founded_leagues["Bookmaker"] = bookmaker_id
    not_founded_leagues = not_founded_leagues.rename(columns={"sport": "Sport", "league": "Name"})

    #
    events_df = events_df.drop(["league", "Name"], 1)

    events_df = events_df.rename(columns={"League": "league"})

    create_leaguenames(not_founded_leagues)

    return events_df


def create_leaguenames(not_founded_leagues):

    engine = create_engine('mysql://root:1234@localhost/betsdb')
    not_founded_leagues.to_sql("leaguesnames", con=engine, if_exists="append", index=False)


def get_leagues_id(league_names, bookmaker_id):

    sql_request = "SELECT League, Name FROM leaguesnames "\
                  "WHERE Bookmaker = %s "\
                  "AND Name IS NOT NULL "\
                  "AND Name IN %s"

    engine = create_engine('mysql://root:1234@localhost/betsdb')

    return pd.read_sql(sql_request, con=engine, params=(bookmaker_id, league_names))


df = get_tenis_test_df()
df = resolve_sports(df, 1)
df = resolve_leagues(df, 1)
df = resolve_participant_names(df, 1)

