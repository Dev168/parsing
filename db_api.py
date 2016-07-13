import MySQLdb as mysql
from distance import distance
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWD, LOG_DIR
from uuid import uuid4
import pandas
import logging
import os
from datetime import datetime


def get_sports():
    """
Возвращает из базы данных все спорты
    :rtype: tuple of tuples
    """
    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')

    cursor = conn.cursor()

    sql_code = 'SELECT sports.id, sports.name, sports.bookmaker, bookmakers.name, sportsmatch.uuid ' \
               'FROM sports ' \
               'LEFT JOIN sportsmatch ' \
               'ON sports.id = sportsmatch.sport ' \
               'LEFT JOIN bookmakers ' \
               'ON sports.bookmaker = bookmakers.id ' \

    cursor.execute(sql_code)

    result = cursor.fetchall()

    conn.close()

    return result


def update_sports(sports):
    """
Обновляет в базе данных сопоставление спортов
    :param sports: list of tuples: (sport: int, uuid: string)
    """

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')

    cursor = conn.cursor()

    sqlcode = "INSERT into sportsmatch (`sport`, `uuid`) VALUES (%s, %s)"

    try:
        cursor.executemany(sqlcode, sports)
    except:
        conn.close()
        raise
    conn.commit()

    conn.close()
