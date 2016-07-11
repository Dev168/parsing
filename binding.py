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
            if el[0] == match[0] and el[1] == match[1] or \
                                    el[0] == match[1] and el[1] == match[0]:
                return el
        return None


conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True, charset='utf8')

cursor = conn.cursor()

sql_code = 'SELECT sports.id as id, sports.name as name, sports.bookmaker as bookmaker FROM sports' \
           'LEFT JOIN sportsmatch' \
           'ON sports.id = sportsmatch.sport' \
           'WHERE sportsmatch.id IS NULL'

cursor.execute(sql_code)

sports_without_matching = cursor.fetchall()

matched = Matched()
for sport1 in sports_without_matching:

    for sport2 in sports_without_matching:
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

matched_list = []
for el in matched.elements:
    if el[2] <= LIVENSHTAIN_MIN:
        matched_list.append((el[0], el[1]))

list_for_insert = []
for el in matched_list:
    uuid = uuid4().bytes
    list_for_insert.append(el[0], uuid)
    list_for_insert.append(el[1], uuid)

sql_code = 'INSERT INTO sportsmatch (`sport`, `uuid`) VALUES (%s, %s)'

cursor.exectemany(sql_code, list_for_insert)

conn.commit()

conn.close()


