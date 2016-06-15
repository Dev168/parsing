import MySQLdb as mysql
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWD, LIVENSHTAIN_MIN
import json
import os
import pandas as pd
from common.distance import distance

DIRNAME = os.path.dirname(os.path.abspath(__file__))


def init():
    """Инициализирует базу данных со всеми необходимыми таблицами
    Если база данных с именем DB_NAME уже существует то будет ошибка"""

    def __load_init_sports():
        with open(os.path.join(DIRNAME, "sports_create.json")) as f:
            text = f.read()
            return json.loads(text)

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD)

    cursor = conn.cursor()

    sql_code = "CREATE DATABASE IF NOT EXISTS {0}; USE {0}".format(DB_NAME)

    cursor.execute(sql_code)

    with open(os.path.join(DIRNAME, "mysql_create.sql"), "r") as f:
        sql_init_code = f.read()

        cursor.execute(sql_init_code)

        cursor.close()

        conn.close()

        print("База данных успешно инициализирована")

    create_sports(__load_init_sports())


def create_bookmaker(bookmaker_name):
    """Создает нового букмекера"""
    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    cursor = conn.cursor()

    sql_code = 'INSERT INTO bookmakers (Name) VALUES ("{0}")'.format(bookmaker_name)

    try:
        cursor.execute(sql_code)
        conn.commit()
        print("{0} контора успешно создана".format(bookmaker_name))
    except mysql.IntegrityError as err:
        print(err)

    cursor.close()

    conn.close()


def create_sports(sports):
    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    cursor = conn.cursor()

    sql_code = "INSERT INTO sports (`Name`) VALUES (%s)"

    cursor.executemany(sql_code, [(sport,) for sport in sports])

    conn.commit()

    conn.close()

    print("Добавлены новые виды спорта")


def create_participants(names, bookmaker_id):
    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    cursor = conn.cursor()

    cursor.executemany("INSERT INTO participants (name) VALUES (%s)", )


def get_bookmakers():
    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    cursor = conn.cursor()

    sql_code = "SELECT * FROM bookmakers"

    cursor.execute(sql_code)

    res = cursor.fetchall()

    cursor.close()

    conn.close()

    return res


def get_participants_from_db(_filter={"1": 1}):

    filter_sql = create_filter_sql(_filter)

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    all_names = pd.read_sql("SELECT participant, bookmaker name  as `name_from_db`, bookmaker FROM "
                            "participantnames WHERE %s",
                            con=conn, params=(filter_sql,))

    conn.close()

    return all_names


def create_filter_sql(dic={"1": 1}):

    filter_sql = ""
    if len(dic) > 0:
        first = True
        for key, value in dic.items():
            if not first:
                filter_sql += " AND "
            else:
                first = False
            filter_sql += key + "=" +str(value)
    return filter_sql


def resolve_participant_names(events_df, bookmaker_id):
    """Процедура для разрешения ссылок на спортивных участников
    получает список имен учатников, возвращает их id в базе данных
    Отсутствующих участников создает"""

    events_df = replace_names_by_id(events_df, bookmaker_id)

    events_df = replace_names_by_similarities(events_df)


def replace_names_by_id(events_df, bookmaker_id):

    bookmaker_participants_df = get_participants_from_db({"bookmaker": bookmaker_id})

    bookmaker_participants_df.set_index("name")

    participants_df = events_df.join(bookmaker_participants_df, "firstparticipant", rsuffix="1") \
        .join(bookmaker_participants_df, "secondparticipant", rsuffix="2")

    return participants_df.drop(
        ["name", "name2, bookmaker"])  # TODO: Лишняя строка, сделать левое соединение без необходимости удалять лишние столбики


def replace_names_by_similarities(df):

    def participants_without_id(df):
        ser1 = df["firstparticipant"][df["participant"].isnull()]

        ser2 = df["secondparticipant"][df["participant2"].isnull()]

        return pd.DataFrame({"missing_name": pd.Series(pd.concat([ser1, ser2]).unique)})

    def cartesian_product(df1, df2):
        df1["formerge"] = 1
        df2["formerge"] = 2
        result_df = df1.merge(df2, on="formerge")
        return result_df.drop(["formerge"])

    def calculate_distance(row, key1, key2):
        return distance(row[key1], row[key2])

    db_names = get_participants_from_db()

    missing_names = participants_without_id(df)

    missing_data = cartesian_product(db_names, missing_names)

    missing_data["distance"] = missing_data.apply(calculate_distance, axis=1, args=(('name_from_db', 'missing_name'),))

    return missing_data

    missing_data.groupby(["bookmaker, missing_name"])["distance"].min()



