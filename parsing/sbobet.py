import bs4
from selenium import webdriver
from settings import PROXY
import sys
import os
from datetime import datetime
import re


def football_events():

    page = get_page("https://www.sbobet.com/euro/football")

    try:
        data = _parse_sport_page(page)
    except:
        _debug_log(page, sys.exc_info())

    return data


def sports():

    page = get_page("https://www.sbobet.com/euro")

    try:
        data = _parse_sports(page)
    except:
        _debug_log(page, sys.exc_info())

    return data


def _parse_ligue(ligue):

    table = ligue.next_sibling()[0]

    children = table.children

    games = [node for node in children]

    games_data = []

    for game in games:

        game_data = {"OddsClosed": False,
                     "Teams": ["team1", "team2"],
                     "Coffs": None,
                     "href": None}

        if "class" in game:
            if "OddsClosed" in game["class"]:
                game_data["OddsClosed"] = True

        teams = game.find_all("span", class_="OddsL")

        game_data["Teams"][0] = teams[0].contents[0].strip()
        game_data["Teams"][1] = teams[2].contents[0].strip()

        if not game_data["OddsClosed"]:

            game.find_all("a", class_="IconMarkets")[0]["href"]

            coffs = game.find_all("span", class_="OddsR")
            coffs_data = [0, 0, 0]

            coffs_data[0] = coffs[0].contents[0].strip()
            coffs_data[1] = coffs[1].contents[0].strip()
            coffs_data[2] = coffs[2].contents[0].strip()

            game_data["Coffs"] = coffs_data

        games_data.append(game_data)

    return games_data


def _parse_sport_page(page):

    bs = bs4.BeautifulSoup(page, "html.parser")

    market = bs.find_all("div", class_="MarketBd")[0]

    ligues = market.find_all("div", class_="MarketLea")

    ligues_data = []

    for ligue in ligues:
        ligue_name = ligue.find_all("div", class_="SubHeadT")[0].contents[0].strip()

        ligue_data = {ligue_name: _parse_ligue(ligue)}

        ligues_data.append(ligue_data)

    return {"football": ligues_data, "BookmakerName": "sbobet"}


def _parse_sports(page):

    data = []

    doc = bs4.BeautifulSoup(page, "html.parser")

    sports = doc.find_all(id=re.compile("bu:ms:all-sp:[0-9]*"))

    for sport in sports:

        sport_dict = {"name": sport.contents[1].strip(), "href": sport["href"]}

        data.append(sport_dict)

    res = list(map(lambda el: {'name': el['name'], 'href': "https://www.sbobet.com/euro" + el['href']}, data))

    return res


def get_page(url):

    service_args = [
        '--proxy={0}'.format(PROXY[0]),
        '--proxy-type=http',
        '--proxy-auth={0}:{1}'.format(PROXY[1], PROXY[2])
    ]

    driver = webdriver.PhantomJS(service_args=service_args)

    driver.get(url)

    page = driver.page_source

    driver.close()

    return page


def _debug_log(page, info):
    dname = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dpath = "parsing/sbobet_logs/{0}".format(dname)
    os.makedirs(dpath)

    with open(dpath+"/page.html", "w+", "utf8") as f:
        f.write(page)

    with open(dpath+"/log.txt", "w+", "utf8") as f:
        f.write(info)



