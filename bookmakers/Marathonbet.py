import requests
import bs4
import re
from bookmakers.Bookmaker import Bookmaker
from requests.exceptions import ConnectTimeout
from settings import LOAD_WAIT_TIME, PROXY


class Marathonbet(Bookmaker):

    bookmaker_id = 2

    bookmaker_name = "marathonbet"

    _timeoutexception = ConnectTimeout

    _default_url = "https://www.marafonsportsbook.com/en/live/26418"

    def _get_page(self, url):
        cookie = {'panbet.sitestyle': 'MULTIMARKETS'}
        proxystring = "http://{0}:{1}@{2}".format(PROXY[1], PROXY[2], PROXY[0])
        proxies = {"http": proxystring, "https": proxystring}
        return requests.get(url, cookies=cookie, timeout=LOAD_WAIT_TIME, proxies=proxies).text

    def _scrape_page(self, page):
        doc = bs4.BeautifulSoup(page, "html.parser")
        spans = doc.find_all("tbody", class_="")

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

            odds[i] = span.find_all("td",
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

            handicap["firstparticipant"] = get_part_string(str(n[m][index_of_hand]))
            handicap["sport"] = "football"
            handicap["secondforward"] = get_forward_string(n[m][index_of_hand1])

            handicap["secondparticipant"] = get_part_string(str(n[m][index_of_hand1]))
            handicap["firstwin"] = c[m][index_of_hand]

            handicap["secondwin"] = c[m][index_of_hand1]
            handicap["live"] = True
            handicap["href"] = "/en/live/animation/" + str(hrefs[m])
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

        def is_forward_zero(a):
            if (str(a).find("(") == -1):
                return 0
            else:
                return 1

        def get_forward_string(a):
            if (is_forward_zero(a) == 0):
                return 0
            else:
                return str(a[int(a.index("(") + 1):int(str(a.index(")")))].strip())

        def get_part_string(a):
            if (is_forward_zero(a) == 0):
                return a
            else:
                return str(a[:int(str(a.index("(")))].strip())

        return get_list_of_hand()

    def get_scraping_urls(self):
        return ["https://www.marathonbet.com/en/live/26418",
                ]