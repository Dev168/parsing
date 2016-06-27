import bs4
from selenium import webdriver
from settings import PROXY
import sys
import os
from datetime import datetime
import re
import json
import linecache


def live_handicaps(url="https://www.sbobet.com/euro/football"):
    return events(url)["handicap"]


def events(url="https://www.sbobet.com/euro/football", debug_page=None):

    def scrap_vs(game_tag, game):

        spans = game_tag.find("div", class_="DateTimeTxt").find_all("span")
        if game["live"]:
            game["score"] = spans[0].contents[0].strip()
            if type(spans[1].contents[0]) == str:
                game["livedate"] = spans[1].font.contents[0].strip()
            else:
                game["livedate"] = ""
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

        diff = 0
        score1 = 0
        score2 = 0

        if game["live"]:
            game["score"] = spans[0].contents[0].strip()

            res = re.findall("[0-9]+", game["score"])
            score1 = float(res[0])
            score2 = float(res[1])
            diff = abs(score1-score2)

            if type(spans[1].contents[0]) == str:
                game["livedate"] = spans[1].font.contents[0].strip()
            else:
                game["livedate"] = ""
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

        game["firstforward"] = float(columns[2].find("span", class_="OddsM").contents[0].strip())

        game["secondforward"] = float(columns[3].find("span", class_="OddsM").contents[0].strip())

        if diff != 0:
            if game["firstforward"] == 0:
                if score1 > 0:
                    game["firstforward"] -= diff
                    game["secondforward"] += diff
                else:
                    game["firstforward"] += diff
                    game["secondforward"] -= diff
            elif game["firstforward"] > 0:
                game["firstforward"] += diff
                game["secondforward"] -= diff
            else:
                game["firstforward"] -= diff
                game["firstforward"] += diff

        game["secondparticipant"] = columns[3].find("span", class_="OddsL").contents[0].strip()

        game["secondwin"] = columns[3].find("span", class_="OddsR").contents[0].strip()

        game["href"] = columns[4].a["href"]

    if debug_page is None:
        page = get_page(url)
    else:
        page = debug_page

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

                            if "class" in game_tag.attrs and "OddsClosed" in game_tag["class"]:
                                continue

                            game = {"sport": sport, "league": league_name, "live": live}

                            scrap_func(game_tag, game)

                            if live:
                                data.append(game)

        print("Данные успешно загружены")

        return {"vs": vs, "handicap": handicap}

    except (IndexError, AttributeError, Exception):
        print("При загрузке данных с сайта произошли ошибки")
        _debug_log(page, sys.exc_info())
        return {}


def bookmaker_id():
    return 1


def bookmaker_name():
    return "sbobet"


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
    dpath = "scraping/sbobet_logs/{0}".format(dname)
    os.makedirs(dpath)

    with open(dpath+"/page.html", "w+", encoding="utf8") as f:
        f.write(page)

    game = json.dumps(info[2].tb_frame.f_locals["game"], indent=4)

    with open(dpath + "/f_locals.json", "w+", encoding="utf8") as f:
        f.write(game)

    with open(dpath + "/line_error.txt", "w+", encoding="utf8") as fl:
        exc_type, exc_obj, tb = info
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        text = 'EXCEPTION IN ({0}, LINE {1} "{2}"): {3}'.format(filename, lineno, line.strip(), exc_obj)
        fl.write(text)

    raise Exception
