import MySQLdb as mysql
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWD, PROJECT_PATH
import os


def get_forks():
    with open(os.path.join(PROJECT_PATH, "forks_searching", "handicap_search.sql"), "r") as f:
        with open(os.path.join(PROJECT_PATH, "forks_searching", "handicap_search2.sql"), "r") as f2:
            sql_code1 = f.read()
            sql_code2 = f2.read()
            conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)
            cursor = conn.cursor()
            cursor.execute(sql_code1)
            conn.commit()
            cursor.execute(sql_code2)
            res = cursor.fetchall()
            conn.commit()
            cursor.execute("DROP TABLE forks")
            conn.commit()
            cursor.close()
            conn.close()

            forks = []

            for row in res:
                fork = {
                    "participant_names": row[0],
                    "event_1": row[1],
                    "event_2": row[2],
                    "coeff_1": row[3],
                    "coeff_2": row[4],
                    "marge_percent": row[5],
                    "href_1": row[6],
                    "href_2": row[7],
                    "bookmaker1": row[8],
                    "bookmaker2": row[9]
                }
                forks.append(fork)

            return forks

