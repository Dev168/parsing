import MySQLdb as mysql
from distance import distance
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWD, LIVENSHTAIN_MIN
from uuid import uuid4


class Matched():


    elements = []

    def get(self, match):
        """
        Проверяет вхождение
        :rtype: bool
        :type match: tuple
        """
        for el in self.elements:
            if el[0] == match[0] or el[1] == match[1] or \
                                    el[0] == match[1] or el[1] == match[0]:
                return el
        return None


def matching(matched_table, matching_table, match_field):

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')

    cursor = conn.cursor()

    sql_code = 'SELECT {0}.id as id, {0}.name as name, {0}.bookmaker as bookmaker FROM {0} ' \
               'LEFT JOIN {1} ' \
               'ON {0}.id = {1}.{2} ' \
               'WHERE {1}.uuid IS NULL'.format(matched_table, matching_table, match_field)

    cursor.execute(sql_code)

    rows_without_matching = cursor.fetchall()

    print("Для {0} строк не найдены соответствия в таблице соответствий".format(str(len(rows_without_matching))))

    matched = Matched()
    for sport1 in rows_without_matching:
        for sport2 in rows_without_matching:
            if sport1[2] != sport2[2]:  # Если строчки для разных букмекеров
                dist = distance(sport1[1], sport2[1])
                match = (sport1[0], sport2[0], dist)
                existed_match = matched.get(match)
                if existed_match is None:
                    matched.elements.append(match)
                else:
                    if existed_match[2] > match[2]:
                        matched.elements.remove(existed_match)
                        matched.elements.append(match)

    print("Установлено {0} соответствий с тем или иным расстоянием левинштейна".format(
        str(
            len(matched.elements)
        )
    ))

    matched_list = []
    for el in matched.elements:
        if el[2] <= LIVENSHTAIN_MIN:
            matched_list.append((el[0], el[1]))

    print("Только {0} соответствий обладают расстоянием левенштейна менее {1}".format(
        str(len(matched_list)),
        str(LIVENSHTAIN_MIN)
    ))

    list_for_insert = []
    for el in matched_list:
        uuid = uuid4().bytes
        list_for_insert.append((el[0], uuid))
        list_for_insert.append((el[1], uuid))

    sql_code = 'INSERT INTO {0} (`{1}`, `uuid`) VALUES (%s, %s)'.format(matching_table, match_field)

    try:
        cursor.executemany(sql_code, list_for_insert)
    except:
        raise
    conn.commit()

    conn.close()


print("Поехали, спорты!")
matching("sports", "sportsmatch", "sport")

print("Поехали, лиги!!!111!")
matching("leagues", "leaguesmatch", "league")

print("Поехали, УЧАСТНИКИ!!!11111!")
matching("participants", "participantsmatch", "participant")



























