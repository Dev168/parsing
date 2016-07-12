import json
import os
import MySQLdb as mysql
import logging
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWD

DIRNAME = os.path.dirname(os.path.abspath("__file__"))


def init():
    """Инициализирует базу данных со всеми необходимыми таблицами
    Если база данных с именем DB_NAME уже существует то будет ошибка"""

    def __load_init_bookmakers():
        with open(os.path.join(DIRNAME, "bookmakers_create.json")) as f:
            text = f.read()
            return json.loads(text)

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD)

    cursor = conn.cursor()

    sql_code = "CREATE DATABASE IF NOT EXISTS {0}".format(DB_NAME)

    cursor.execute(sql_code)

    cursor.close()

    conn.close()

    print("База данных успешно создана")

    with open(os.path.join(DIRNAME, "mysql_create.sql"), "r") as f:
        sql_init_code = f.read()

        conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

        cursor = conn.cursor()

        cursor.execute(sql_init_code)

        cursor.close()

        conn.close()

        print("Таблицы успешно созданы")

    create_bookmakers(__load_init_bookmakers())


def get_bookmakers():
    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    cursor = conn.cursor()

    sql_code = "SELECT * FROM bookmakers"

    cursor.execute(sql_code)

    res = cursor.fetchall()

    cursor.close()

    conn.close()

    return res


def create_bookmakers(bookmakers):

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    cursor = conn.cursor()

    sql_code = "INSERT INTO bookmakers (`id`, `Name`, `hostname`) VALUES (%s, %s, %s)"

    cursor.executemany(sql_code, [(bookmaker[0], bookmaker[1], bookmaker[2]) for bookmaker in bookmakers])

    conn.commit()

    conn.close()

    print("Добавлены букмекеры")


def create_sports(sports):
    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    cursor = conn.cursor()

    sql_code = "INSERT INTO sports (`Name`) VALUES (%s)"

    cursor.executemany(sql_code, [(sport,) for sport in sports])

    conn.commit()

    conn.close()

    print("Добавлены новые виды спорта")


def create_handicaps(handicaps):

    logger = logging.getLogger(__name__)
    delete_previous("handicaps", handicaps[0]["bookmaker"], handicaps[0]["sport"])
    logger.info("Из базы данных удалены все гандикапы по конторе {0} и спорту {1}".
                format(handicaps[0]["bookmaker"], handicaps[0]["sport"]))

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')

    cursor = conn.cursor()

    sql_code = 'INSERT INTO handicaps ' \
               '(`firstforward`, `firstwin`, `secondforward`, `secondwin`,' \
               ' `oddsdate`, `live`, `href`, `firstparticipant`, `secondparticipant`,' \
               ' `bookmaker`, `actual`, `sport`, `league`)' \
               ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    params = []

    for h in handicaps:
        params.append(
            (h["firstforward"], h["firstwin"], h["secondforward"], h["secondwin"],
             h["oddsdate"], h["live"], h["href"], h["firstparticipant"], h["secondparticipant"],
             h["bookmaker"], h["actual"], h["sport"], h["league"])
        )

    cursor.executemany(sql_code, params)

    conn.commit()

    logger.info("Добавлено {0} гандикапов".format(len(handicaps)))

    conn.close()


def delete_previous(table, bookmaker, sport):

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')

    cursor = conn.cursor()

    sql_code_del = "DELETE FROM %s WHERE bookmaker = %s AND sport = %s" % (table, bookmaker, sport)

    cursor.execute(sql_code_del)

    conn.commit()

    conn.close()


def create_moneylines(moneylines):
    logger = logging.getLogger(__name__)
    delete_previous("moneylines", moneylines[0]["bookmaker"], moneylines[0]["sport"])
    logger.info("Из базы данных удалены все манилайны по конторе {0} и спорту {1}".
                format(moneylines[0]["bookmaker"], moneylines[0]["sport"]))

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')

    cursor = conn.cursor()

    sql_code = 'INSERT INTO moneylines ' \
               '(`firstwin`, `secondwin`, `draw`' \
               ' `oddsdate`, `live`, `href`, `firstparticipant`, `secondparticipant`,' \
               ' `bookmaker`, `actual`, `sport`, `league`)' \
               ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    params = []

    for h in moneylines:
        params.append(
            (h["firstwin"], h["secondwin"], h["draw"],
             h["oddsdate"], h["live"], h["href"], h["firstparticipant"], h["secondparticipant"],
             h["bookmaker"], h["actual"], h["sport"], h["league"])
        )

    cursor.executemany(sql_code, params)

    conn.commit()

    logger.info("Добавлено {0} манилайнов".format(len(moneylines)))

    conn.close()





