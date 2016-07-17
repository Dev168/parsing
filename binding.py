from distance import distance
from settings import LOG_DIR
import pandas
import logging
import os
from datetime import datetime
import db_api


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

    logger = logging.getLogger(__name__)

    logger.info("* * * * * * * * * * * * * * * * *")
    logger.info("Начало автоматической обработки спортов")

    result = db_api.get_sports()

    optimized_result = [(el[0], el[1], el[2]) for el in result if el[4] is None]

    logger.info("{0} элементов не связаны".format(len(optimized_result)))

    df = pandas.DataFrame(optimized_result, columns=["id", "name", "bookmaker"])

    df2 = _cartesian_product(df)

    df3 = df2[df2.bookmaker_x != df2.bookmaker_y]

    if df3.empty:
        logger.info("Нет возможных комбинаций для связи")
        return

    logger.info("{0} возможных комбинаций для связи".format(len(df3)))

    df3["distance"] = df3.apply(_calculate_distance, axis=1, args=('name_x', 'name_y'))

    df4 = df3[df3.distance < 0.35]

    logger.info("{0} комбинаций для связи с расстоянием меньше 0.35".format(len(df4)))

    if df4.empty:
        return

    rows = [tuple(x) for x in df4[['id_x', 'id_y', 'distance', 'name_x', 'name_y']].values]

    best_rows = get_best_matching(rows)

    best_rows_msg = "\n".join([
                                  row[3] + " = " + row[4] + ": distance = " + str(row[2]) for row in best_rows
                                  ])

    msg = "Следующие спорты будут связаны: \n" + best_rows_msg

    logger.info(msg)

    db_api.update_sports(best_rows)


def match_leagues():

    logger = logging.getLogger(__name__)

    logger.info("* * * * * * * * * * * * * * * * *")
    logger.info("Начало автоматической обработки лиг")

    leagues = db_api.get_leagues()

    result = [(row[0], row[1], row[2], row[5]) for row in leagues if row[4] is None]

    logger.info("{0} элементов не связаны".format(len(result)))

    df = pandas.DataFrame(result, columns=["id", "name", "bookmaker", "sport"])

    df2 = _cartesian_product(df)

    df3 = df2[(df2['bookmaker_x'] != df2['bookmaker_y']) & (df2['sport_x'] == df2['sport_y'])]

    if df3.empty:
        logger.info("Нет возможных комбинаций для связи")
        return

    logger.info("{0} возможных комбинаций для связи".format(len(df3)))

    df3["distance"] = df3.apply(_calculate_distance, axis=1, args=('name_x', 'name_y'))

    df4 = df3[df3.distance < 0.35]

    logger.info("{0} комбинаций для связи с расстоянием меньше 0.35".format(len(df4)))

    if df4.empty:
        return

    rows = [tuple(x) for x in df4[['id_x', 'id_y', 'distance', 'name_x', 'name_y']].values]

    best_rows = get_best_matching(rows)

    best_rows_msg = "\n".join([
                                  row[3] + " = " + row[4] + ": distance = " + str(row[2]) for row in best_rows
                                  ])

    msg = "Следующие лиги будут связаны: \n" + best_rows_msg

    logger.info(msg)

    db_api.update_leagues(best_rows)


def match_participants():

    logger = logging.getLogger(__name__)

    logger.info("* * * * * * * * * * * * * * * * *")
    logger.info("Начало автоматической обработки участников")

    participants = db_api.get_participants()

    result = [(row[0], row[1], row[2], row[5]) for row in participants if row[4] is None]

    logger.info("{0} элементов не связаны".format(len(result)))

    df = pandas.DataFrame(result, columns=["id", "name", "bookmaker", "league"])

    df2 = _cartesian_product(df)

    df3 = df2[(df2['bookmaker_x'] != df2['bookmaker_y']) & (df2['league_x'] == df2['league_y'])]

    if df3.empty:
        logger.info("Нет возможных комбинаций для связи")
        return

    logger.info("{0} возможных комбинаций для связи".format(len(df3)))

    df3["distance"] = df3.apply(_calculate_distance, axis=1, args=('name_x', 'name_y'))

    df4 = df3[df3.distance < 0.35]

    logger.info("{0} комбинаций для связи с расстоянием меньше 0.35".format(len(df4)))

    if df4.empty:
        return

    rows = [tuple(x) for x in df4[['id_x', 'id_y', 'distance', 'name_x', 'name_y']].values]

    best_rows = get_best_matching(rows)

    best_rows_msg = "\n".join([
                                  row[3] + " = " + row[4] + ": distance = " + str(row[2]) for row in best_rows
                                  ])

    msg = "Следующие участники будут связаны: \n" + best_rows_msg

    logger.info(msg)

    db_api.update_participants(best_rows)


time = datetime.utcnow()
logname = time.strftime("auto_bind_%d.%m.%Y.log")
logpath = os.path.join(LOG_DIR, logname)
handler = logging.FileHandler(logpath, "a",
                              encoding="UTF-8")
formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

match_sports()

match_leagues()

match_participants()

for handler in logger.handlers:
    handler.close()


















