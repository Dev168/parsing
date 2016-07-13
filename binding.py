import MySQLdb as mysql
from distance import distance
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWD, LOG_DIR
from uuid import uuid4
import pandas
import logging
import os
from datetime import datetime


def _cartesian_product(df):
    df["formerge"] = 1
    result_df = df.merge(df, on="formerge")
    return result_df.drop(["formerge"], axis=1)


def _calculate_distance(row, key1, key2):
    return distance(row[key1], row[key2])


def get_duplicate(row, best_rows):
    for el in best_rows:
        if row[0] == el[0] or row[1] == el[0] or row[0] == el[1] or row[1] == el[1]:
            return el
    return None


def get_best_matching(rows: list) -> list:

    best_rows = []
    for row in rows:
        dupl = get_duplicate(row, best_rows)
        if dupl is None:
            best_rows.append(row)
        else:
            if row[2] < dupl[2]:
                best_rows.remove(dupl)
                best_rows.append(row)
    return best_rows


def match_sports():

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')

    cursor = conn.cursor()

    sql_code = 'SELECT sports.id, sports.name, sports.bookmaker ' \
               'FROM sports ' \
               'LEFT JOIN sportsmatch ' \
               'ON sports.id = sportsmatch.sport ' \
               'WHERE sportsmatch.uuid IS NULL'

    cursor.execute(sql_code)

    result = list(cursor.fetchall())

    df = pandas.DataFrame(result, columns=["id", "name", "bookmaker"])

    df2 = _cartesian_product(df)

    df3 = df2[df2.bookmaker_x != df2.bookmaker_y]

    if df3.empty:
        return

    df3["distance"] = df3.apply(_calculate_distance, axis=1, args=('name_x', 'name_y'))

    df4 = df3[df3.distance < 0.35]

    rows = [tuple(x) for x in df4[['id_x', 'id_y', 'distance', 'name_x', 'name_y']].values]

    best_rows = get_best_matching(rows)
    insert_rows = []
    for row in best_rows:
        uuid_ = uuid4().bytes.hex()
        insert_rows.append((row[0], uuid_))
        insert_rows.append((row[1], uuid_))

    best_rows_msg = "\n".join([
        row[3] + " = " + row[4] + ": distance = " + str(row[2]) for row in best_rows
    ])
    msg = "Следующие спорты будут связаны: \n" + best_rows_msg

    time = datetime.utcnow()
    logname = time.strftime("auto_bind_%d.%m.%Y.log")
    logpath = os.path.join(LOG_DIR, logname)
    logging.basicConfig(filename=logpath, level=logging.INFO, format='%(asctime)s - '
                                                                     '%(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    logger.info(msg)

    sqlcode = "INSERT into sportsmatch (`sport`, `uuid`) VALUES (%s, %s)"

    try:
        cursor.executemany(sqlcode, insert_rows)
    except:
        conn.close()
        raise
    conn.commit()

    conn.close()


def match_leagues():

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')

    cursor = conn.cursor()

    sql_code = 'SELECT leagues.id, leagues.name, leagues.bookmaker, sportsmatch.uuid as sport ' \
               'FROM leagues ' \
               'LEFT JOIN sportsmatch ' \
               'ON leagues.sport = sportsmatch.sport ' \
               'LEFT JOIN leaguesmatch ' \
               'ON leagues.id = leaguesmatch.league ' \
               'WHERE sportsmatch.uuid IS NOT NULL ' \
               'AND leaguesmatch.uuid IS NULL'

    cursor.execute(sql_code)

    result = list(cursor.fetchall())

    df = pandas.DataFrame(result, columns=["id", "name", "bookmaker", "sport"])

    df2 = _cartesian_product(df)

    df3 = df2[(df2['bookmaker_x'] != df2['bookmaker_y']) & (df2['sport_x'] == df2['sport_y'])]

    if df3.empty:
        return

    df3["distance"] = df3.apply(_calculate_distance, axis=1, args=('name_x', 'name_y'))

    df4 = df3[df3.distance < 0.35]

    rows = [tuple(x) for x in df4[['id_x', 'id_y', 'distance', 'name_x', 'name_y']].values]

    best_rows = get_best_matching(rows)
    insert_rows = []
    for row in best_rows:
        uuid_ = uuid4().bytes.hex()
        insert_rows.append((row[0], uuid_))
        insert_rows.append((row[1], uuid_))

    best_rows_msg = "\n".join([
                                  row[3] + " = " + row[4] + ": distance = " + str(row[2]) for row in best_rows
                                  ])
    msg = "Следующие лиги будут связаны: \n" + best_rows_msg

    time = datetime.utcnow()
    logname = time.strftime("auto_bind_%d.%m.%Y.log")
    logpath = os.path.join(LOG_DIR, logname)
    logging.basicConfig(filename=logpath, level=logging.INFO, format='%(asctime)s - '
                                                                     '%(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    logger.info(msg)

    sqlcode = "INSERT into leaguesmatch (`league`, `uuid`) VALUES (%s, %s)"

    try:
        cursor.executemany(sqlcode, insert_rows)
    except:
        conn.close()
        raise
    conn.commit()

    conn.close()


def match_participants():

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')

    cursor = conn.cursor()

    sql_code = 'SELECT participants.id, participants.name, participants.bookmaker, leaguesmatch.uuid as league ' \
               'FROM participants ' \
               'LEFT JOIN leaguesmatch ' \
               'ON participants.league = leaguesmatch.league ' \
               'LEFT JOIN participantsmatch ' \
               'ON participants.id = participantsmatch.participant ' \
               'WHERE leaguesmatch.uuid IS NOT NULL ' \
               'AND participantsmatch.uuid IS NULL'

    cursor.execute(sql_code)

    result = list(cursor.fetchall())

    df = pandas.DataFrame(result, columns=["id", "name", "bookmaker", "league"])

    df2 = _cartesian_product(df)

    df3 = df2[(df2['bookmaker_x'] != df2['bookmaker_y']) & (df2['league_x'] == df2['league_y'])]

    if df3.empty:
        return

    df3["distance"] = df3.apply(_calculate_distance, axis=1, args=('name_x', 'name_y'))

    df4 = df3[df3.distance < 0.35]

    rows = [tuple(x) for x in df4[['id_x', 'id_y', 'distance', 'name_x', 'name_y']].values]

    best_rows = get_best_matching(rows)
    insert_rows = []
    for row in best_rows:
        uuid_ = uuid4().bytes.hex()
        insert_rows.append((row[0], uuid_))
        insert_rows.append((row[1], uuid_))

    best_rows_msg = "\n".join([
                                  row[3] + " = " + row[4] + ": distance = " + str(row[2]) for row in best_rows
                                  ])
    msg = "Следующие участники будут связаны: \n" + best_rows_msg

    time = datetime.utcnow()
    logname = time.strftime("auto_bind_%d.%m.%Y.log")
    logpath = os.path.join(LOG_DIR, logname)
    logging.basicConfig(filename=logpath, level=logging.INFO, format='%(asctime)s - '
                                                                     '%(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    logger.info(msg)

    sqlcode = "INSERT into participantsmatch (`participant`, `uuid`) VALUES (%s, %s)"

    try:
        cursor.executemany(sqlcode, insert_rows)
    except:
        conn.close()
        raise
    conn.commit()

    conn.close()


match_sports()


match_leagues()


match_participants()




















