from bookmakers.Sbobet import Sbobet
import MySQLdb as mysql
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWD


def get_football_test():
    sb = Sbobet()
    with open("football.html", encoding="utf8") as page:
        events = sb.events(debug_page=page)
        handicaps = events["handicap"]
        for h in handicaps:
            h["bookmaker"] = sb.bookmaker_id
        return events


def resolve_links(list_of_dicts, aim_field, filter_field, table):

    unique_dicts = get_dicts_with_unique_values_of_keys(list_of_dicts, aim_field, filter_field)

    rolled_dict = list_of_dicts_roll_to_dict_of_lists(unique_dicts, filter_field, aim_field)

    id_list = get_id_from_db(rolled_dict, table, filter_field, aim_field)
    
    return replace_attribute_value(id_list, list_of_dicts, (aim_field, filter_field), "id_", aim_field)


def get_dicts_with_unique_values_of_keys(list_of_dicts, aim_field, filter_field):
    unique_values_local = []
    for dict_ in list_of_dicts:
        new_dict = {
            aim_field: dict_[aim_field],
            filter_field: dict_[filter_field]
        }
        if new_dict not in unique_values_local:
            unique_values_local.append(new_dict)
    return unique_values_local


def list_of_dicts_roll_to_dict_of_lists(list_of_dicts, key, outkey):

    rolled_dict = {}
    for dict_ in list_of_dicts:
        dictkey = dict_[key]
        if dictkey not in rolled_dict.keys():
            rolled_dict[dictkey] = []

        rolled_dict[dictkey].append(dict_[outkey])

    return rolled_dict


def get_id_from_db(dict_of_lists, table, filter_field, aim_field):

    result = []

    def find(value, tuples):
        for tuple_ in tuples:
            if value == tuple_[1]:
                return tuple_[0]
        return None

    for key in dict_of_lists:

        names = dict_of_lists[key]

        tuples = get_from_db(table, names, filter_field, key)

        absent_names = []

        for name in names:

            id_ = find(name, tuples)

            if id_ is None:
                absent_names.append(name)
            else:
                result.append({filter_field: key, aim_field: name, id_: id_})

        tuples = insert_to_db(absent_names, table, filter_field, key)

        for name in absent_names:
            id_ = find(name, tuples)
            result.append({filter_field: key, aim_field: name, id_: id_})

    return result


def insert_to_db(absent_names, table, filter_field, filter_value):
    with mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True,
                       charset='utf8') as cursor:
        sql_request = "INSERT INTO {0} (`Name`, `{1}`) VALUES (%s, {2})".format(table, filter_field, filter_value)
        cursor.executemany(sql_request, absent_names)

    return get_from_db(table, absent_names, filter_field, filter_value)


def get_from_db(table, values, filter_field, filter_value):

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME, use_unicode=True,
                       charset='utf8')

    cursor = conn.cursor()
    sql_request = "SELECT id, name from {0} WHERE name IN (%s) AND {1} = {2}".format(table, filter_field, filter_value)
    in_p = ', '.join(list(map(lambda x: '%s', values)))
    sql_request = sql_request % in_p
    cursor.execute(sql_request, values)

    result = cursor.fetchall()
    conn.close()
    return result


def replace_attribute_value(substitutional_objs, subsitutable_objs, match_attrs, substitutional_attr, subsitutable_atrr):

    for substitutional_obj in substitutional_objs:
        for subsitutable_obj in subsitutable_objs:
            eq = True
            for attr in match_attrs:
                if subsitutable_obj[attr] != substitutional_obj[attr]:
                    eq = False
                    break
            if eq:
                subsitutable_obj[subsitutable_atrr] = substitutional_obj[substitutional_attr]

    return substitutional_objs


data = get_football_test()["handicap"]

data = resolve_links(data, "sport", "bookmaker", "sports")

debug = 1
