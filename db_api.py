import MySQLdb as mysql
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWD
from uuid import uuid4


class BelongException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


def get_sports():
    """
Возвращает из базы данных все спорты
    :rtype: tuple of tuples
    """
    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')

    cursor = conn.cursor()

    sql_code = 'SELECT sports.id, sports.name, sports.bookmaker, bookmakers.name, sports.uuid ' \
               'FROM sports ' \
               'LEFT JOIN bookmakers ' \
               'ON sports.bookmaker = bookmakers.id '

    cursor.execute(sql_code)

    result = cursor.fetchall()

    conn.close()

    return result


def get_leagues(sport_uuid=None):

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')

    cursor = conn.cursor()

    #  TODO: Следующий код сильно подвержен SQL иньекциям! Необходимо переписать безопасно!

    if sport_uuid is None:
        sport_uuid_parameter = "WHERE sports.uuid IS NOT NULL"
    else:
        sport_uuid_parameter = "WHERE sports.uuid = %s" % sport_uuid

    sql_code = 'SELECT leagues.id, leagues.name, leagues.bookmaker, ' \
               'bookmakers.name, leagues.uuid, sports.uuid as sport, sports.name as sportname ' \
               'FROM leagues ' \
               'LEFT JOIN bookmakers ' \
               'ON leagues.bookmaker = bookmakers.id ' \
               'LEFT JOIN sports ' \
               'ON leagues.sport = sports.id ' \
               '%s' % sport_uuid_parameter

    cursor.execute(sql_code)

    result = cursor.fetchall()

    conn.close()

    return result


def get_participants(league_uuid=None):
    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')

    cursor = conn.cursor()

    #  TODO: Следующий код сильно подвержен SQL иньекциям! Необходимо переписать безопасно!

    if league_uuid is None:
        league_uuid_parameter = "WHERE leagues.uuid IS NOT NULL AND sports.uuid IS NOT NULL"
    else:
        league_uuid_parameter = "WHERE leagues.uuid = %s" % league_uuid

    sql_code = 'SELECT participants.id, participants.name, participants.bookmaker, ' \
               'bookmakers.name, participants.uuid, leagues.uuid as league, leagues.name as leaguename, ' \
               'sports.uuid as sport, sports.name as sportname ' \
               'FROM participants ' \
               'LEFT JOIN bookmakers ' \
               'ON participants.bookmaker = bookmakers.id ' \
               'LEFT JOIN leagues ' \
               'ON participants.league = leagues.id ' \
               'LEFT JOIN sports ' \
               'ON leagues.sport = sports.id ' \
               '%s' % league_uuid_parameter

    cursor.execute(sql_code)

    result = cursor.fetchall()

    conn.close()

    return result


def update_sports(sports):

    update_uuid("sports", sports)


def update_leagues(leagues):

    update_uuid("leagues", leagues)


def update_participants(participants):

    update_uuid("participants", participants)


def update_uuid(table_name, uuid_list):

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')

    cursor = conn.cursor()

    new_uuid_list = []
    for row in uuid_list:
        uuid_ = uuid4().bytes.hex()
        new_uuid_list.append((uuid_, row[0]))
        new_uuid_list.append((uuid_, row[1]))

    try:
        ids_parameter = ', '.join(list(map(lambda id_: '%s', new_uuid_list)))
        sql_select = "SELECT DISTINCT uuid " \
                     "FROM %s " \
                     "WHERE id in (%s) FOR UPDATE" % (table_name, ids_parameter)
        cursor.execute(sql_select, [el[1] for el in new_uuid_list])
        reset_rows = cursor.fetchall()

        sql_reset = "UPDATE %s SET uuid = NULL WHERE uuid IN (%s)" % \
                    (table_name, ', '.join(list(map(lambda id_: '%s', reset_rows))))
        cursor.execute(sql_reset, reset_rows)

        cursor.executemany("UPDATE {0} SET uuid = %s WHERE id = %s".format(table_name), new_uuid_list)

    except:
        conn.close()
        raise
    conn.commit()

    conn.close()




