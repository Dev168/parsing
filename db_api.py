import MySQLdb as mysql
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWD
from uuid import uuid4


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
               'ON sports.bookmaker = bookmakers.id '

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

    insert_rows = []
    ids = []
    for row in sports:
        uuid_ = uuid4().bytes.hex()
        insert_rows.append((row[0], uuid_))
        insert_rows.append((row[1], uuid_))
        ids.append(row[0])
        ids.append(row[1])

    ids_parameter = ', '.join(list(map(lambda id_: '%s', ids)))

    sql_select = "SELECT sport, uuid FROM sportsmatch WHERE sport in (%s) FOR UPDATE" % ids_parameter

    sql_delete = "DELETE FROM sportsmatch WHERE uuid in (%s)"

    sql_insert = "INSERT into sportsmatch (`sport`, `uuid`) VALUES (%s, %s)"

    try:
        cursor.execute(sql_select, ids)
        rows = cursor.fetchall()
        set_ = {}
        for row in rows:
            set.add(row[1])
        list_ = list(set_)

        if len(list_) > 0:
            cursor.execute(sql_delete, list_)

        cursor.executemany(sql_insert, insert_rows)

    except:
        conn.close()
        raise
    conn.commit()

    conn.close()


def get_leagues(sport_uuid=None):

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')

    cursor = conn.cursor()

    #  TODO: Следующий код сильно подвержен SQL иньекциям! Необходимо переписать безопасно!

    if sport_uuid is None:
        sport_uuid_parameter = ""
    else:
        sport_uuid_parameter = "WHERE sportsmatch.uuid = %s" % sport_uuid

    sql_code = 'SELECT leagues.id, leagues.name, leagues.bookmaker, ' \
               'bookmakers.name, leaguesmatch.uuid, sportsmatch.uuid as sport, sports.name as sportname ' \
               'FROM leagues ' \
               'LEFT JOIN sportsmatch ' \
               'ON leagues.sport = sportsmatch.sport ' \
               'LEFT JOIN leaguesmatch ' \
               'ON leagues.id = leaguesmatch.league ' \
               'LEFT JOIN bookmakers ' \
               'ON leagues.bookmaker = bookmakers.id ' \
               'LEFT JOIN sports ' \
               'ON leagues.sport = sports.id' \
               '%s' % sport_uuid_parameter

    cursor.execute(sql_code)

    result = cursor.fetchall()

    conn.close()

    return result


def update_leagues():
    pass


def get_participants():
    pass


def update_participants():
    pass
