import parsing.main
from tests.t1.test import load_test_data
events = load_test_data()
import db.database as d
import pandas as pd
import MySQLdb as mysql
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWD

df = parsing.main.replace_names_by_id(events, 1)

missing_names = parsing.main.participants_without_id(df)


conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)
db_names = pd.read_sql("SELECT participant, bookmaker, name  as `name_from_db`, bookmaker FROM "
                       "participantnames",
                       con=conn)
conn.close()


missing_data = parsing.main.cartesian_product(db_names, missing_names)


if missing_data.empty:
    pass

missing_data["distance"] = missing_data.apply(parsing.main.calculate_distance, axis=1, args=('name_from_db', 'missing_name'))

creating_participants = parsing.main.participants_without_id(df)

created_participants = d.create_participants(creating_participants)

merged_participants = df.merge(created_participants, how='left', left_on="firstparticipant", right_on="Name").merge(
    created_participants, how="left",
    left_on="secondparticipant",
    right_on="Name")

merged_participants.loc[merged_participants["participant"].isnull(), "participant"] = \
    merged_participants.loc[merged_participants["participant"].isnull()]["id_x"]

merged_participants.loc[merged_participants["participant2"].isnull(), "participant2"] = \
    merged_participants.loc[merged_participants["participant2"].isnull()]["id_y"]

merged_participants.columns.drop(["id_x", "id_y", "Name_x", "Name_y"])
