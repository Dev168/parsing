import MySQLdb as mysql
import pandas as pd

import db.database as db
from distance import distance
from settings import DB_HOST, DB_USER, DB_PASSWD, DB_NAME, LIVENSHTAIN_MIN


def resolve_participant_names(events_df, bookmaker_id):
    """Процедура для разрешения ссылок на спортивных участников
    получает список имен учатников, возвращает их id в базе данных
    Отсутствующих участников создает"""

    if events_df.empty:
        return events_df

    events_df = _replace_names_by_id(events_df, bookmaker_id)

    events_df = _replace_names_by_similarities(events_df, bookmaker_id)

    events_df = _replace_names_by_created_id(events_df, bookmaker_id)

    events_df = events_df.drop(["firstparticipant", "secondparticipant"], 1)

    events_df = events_df.rename(
        columns={"participant_x": "firstparticipant", "participant_y": "secondparticipant"})

    return events_df


def _replace_names_by_id(events_df, bookmaker_id):

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    bookmaker_participants_df = pd.read_sql("SELECT participant, name  FROM "
                            "participantnames WHERE bookmaker = %s",
                            con=conn, params=(bookmaker_id,))

    conn.close()

    bookmaker_participants_df.set_index("name")

    participants_df = events_df.\
        merge(bookmaker_participants_df, how="left", left_on="firstparticipant", right_on="name").\
        merge(bookmaker_participants_df, how="left", left_on="secondparticipant", right_on="name")

    return participants_df.drop(
        ["name_x", "name_y"], axis=1)  # TODO: Лишняя строка, сделать левое соединение без необходимости удалять лишние столбики


def _replace_names_by_similarities(df, bookmaker_id):

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    db_names = pd.read_sql("SELECT participant, bookmaker, name  as `name_from_db`, bookmaker FROM "
                            "participantnames WHERE bookmaker != %s",
                            con=conn, params=(bookmaker_id,))

    conn.close()

    missing_names = _participants_without_id(df)

    missing_data = _cartesian_product(db_names, missing_names)

    if missing_data.empty:
        return df

    missing_data["distance"] = missing_data.apply(_calculate_distance, axis=1, args=('name_from_db', 'missing_name'))

    similar_participants = missing_data[missing_data["distance"] <= LIVENSHTAIN_MIN][["participant", "missing_name"]]
    similar_participants.columns = ["participant", "name"]
    similar_participants = similar_participants.groupby("name").max()
    similar_participants.reset_index(level=0, inplace=True)
    similar_participants = similar_participants.reindex_axis(["participant", "name"], 1)
    created_participants = db.create_participant_names(similar_participants, bookmaker_id)

    merged_participants = df.merge(created_participants, how='left', left_on="firstparticipant", right_on="name").merge(
        created_participants, how="left",
        left_on="secondparticipant",
        right_on="name")

    merged_participants.loc[merged_participants["participant_x"].isnull(), "participant_x"] = \
        merged_participants.loc[merged_participants["participant_x"].isnull()]["id_x"]

    merged_participants.loc[merged_participants["participant_y"].isnull(), "participant_y"] = \
        merged_participants.loc[merged_participants["participant_y"].isnull()]["id_y"]

    merged_participants = merged_participants.drop(["id_x", "id_y", "name_x", "name_y"], 1)

    return merged_participants


def _replace_names_by_created_id(df, bookmaker_id):

    creating_participants = _participants_without_id(df)

    if creating_participants.empty:
        return df

    print("Следующие участники будут созданы в базе")
    print(creating_participants)

    created_participants = db.create_participants(creating_participants)

    created_participants = db.create_participant_names(created_participants, bookmaker_id)

    merged_participants = df.merge(created_participants, how='left', left_on="firstparticipant", right_on="name").merge(created_participants, how="left",
                                                                                 left_on="secondparticipant",
                                                                                 right_on="name")

    merged_participants.loc[merged_participants["participant_x"].isnull(), "participant_x"] = \
        merged_participants.loc[merged_participants["participant_x"].isnull()]["id_x"]

    merged_participants.loc[merged_participants["participant_y"].isnull(), "participant_y"] = \
        merged_participants.loc[merged_participants["participant_y"].isnull()]["id_y"]

    merged_participants = merged_participants.drop(["id_x", "id_y", "name_x", "name_y"], 1)

    return merged_participants


def _participants_without_id(df):

    ser1 = df["firstparticipant"][df["participant_x"].isnull()]

    ser2 = df["secondparticipant"][df["participant_y"].isnull()]

    conc_ser = pd.concat([ser1, ser2], ignore_index=True)

    return pd.DataFrame({"missing_name": conc_ser.unique()})


def _cartesian_product(df1, df2):
    df1["formerge"] = 1
    df2["formerge"] = 1
    result_df = df1.merge(df2, on="formerge")
    return result_df.drop(["formerge"], axis=1)


def _calculate_distance(row, key1, key2):
    return distance(row[key1], row[key2])


def store_handicaps(handicaps_json, bookmaker_id):

    handicaps_df = pd.DataFrame(handicaps_json)

    handicaps_df = resolve_participant_names(handicaps_df, bookmaker_id)

    db.create_handicaps(handicaps_df)

