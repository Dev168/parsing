import MySQLdb as mysql
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWD
from uuid import uuid4


class BelongException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


# Методы используемые фронтэндом


def get_sport_select_list():

    """
Возвращает список спортов с уникальными uuid из базы данных (имя берется произвольно из одной из контор)
    :return:
    """
    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')

    cursor = conn.cursor()

    sql_code = 'SELECT name, uuid FROM sports GROUP BY uuid'

    cursor.execute(sql_code)

    result = cursor.fetchall()

    conn.close()

    return result


def get_leagues_select_list(sportuuid):
    """
Возвращает список диг с уникальными uuid из базы данных (имя берется произвольно из одной из контор)
    :return:
    """
    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')

    cursor = conn.cursor()

    sql_code = 'SELECT leagues.name, leagues.uuid ' \
               'FROM leagues ' \
               'LEFT JOIN sports ' \
               'ON leagues.sport = sports.id ' \
               'WHERE sports.uuid = %s' \
               'GROUP BY uuid'

    cursor.execute(sql_code, (sportuuid,))

    result = cursor.fetchall()

    conn.close()

    return result


def get_participants_list(bookmaker_id, league_uuid, full=False):

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')

    cursor = conn.cursor()

    if full:
        cond_part = ""
    else:
        cond_part = "AND participants.uuid IS NULL "

    sql_code = "SELECT participants.id, participants.name, participants.uuid " \
               "FROM participants " \
               "LEFT JOIN leagues " \
               "ON participants.league = leagues.id " \
               "WHERE participants.bookmaker = %s " \
               "AND leagues.uuid = %s " \
               "{0} " \
               "ORDER BY participants.name".format(cond_part)

    cursor.execute(sql_code, (bookmaker_id, league_uuid))

    result = cursor.fetchall()

    json_obj = [{"id": row[0], "name": row[1], "uuid": row[2]} for row in result]

    conn.close()

    return json_obj


def get_leagues_list(bookmaker_id, sport_uuid, full=False):

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')

    cursor = conn.cursor()

    if full:
        cond_part = ""
    else:
        cond_part = "AND leagues.uuid IS NULL "

    sql_code = "SELECT leagues.id, leagues.name, leagues.uuid " \
               "FROM leagues " \
               "LEFT JOIN sports " \
               "ON leagues.sport = sports.id " \
               "WHERE leagues.bookmaker = %s " \
               "AND sports.uuid = %s " \
               "{0} " \
               "ORDER BY leagues.name".format(cond_part)

    cursor.execute(sql_code, (bookmaker_id, sport_uuid))

    result = cursor.fetchall()

    json_obj = [{"id": row[0], "name": row[1], "uuid": row[2]} for row in result]

    conn.close()

    return json_obj


def get_sports_list(bookmaker_id, full=False):

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')

    cursor = conn.cursor()

    if full:
        cond_part = ""
    else:
        cond_part = "AND sports.uuid IS NULL "

    sql_code = "SELECT sports.id, sports.name, sports.uuid " \
               "FROM sports " \
               "WHERE sports.bookmaker = %s " \
               "{0} " \
               "ORDER BY sports.name".format(cond_part)

    cursor.execute(sql_code, (bookmaker_id,))

    result = cursor.fetchall()

    json_obj = [{"id": row[0], "name": row[1], "uuid": row[2]} for row in result]

    conn.close()

    return json_obj


def get_participants_matches(league_uuid):
    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')

    cursor = conn.cursor()

    sql_code = 'SELECT participants.id, participants.name, participants.uuid, participants.bookmaker ' \
               'FROM participants ' \
               'LEFT JOIN leagues ' \
               'ON participants.league = leagues.id ' \
               'WHERE participants.uuid IS NOT NULL ' \
               'AND leagues.uuid = %s ' \
               'ORDER BY participants.uuid'

    cursor.execute(sql_code, (league_uuid,))

    result = cursor.fetchall()
    json_obj = []

    for i in range(1, len(result), 2):
        first = result[i]
        second = result[i-1]

        if first[3] != 1:
            first, second = second, first

        if first[2] == second[2]:
            json_obj.append(
                {"id1": first[0],
                 "name1": first[1],
                 "uuid": first[2],
                 "id2": second[0],
                 "name2": second[1]
                 }
            )
        else:
            return {"error": True}

    conn.close()

    return json_obj


def get_leagues_matches(sport_uuid):
    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')

    cursor = conn.cursor()

    sql_code = 'SELECT leagues.id, leagues.name, leagues.uuid, leagues.bookmaker ' \
               'FROM leagues ' \
               'LEFT JOIN sports ' \
               'ON leagues.sport = sports.id ' \
               'WHERE leagues.uuid IS NOT NULL ' \
               'AND sports.uuid = %s ' \
               'ORDER BY leagues.uuid'

    cursor.execute(sql_code, (sport_uuid,))

    result = cursor.fetchall()
    json_obj = []

    for i in range(1, len(result), 2):
        first = result[i]
        second = result[i-1]

        if first[3] != 1:
            first, second = second, first

        if first[2] == second[2]:
            json_obj.append(
                {"id1": first[0],
                 "name1": first[1],
                 "uuid": first[2],
                 "id2": second[0],
                 "name2": second[1]
                 }
            )
        else:
            return {"error": True}

    conn.close()

    return json_obj


def get_sports_matches():
    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')

    cursor = conn.cursor()

    sql_code = 'SELECT sports.id, sports.name, sports.uuid, sports.bookmaker ' \
               'FROM sports ' \
               'WHERE sports.uuid IS NOT NULL ' \
               'ORDER BY sports.uuid'

    cursor.execute(sql_code)

    result = cursor.fetchall()
    json_obj = []

    for i in range(1, len(result), 2):
        first = result[i]
        second = result[i-1]

        if first[3] != 1:
            first, second = second, first

        if first[2] == second[2]:
            json_obj.append(
                {"id1": first[0],
                 "name1": first[1],
                 "uuid": first[2],
                 "id2": second[0],
                 "name2": second[1]
                 }
            )
        else:
            return {"error": True}

    conn.close()

    return json_obj


def get_events(bookmaker_id):

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')

    cursor = conn.cursor()

    sql_code = '(SELECT h.firstforward, h.secondforward, h.firstwin, h.secondwin, h.oddsdate, h.href, ' \
               's.name as sport, p1.name as p1, p2.name as p2, l.name as league ' \
               'FROM betsdb.handicaps as h ' \
               'LEFT JOIN sports as s ' \
               'ON h.sport = s.id ' \
               'LEFT JOIN leagues as l ' \
               'ON h.league = l.id ' \
               'LEFT JOIN participants as p1 ' \
               'ON h.firstparticipant = p1.id ' \
               'LEFT JOIN participants as p2 ' \
               'ON h.secondparticipant = p2.id ' \
               'WHERE h.bookmaker = %s) ' \
               'UNION ' \
               '(SELECT null, h.draw, h.firstwin, h.secondwin, h.oddsdate, h.href, ' \
               's.name as sport, p1.name as p1, p2.name as p2, l.name as league ' \
               'FROM betsdb.moneylines as h ' \
               'LEFT JOIN sports as s ' \
               'ON h.sport = s.id ' \
               'LEFT JOIN leagues as l ' \
               'ON h.league = l.id ' \
               'LEFT JOIN participants as p1 ' \
               'ON h.firstparticipant = p1.id ' \
               'LEFT JOIN participants as p2 ' \
               'ON h.secondparticipant = p2.id ' \
               'WHERE h.bookmaker = %s)'

    cursor.execute(sql_code, (bookmaker_id,bookmaker_id))

    result = cursor.fetchall()

    json_obj = {}

    for row in result:
        sport = row[6]
        league = row[9]
        first_participant = row[7]
        second_participant = row[8]
        participants = " - ".join((first_participant, second_participant))

        if sport not in json_obj:
            json_obj[sport] = {}
        sport_json = json_obj[sport]

        if league not in sport_json:
            sport_json[league] = {}
        league_json = sport_json[league]

        if participants not in league_json:
            league_json[participants] = {}
        participants_json = league_json[participants]

        if row[0] is not None:
            if "handicaps" not in participants_json:
                participants_json["handicaps"] = []
            handicaps = participants_json["handicaps"]
            handicaps.append(
                {
                 "firstforward": row[0],
                 "secondforward": row[1],
                 "firstwin": row[2],
                 "secondwin": row[3],
                 "oddsdate": row[4].strftime("%H:%M:%S %d.%m.%Y"),
                 "href": row[5]
                 })
        else:
            if "moneylines" not in participants_json:
                participants_json["moneylines"] = []
            moneylines = participants_json["moneylines"]
            moneylines.append(
                {
                    "draw": row[1],
                    "firstwin": row[2],
                    "secondwin": row[3],
                    "oddsdate": row[4].strftime("%H:%M:%S %d.%m.%Y"),
                    "href": row[5]
                })

    conn.close()

    return json_obj

# Методы применяемые автобиндингом


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
        sport_uuid_parameter = "WHERE sports.uuid = '%s'" % sport_uuid

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




