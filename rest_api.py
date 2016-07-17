import db_api
import json


def get_sports_list():
    sports = db_api.get_sports_list()
    list_ = []
    for row in sports:
        list_.append(
            {
                "name": row[0],
                "uuid": row[1]
            }
        )
    return json.dumps(list_)


def get_leagues(sport_uuid):
    fix_list = db_api.get_leagues_list(1, sport_uuid)
    select_list = db_api.get_leagues_list(2, sport_uuid, full=True)
    matches = db_api.get_leagues_matches(sport_uuid)

    result = {
        "fix": fix_list,
        "select": select_list,
        "matches": matches
    }


    return json.dumps(result, indent=4)






