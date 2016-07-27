import db_api
import json
from MySQLdb import IntegrityError


def get_sports_select_list():
    sports = db_api.get_sport_select_list()
    list_ = []
    for row in sports:
        list_.append(
            {
                "name": row[0],
                "uuid": row[1]
            }
        )
    return json.dumps(list_)


def get_leagues_select_list(sportuuid):

    sports = db_api.get_leagues_select_list(sportuuid)
    list_ = []
    for row in sports:
        list_.append(
            {
                "name": row[0],
                "uuid": row[1]
            }
        )
    return json.dumps(list_)


def get_participants(leagueuuid):
    fix_list = db_api.get_participants_list(1, leagueuuid)
    select_list = db_api.get_participants_list(2, leagueuuid, full=True)
    matches = db_api.get_participants_matches(leagueuuid)

    result = {
        "fix": fix_list,
        "select": select_list,
        "matches": matches
    }

    return json.dumps(result, indent=4)


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


def get_sports():
    fix_list = db_api.get_sports_list(1)
    select_list = db_api.get_sports_list(2, full=True)
    matches = db_api.get_sports_matches()

    result = {
        "fix": fix_list,
        "select": select_list,
        "matches": matches
    }

    return json.dumps(result, indent=4)


def update_sports(sports):
    try:
        db_api.update_sports(sports)
        return json.dumps(
            {"result": True}
        )
    except IntegrityError:
        return json.dumps(
            {"result": False}
        )


def update_leagues(leagues):
    try:
        db_api.update_leagues(leagues)
        return json.dumps(
            {"result": True}
        )
    except IntegrityError:
        return json.dumps(
            {"result": False}
        )


def update_participants(participants):
    try:
        db_api.update_participants(participants)
        return json.dumps(
            {"result": True}
        )
    except IntegrityError:
        return json.dumps(
            {"result": False}
        )


def get_events(bookmaker_id):
    return json.dumps(db_api.get_events(bookmaker_id))
