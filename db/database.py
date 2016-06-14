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


def get_participant_ids(names, bookmaker_id=None):
    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    cursor = conn.cursor()

    if bookmaker_id is not None:
        cursor.execute("SELECT participant, name FROM participantnames WHERE bookmaker = %s AND name in %s",
                       (bookmaker_id, names))
    else:
        cursor.execute("SELECT Participant, name, Bookmaker  FROM participantnames WHERE name in %s",
                       (bookmaker_id, names))

    result = cursor.fetchall()

    cursor.close()

    conn.close()

    return result


def resolve_participant_names(events, bookmaker_id):
    """Процедура для разрешения ссылок на спортивных участников
    получает список имен учатников, возвращает их id в базе данных
    Отсутствующих участников создает"""

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    bookmaker_participants_df = pd.read_sql("SELECT name, participant FROM participantnames WHERE bookmaker = 1",
                                            con=conn)

    conn.close()

    bookmaker_participants_df.set_index("name")

    events_df = pd.DataFrame(events["handicap"])

    events_df = events_df.join(bookmaker_participants_df, "firstparticipant", rsuffix="1")\
        .join(bookmaker_participants_df, "secondparticipant", rsuffix="2")

    semantic_name_resolving(events_df)


def semantic_name_resolving(df):

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    all_names = pd.read_sql("SELECT participant, name, bookmaker FROM participantnames", con=conn)

    conn.close()

    ser = df["firstparticipant"][df["participant"].isnull()]

    ser2 = df["secondparticipant"][df["participant2"].isnull()]

    df = ser.apply(cluster_analysis_resolving, axis=1, args=(all_names,))


def cluster_analysis_resolving(name, cluster_df):






def detect_possible_participant(names):
    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    df = pd.read_sql("SELECT participant, name, bookmaker FROM participantnames", con=conn)

    conn.close()

    founded_names = []

    for name in names:

        df["probability"] = df["name"].apply(distance, args=(name,))

        idx = df.groupby("participant")["probability"].transform(min) == df["probability"]

        filtered_df = df[idx][df["probability"] < LIVENSHTAIN_MIN]

        if len(filtered_df) > 0:
            id_participant = filtered_df['participant'].value_counts().idmax()

            founded_names.append({"name": name, "participant": id_participant})

    return founded_names
