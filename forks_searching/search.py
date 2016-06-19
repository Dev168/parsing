import pandas as pd
import MySQLdb as mysql
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWD


def get_forks():
    with open("forks_searching\handicap_search.sql", "r") as f:
        sql_code = f.read()
        conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)
        df = pd.read_sql(sql_code, con=conn)
        conn.close()

