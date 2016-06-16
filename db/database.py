import MySQLdb as mysql
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWD
import json
import os
import pandas as pd
from common.distance import distance

#DIRNAME = os.path.dirname(os.path.abspath(__file__))
DIRNAME = "/"

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


def create_participants(names_df):

    names_df.columns = ["name"]
    names_list = names_df["name"].tolist()
    par = [(el,) for el in names_list]

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    cursor = conn.cursor()

    sql_code = "INSERT INTO participants (`Name`) VALUES (%s)"

    cursor.executemany(sql_code, par)

    conn.commit()

    df = pd.read_sql("SELECT * FROM participants WHERE name in %(names)s", con=conn, params={"names": names_list})

    conn.close()

    return df


def create_participant_names(names_df, bookmaker_id):

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    names_df.columns = ["participant", "name"]
    names_df["bookmaker"] = bookmaker_id

    names_df.to_sql("participantnames", con=conn)

    names_df = names_df.columns.drop("bookmaker")

    names_df.columns = ["id", "name"]

    conn.close()


def create_events(events_df):
    raise NotImplementedError


def get_bookmakers():
    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    cursor = conn.cursor()

    sql_code = "SELECT * FROM bookmakers"

    cursor.execute(sql_code)

    res = cursor.fetchall()

    cursor.close()

    conn.close()

    return res


def store_events(events_df, bookmaker_id):

    events_df = resolve_participant_names(events_df, bookmaker_id)

    create_events(events_df)


def resolve_participant_names(events_df, bookmaker_id):
    """Процедура для разрешения ссылок на спортивных участников
    получает список имен учатников, возвращает их id в базе данных
    Отсутствующих участников создает"""

    events_df = replace_names_by_id(events_df, bookmaker_id)

    events_df = replace_names_by_similarities(events_df)

    events_df = replace_names_by_created_id(events_df, bookmaker_id)

    return events_df


def replace_names_by_id(events_df, bookmaker_id):

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    bookmaker_participants_df = pd.read_sql("SELECT participant, name  FROM "
                            "participantnames WHERE %s",
                            con=conn, params=(bookmaker_id,))

    conn.close()

    bookmaker_participants_df.set_index("name")

    participants_df = events_df.\
        merge(bookmaker_participants_df, how="left", left_on="firstparticipant", right_on="name").\
        merge(bookmaker_participants_df, how="left", left_on="secondparticipant", right_on="name")

    return participants_df.drop(
        ["name_x", "name_y"], axis=1)  # TODO: Лишняя строка, сделать левое соединение без необходимости удалять лишние столбики


def replace_names_by_similarities(df):

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    db_names = pd.read_sql("SELECT participant, bookmaker, name  as `name_from_db`, bookmaker FROM "
                            "participantnames",
                            con=conn)

    conn.close()

    missing_names = participants_without_id(df)

    missing_data = cartesian_product(db_names, missing_names)

    if missing_data.empty:
        return df

    missing_data["distance"] = missing_data.apply(calculate_distance, axis=1, args=('name_from_db', 'missing_name'))

    #  TODO доработать логику распознавания


def replace_names_by_created_id(df, bookmaker_id):

    creating_participants = participants_without_id(df)

    if creating_participants.empty:
        return df

    created_participants = create_participants(creating_participants)

    create_participant_names(created_participants, bookmaker_id)

    merged_participants = df.merge(created_participants, how='left', left_on="firstparticipant", right_on="Name").merge(created_participants, how="left",
                                                                                 left_on="secondparticipant",
                                                                                 right_on="Name")

    merged_participants.loc[merged_participants["participant"].isnull(), "participant"] = \
        merged_participants.loc[merged_participants["participant"].isnull()]["id_x"]

    merged_participants.loc[merged_participants["participant2"].isnull(), "participant2"] = \
        merged_participants.loc[merged_participants["participant2"].isnull()]["id_y"]

    merged_participants = merged_participants.columns.drop(["id_x", "id_y", "Name_x", "Name_y"])

    return merged_participants


def participants_without_id(df):

    ser1 = df["firstparticipant"][df["participant_x"].isnull()]

    ser2 = df["secondparticipant"][df["participant_y"].isnull()]

    conc_ser = pd.concat([ser1, ser2], ignore_index=True)

    return pd.DataFrame({"missing_name": conc_ser.unique()})


def cartesian_product(df1, df2):
    df1["formerge"] = 1
    df2["formerge"] = 1
    result_df = df1.merge(df2, on="formerge")
    return result_df.drop(["formerge"], axis=1)


def calculate_distance(row, key1, key2):
    return distance(row[key1], row[key2])


