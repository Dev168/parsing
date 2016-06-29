from bookmakers.Bookmaker import Bookmaker
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from settings import PROXY, LOAD_WAIT_TIME
import bs4
import re
import sys


class Sbobet(Bookmaker):

    bookmaker_id = 1

    bookmaker_name = "sbobet"

    _timeoutexception = TimeoutException

    _default_url = "https://www.sbobet.com/euro/football"

    def _get_page(self, url):

        service_args = [
            '--proxy={0}'.format(PROXY[0]),
            '--proxy-type=http',
            '--proxy-auth={0}:{1}'.format(PROXY[1], PROXY[2])
        ]

        driver = webdriver.PhantomJS(service_args=service_args)

        driver.set_page_load_timeout(LOAD_WAIT_TIME)

        driver.get(url)

        page = driver.page_source

        driver.close()

        return page

    def _scrape_page(self, page):

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
                diff = score1 - score2

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

            game["firstforward"] -= diff

            game["secondforward"] += diff

            game["secondparticipant"] = columns[3].find("span", class_="OddsL").contents[0].strip()

            game["secondwin"] = columns[3].find("span", class_="OddsR").contents[0].strip()

            game["href"] = columns[4].a["href"]

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

        return {"vs": vs, "handicap": handicap}
