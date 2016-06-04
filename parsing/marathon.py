import requests
import bs4


def get_live_football_events():


    i =1
    jsdata = {}  # Будем использовать словарь словарей, листов и строк, чтобы в дальнейшем с легкостью
    #  серилизовать его в JSON

    html_text = requests.get("https://www.marathonbet6.com/su/live/popular").text

    doc = bs4.BeautifulSoup(html_text, "html.parser")  # Создадим Объект для парсинга на основе HTML текста

    jsdata["sport"] = doc.find_all("div", class_="sport-category-label")[0].contents[0].strip()

    events = doc.find_all("tbody")

    jsdata["events"] = []  # В этот список будем класть события

    for event in events:

        event_dict = parse_event(event)

        jsdata["events"].append(event_dict)

    return jsdata


def parse_event(event):

    event_dict = {}

    teams = event.find_all("div", class_="live-today-member-name")

    event_dict["team1"] = teams[0].contents[0].strip()

    event_dict["team2"] = teams[1].contents[0].strip()

    return event_dict


