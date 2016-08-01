import requests
import bs4
import re
from bookmakers.Bookmaker import Bookmaker, GetSportPageException
from requests.exceptions import ConnectTimeout
from settings import LOAD_WAIT_TIME, PROXY


class Marathonbet(Bookmaker):

    bookmaker_id = 2

    bookmaker_name = "marathonbet"

    _timeoutexception = ConnectTimeout

    _default_url = "https://www.marathonplay.com/en/live/26418"

    def _get_page(self, url):
        cookie = {'panbet.sitestyle': 'MULTIMARKETS'}
        proxystring = "http://{0}:{1}@{2}".format(PROXY[1], PROXY[2], PROXY[0])
        proxies = {"http": proxystring, "https": proxystring}
        response = requests.get(url, cookies=cookie, timeout=LOAD_WAIT_TIME, proxies=proxies)
        is_red = str(response.url).__contains__("popular")
        if is_red:
            raise GetSportPageException

        return response.text

    def _scrape_page(self, page):
        try:
            doc = bs4.BeautifulSoup(page, "html.parser")
            a = doc.find("div", class_="sport-category-label")
            new_list_money = []
            new_list_hand = []
            new_list_result2way = []
            def remove_to_win(a):
                return a[:len(a) - 7]

            def coeff(cell):
                q = []
                q = re.split('[,]+', cell)

                for i in range(len(q)):
                    if (q[i].__contains__("epr")):
                        coeff = q[i][7:len(q[i]) - 1]

                return coeff

            def result(cell):
                q = []
                q = re.split('[,]+', cell)
                q[0] = q[0][(q[0].index(':') + 2):(len(q[0]) - 1)]
                result_string = ''

                index = 0
                index1 = 0

                for i in range(len(q)):
                    if (q[i].__contains__("ewc")):
                        index = i

                for i in range(len(q)):
                    if (q[i].__contains__("nm")):
                        index1 = i

                for i in range(index1, index):
                    result_string += q[i] + ' '

                result_string = result_string[(result_string.index(':') + 2):(len(result_string) - 1)]
                result_string = result_string.strip()
                if (result_string[len(result_string) - 1] == '"'):
                    result_string = result_string[:len(result_string) - 1]
                return result_string

            def name(cell):
                q = []
                q = re.split('[,]+', cell)

                for i in range(len(q)):
                    if (q[i].__contains__("mn")):
                        index = i
                for i in range(index - 1):
                    q[0] += q[i + 1] + ' '

                q[0] = q[0][(q[0].index(':') + 2):(len(q[0]) - 1)]

                return q[0]

            def is_empty(a):
                if(len(str(a))>0):
                    return a
                else:
                    return 1

            handicap_list = []
            moneyline = []
            result2way = []

            s = doc.find_all("div", class_="category-container")

            def get_league(x):
                s1 = x.find_all("span", class_="nowrap")
                l = []
                for i in s1:
                    l.append(i.text)

                l1 = ""
                for league in l:
                    l1 = l1 + league
                return l1

            for ev in s:
                spans = []
                spans = ev.find_all("tbody",{"data-event-name":True}, class_="",)

                events = []
                hrefs = []
                odds = []
                data_sel = []
                odds.append([])
                data_sel.append([])
                new_odds = []
                new_odds.append([])
                i = 0
                j = 0
                k = 0
                c = []
                r = []
                n = []
                n.append([])
                r.append([])
                c.append([])

                def coeff(cell):
                    q = []
                    q = re.split('[,]+', cell)

                    for i in range(len(q)):
                        if (q[i].__contains__("epr")):
                            coeff = q[i][7:len(q[i]) - 1]

                    return coeff

                def result(cell):
                    q = []
                    q = re.split('[,]+', cell)
                    q[0] = q[0][(q[0].index(':') + 2):(len(q[0]) - 1)]
                    result_string = ''

                    index = 0
                    index1 = 0

                    for i in range(len(q)):
                        if (q[i].__contains__("ewc")):
                            index = i

                    for i in range(len(q)):
                        if (q[i].__contains__("nm")):
                            index1 = i

                    for i in range(index1, index):
                        result_string += q[i] + ' '

                    result_string = result_string[(result_string.index(':') + 2):(len(result_string) - 1)]
                    result_string = result_string.strip()
                    if (result_string[len(result_string) - 1] == '"'):
                        result_string = result_string[:len(result_string) - 1]
                    return result_string

                def name(cell):
                    q = []
                    q = re.split('[,]+', cell)

                    for i in range(len(q)):
                        if (q[i].__contains__("mn")):
                            index = i
                    for i in range(index - 1):
                        q[0] += q[i + 1] + ' '

                    q[0] = q[0][(q[0].index(':') + 2):(len(q[0]) - 1)]

                    return q[0]

                for span in spans:

                    events.append(span['data-event-name'])
                    hrefs.append(span['data-event-treeid'])

                    odds[i] = span.find_all("td", {"data-market-type": True, "data-sel": True},
                                            {'class': lambda x: x
                                                                and 'price' in x.split()

                                             }
                                            )

                    if (i < len(spans) - 1):
                        odds.append([])
                    i += 1

                for odd in odds:
                    for od in odd:
                        data_sel[j].append(od['data-sel'].strip())
                        new_odds[k].append(od['data-market-type'].strip())

                        c[j].append(coeff(od['data-sel'].strip()))
                        r[j].append(result(od['data-sel'].strip()))
                        n[j].append(name(od['data-sel'].strip()))

                    if (j < len(spans) - 1):
                        data_sel.append([])
                        new_odds.append([])
                        c.append([])
                        r.append([])
                        n.append([])
                    j += 1
                    k += 1

                def get_handicap(index_of_hand, index_of_hand1, m):

                    handicap = {}

                    handicap["firstforward"] = get_forward_string(str(n[m][index_of_hand]))
                    handicap["sport"] = str(a.text).title().strip()
                    handicap["firstparticipant"] = get_part_string(str(n[m][index_of_hand])).strip()

                    handicap["secondforward"] = get_forward_string(n[m][index_of_hand1])
                    handicap["league"] = get_league(ev).strip()
                    handicap["secondparticipant"] = get_part_string(str(n[m][index_of_hand1])).strip()
                    handicap["firstwin"] = round(float(c[m][index_of_hand]),2)

                    handicap["secondwin"] = round(float(c[m][index_of_hand1]),2)
                    handicap["live"] = True
                    handicap["href"] = "/en/live/" + str(hrefs[m])
                    return handicap

                def get_pairs_of_participants_handicap():
                    pairs = []
                    pairs.append([])
                    m = 0

                    for odds_ in new_odds:
                        s = 0
                        for odd_ in odds_:

                            if ((str(odd_) == 'HANDICAP')):
                                pairs[m].append(s)
                                pairs[m].append(s + 1)
                                break
                            else:
                                s += 1
                        if (m < len(spans) - 1):
                            pairs.append([])
                        m += 1
                    return pairs

                def get_list_of_hand():
                    d = {}
                    list = []
                    pairs = get_pairs_of_participants_handicap()
                    s = 0
                    for pair in pairs:
                        if (len(pair) > 1):
                            list.append(get_handicap(pair[0], pair[1], s))
                            s += 1
                        else:
                            s += 1

                    d["handicap"] = list
                    return d

                def get_result2way(index_of_hand, index_of_hand1, m):

                    result2way = {}

                    if (str(a.text).title() == "Basketball"):
                        result2way["firstparticipant"] = get_part_string(str(n[m][index_of_hand])).strip()
                        result2way["secondparticipant"] = get_part_string(str(n[m][index_of_hand1])).strip()
                    else:
                        result2way["firstparticipant"] = remove_to_win(get_part_string(str(n[m][index_of_hand]))).strip()
                        result2way["secondparticipant"] = remove_to_win(get_part_string(str(n[m][index_of_hand1]))).strip()
                    result2way["draw"] = None
                    result2way["sport"] = str(a.text).title().strip()
                    result2way["firstwin"] = round(float(c[m][index_of_hand]),2)
                    result2way["league"] = get_league(ev).strip()
                    result2way["secondwin"] = round(float(c[m][index_of_hand1]),2)
                    result2way["live"] = True
                    result2way["href"] = "/en/live/" + str(hrefs[m])
                    return result2way

                def get_pairs_of_participants_result2way():
                    pairs = []
                    pairs.append([])
                    m = 0

                    for odds_ in new_odds:
                        s = 0
                        for odd_ in odds_:

                            if ((str(odd_) == "RESULT_2WAY")):
                                pairs[m].append(s)
                                pairs[m].append(s + 1)
                                break
                            else:
                                s += 1
                        if (m < len(spans) - 1):
                            pairs.append([])
                        m += 1
                    return pairs

                def get_list_of_result2way():
                    d = {}
                    list = []
                    pairs = get_pairs_of_participants_result2way()
                    s = 0
                    for pair in pairs:
                        if (len(pair) > 1):
                            list.append(get_result2way(pair[0], pair[1], s))
                            s += 1
                        else:
                            s += 1

                    d["result2way"] = list
                    return d

                def get_moneyline(index_of_hand, index_of_hand1, index_of_draw, m):

                    moneyline = {}

                    moneyline["firstparticipant"] = remove_to_win(get_part_string(str(n[m][index_of_hand]))).strip()

                    moneyline["sport"] = "Football"

                    moneyline["secondparticipant"] = remove_to_win(get_part_string(str(n[m][index_of_hand1]))).strip()
                    moneyline["firstwin"] = is_empty(round(float(c[m][index_of_hand]),2))
                    moneyline["league"] = get_league(ev).strip()
                    moneyline["secondwin"] = is_empty(round(float(c[m][index_of_hand1]),2))
                    moneyline["draw"] = round(float(c[m][index_of_draw]),2)
                    moneyline["live"] = True
                    moneyline["href"] = "/en/live/" + str(hrefs[m])
                    return moneyline

                def get_pairs_of_participants_moneyline():
                    pairs = []
                    pairs.append([])
                    m = 0

                    for odds_ in new_odds:
                        s = 0
                        for odd_ in odds_:

                            if ((str(odd_) == 'RESULT')):
                                pairs[m].append(s)
                                pairs[m].append(s + 1)
                                pairs[m].append(s + 2)
                                break
                            else:
                                s += 1
                        if (m < len(spans) - 1):
                            pairs.append([])
                        m += 1
                    return pairs

                def get_list_of_moneyline():
                    d = {}
                    list = []
                    pairs = get_pairs_of_participants_moneyline()
                    s = 0
                    for pair in pairs:
                        if (len(pair) > 2):
                            list.append(get_moneyline(pair[0], pair[2], pair[1], s))
                            s += 1
                        else:
                            s += 1

                    d["moneyline"] = list
                    return d


                def is_forward_zero(a):
                    if (str(a).find("(") == -1):
                        return 0
                    else:
                        return 1

                def get_forward_string(a):
                    if (is_forward_zero(a) == 0):
                        return 0
                    else:
                        return str(a[int(a.rfind("(") + 1):int(str(a.rfind(")")))].strip())


                def get_part_string(a):
                    if (is_forward_zero(a) == 0)or(a.__contains__("Doubles")):
                        return a
                    else:
                        return str(a[:int(str(a.index("(")))].strip())

                def unite_dict(dict1, dict2):
                    dict1.update(dict2)
                    return dict1

                if (a.text == "Football")or(a.text == "football"):
                    moneyline.append(get_list_of_moneyline()["moneyline"])
                    handicap_list.append(get_list_of_hand()["handicap"])


                else:
                    result2way.append(get_list_of_result2way()["result2way"])
                    handicap_list.append(get_list_of_hand()["handicap"])

            d = {}
            if (a.text == "Football") or (a.text == "football"):
                for inner_list in moneyline:
                    if (len(inner_list) > 0):
                        new_list_money.append(inner_list[0])

                for inner_list in handicap_list:
                    if (len(inner_list) > 0):
                        new_list_hand.append(inner_list[0])

                d["handicap"] = new_list_hand
                d["moneyline"] = new_list_money
            else:
                for inner_list in handicap_list:
                    if (len(inner_list) > 0):
                        new_list_hand.append(inner_list[0])

                for inner_list in result2way:
                    if (len(inner_list) > 0):
                        new_list_result2way.append(inner_list[0])

                d["handicap"] = new_list_hand
                d["moneyline"] = new_list_result2way

            return d
        except GetSportPageException:
            d = {}
            d["handicap"] = []
            d["moneyline"] = []
            return d

    def get_scraping_urls(self):
        return ["https://www.marathonbet.com/en/live/26418",
                "https://www.marathonbet.com/en/live/45356",
                "https://www.marathonbet.com/en/live/22723",
                "https://www.marathonbet.com/en/live/120866"
                ]
    def get_scraping_urls1(self):
        return ["https://www.marathonbet.com/en/live/26418",
                "https://www.marathonbet.com/en/live/45356",
                "https://www.marathonbet.com/en/live/22723",

                ]