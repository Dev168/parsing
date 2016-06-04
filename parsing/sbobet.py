import bs4
from selenium import webdriver
from settings import PROXY
import sys
import os
from datetime import datetime
import re


def events(url="https://www.sbobet.com/euro/football"):

    def scrap_vs(game_tag, game):

        spans = game_tag.find("div", class_="DateTimeTxt").find_all("span")
        if game["live"]:
            game["score"] = spans[0].contents[0].strip()
            game["livedate"] = spans[1].font.contents[0].strip()
            game["oddsdate"] = None
            game["gamedate"] = None
        else:
            game["score"] = None
            game["livedate"] = None
            game["oddsdate"] = None
            game["gamedate"] = spans[0].contents[0].strip() + " " + spans[1].contents[0].strip()

        columns = list(game_tag.children)

        game["firstparticipant"] = columns[2].find("span", class_="OddsL").contents[0].strip()

        game["firstwin"] = columns[2].find("span", class_="OddsR").contents[0].strip()

        game["secondparticipant"] = columns[4].find("span", class_="OddsL").contents[0].strip()

        game["secondwin"] = columns[4].find("span", class_="OddsR").contents[0].strip()

        game["draw"] = columns[3].find("span", class_="OddsR").contents[0].strip()

        game["href"] = columns[5].a["href"]

    def scrap_handicap(game_tag, game):
        spans = game_tag.find("div", class_="DateTimeTxt").find_all("span")
        if game["live"]:
            game["score"] = spans[0].contents[0].strip()
            game["livedate"] = spans[1].font.contents[0].strip()
            game["oddsdate"] = None
            game["gamedate"] = None
        else:
            game["score"] = None
            game["livedate"] = None
            game["oddsdate"] = None
            game["gamedate"] = spans[0].contents[0].strip() + " " + spans[1].contents[0].strip()

        columns = list(game_tag.children)

        game["firstparticipant"] = columns[2].find("span", class_="OddsL").contents[0].strip()

        game["firstwin"] = columns[2].find("span", class_="OddsR").contents[0].strip()

        game["firstforward"] = columns[2].find("span", class_="OddsM").contents[0].strip()

        game["secondparticipant"] = columns[3].find("span", class_="OddsL").contents[0].strip()

        game["secondwin"] = columns[3].find("span", class_="OddsR").contents[0].strip()

        game["secondforward"] = columns[3].find("span", class_="OddsM").contents[0].strip()

        game["href"] = columns[4].a["href"]

    page = get_page(url)

    try:

        vs = []

        handicap = []

        doc = bs4.BeautifulSoup(page, "html.parser")

        panel_odds_display = doc.find(id="panel-odds-display")

        panels = panel_odds_display.find_all(class_="Panel")

        for panel in panels:

            sport = panel.find("div", class_="HdTitle").contents[0].strip()

            markets = panel.find_all("div", class_=lambda x: x in ["LiveMarket", "NonLiveMarket"])

            for market in markets:

                live = "LiveMarket" in market["class"]

                for odds_type_tag in market.childGenerator():

                    odds_type = odds_type_tag.span.contents[0].strip()

                    scrap_func = scrap_handicap  # Функция которая будет парсить строчку с матчем
                    data = handicap

                    if odds_type == "1X2":  # Если тип ставки - 1х2, то меняем функцию обработки
                                            # строчки с матчем (т.к. различается)
                        scrap_func = scrap_vs
                        data = vs

                    leagues = odds_type_tag.find_all("div", class_="MarketLea")

                    for league in leagues:

                        league_name = league.find("div", class_="SubHeadT").contents[0].strip()

                        table = league.nextSibling

                        game_tags = table.find_all("tr")

                        for game_tag in game_tags:

                            if "class" in game_tag.attrs and game_tag["class"] == "OddsClosed":
                                continue

                            game = {"sport": sport, "league": league_name, "live": live}

                            scrap_func(game_tag, game)

                            data.append(game)

        return {"vs": vs, "handicap": handicap}


    except IndexError:
        _debug_log(page, sys.exc_info())
        return {}


def sports():

    page = get_page("https://www.sbobet.com/euro")

    try:
        data = _parse_sports(page)
        return data
    except:
        _debug_log(page, sys.exc_info())
        return {}




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


def _parse_sports(page):

    data = []

    doc = bs4.BeautifulSoup(page, "html.parser")

    sports = doc.find_all(id=re.compile("bu:ms:all-sp:[0-9]*"))

    for sport in sports:

        sport_dict = {"name": sport.contents[1].strip(), "href": sport["href"]}

        data.append(sport_dict)

    res = list(map(lambda el: {'name': el['name'], 'href': "https://www.sbobet.com/euro" + el['href']}, data))

    return res


def _debug_log(page, info):
    dname = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dpath = "parsing/sbobet_logs/{0}".format(dname)
    os.makedirs(dpath)

    with open(dpath+"/page.html", "w+", encoding="utf8") as f:
        f.write(page)

    with open(dpath+"/log.txt", "w+", encoding="utf8") as f:
        f.write(info)
