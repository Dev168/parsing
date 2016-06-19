import pandas as pd
import MySQLdb as mysql
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWD, PROJECT_PATH
import os


def get_forks():
    with open(os.path.join(PROJECT_PATH, "forks_searching\handicap_search.sql"), "r") as f:
        sql_code = f.read()
        conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)
        df = pd.read_sql(sql_code, con=conn)
        conn.close()
        return [
            {"participant_names": "Rus-England",
             "event_1": "handicap Rus +2",
             "event_2": "handicap Eng -2",
             "coeff_1": "2",
             "coeff_2": "3",
             "marge_percent": "10%",
             "href_1": "раз",
             "href_2": "два",
             "bookmaker1": "sbobet",
             "bookmaker2": "marathon"
            }
                ]

