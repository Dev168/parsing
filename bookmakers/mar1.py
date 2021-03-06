import requests
import bs4
import re
import sys
import os
from datetime import datetime
from multiprocessing import Process
from time import sleep


def events(url="https://www.marathonbet9.com/ru/live/popular"):

    html_text = requests.get(url).text

    doc = bs4.BeautifulSoup(html_text, "html.parser")



    #price height-column-with-price first-in-main-row


    events = []
    odd  =  [] # тип события
    cell = []
    hrefs = []
    href = []
    team =[]
    hrefs = doc.find_all("tr", class_="broadcasts-menu-container-tr all-regions")

    for i in range(len(hrefs)):
        href.append(hrefs[i].a['href'])

    teams = doc.find_all("div", class_="live-today-member-name")
    odds =doc.find_all("td",
                       {'class': lambda x: x
                                           and 'price' in x.split()
                        }
                       )
    names = doc.find_all("tbody",class_="")

    for i in range(len(odds)):
        try:
            odd.append(odds[i]['data-market-type'].strip())
        except:
            pass
        finally:
            pass
        cell.append(odds[i]['data-sel'].strip())

    for i in range(len(names)):
        try:
            events.append(names[i]['data-event-name'].strip())
        except:
            pass
        finally:
            pass

    for i in range(len(teams)):
        team.append(teams[i].contents[0].strip())





    def coeff(cell):
        q=[]
        q = re.split('[,]+', cell)



        for i in range(len(q)):
            if (q[i].__contains__("epr")):
                coeff = q[i][7:len(q[i])-1]

        return coeff
    def result(cell):
        q=[]
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

        for i in range(index1,index):
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
            q[0] += q[i  + 1 ] + ' '

        q[0] = q[0][(q[0].index(':') + 2):(len(q[0]) - 1)]


        return q[0]

    def Convert(cell):
        d = dict.fromkeys(['coeffs', 'res','name'])
        c = []
        r = []
        n = []
        for i in range(len(cell)):
            c.append(coeff(cell[i]))
            r.append(result(cell[i]))
            n.append(name(cell[i]))
        d["coeffs"] = c
        d["res"] = r
        d["name"] = n
        return d

    def get_url(team1, team2):
        for i in range(len(events)):
            if ((str(events[i]).find(team1) != -1) and (str(events[i]).find(team2) != -1)):
                return href[i]

    uniq_odds = []

    for o in  odd:
        if(uniq_odds.__contains__(o)==0):
            uniq_odds.append(o)




    def get_handicap(index_of_hand,index_of_hand1):


        handicap = {}
        handicap["firstforward"] = str(Convert(cell)['name'][index_of_hand])[str(Convert(cell)['name'][index_of_hand]).index("(")+1:str(Convert(cell)['name'][index_of_hand]).index(")")].strip()
        handicap["firstparticipant"] = str(Convert(cell)['name'][index_of_hand])[:str(Convert(cell)['name'][index_of_hand]).index("(")].strip()
        handicap["firstwin"] = Convert(cell)['coeffs'][index_of_hand]
        handicap["secondforward"] = str(Convert(cell)['name'][index_of_hand1])[str(Convert(cell)['name'][index_of_hand1]).index("(")+1:str(Convert(cell)['name'][index_of_hand1]).index(")")].strip()
        handicap["secondparticipant"] = str(Convert(cell)['name'][index_of_hand1])[:str(Convert(cell)['name'][index_of_hand1]).index("(")].strip()
        handicap["secondwin"] = Convert(cell)['coeffs'][index_of_hand1]
        handicap["href"] = get_url(str(Convert(cell)['name'][index_of_hand])[:str(Convert(cell)['name'][index_of_hand]).index("(")].strip(),str(Convert(cell)['name'][index_of_hand1])[:str(Convert(cell)['name'][index_of_hand1]).index("(")].strip())
        return handicap
    def get_pairs_of_participants_handicap():
        pairs = []
        uniq_pairs = []

        for j in range(len(events)):
            for i in range(len(Convert(cell)['name'])-1):
                if((str(odd[i])=='HANDICAP')and(str(odd[i+1])=='HANDICAP')):
                    if (str(events[j]).find(str(Convert(cell)['name'][i])[str(Convert(cell)['name'][i]).index("(")+1:str(Convert(cell)['name'][i]).index(")")].strip())!=1)and(str(events[j]).find(str(Convert(cell)['name'][i+1])[str(Convert(cell)['name'][i+1]).index("(")+1:str(Convert(cell)['name'][i+1]).index(")")].strip())!=1):
                        pairs.append(i)
                        pairs.append(i + 1)
                    else:
                        pass
        for o in pairs:
            if (uniq_pairs.__contains__(o) == 0):
                uniq_pairs.append(o)
        return uniq_pairs
    def get_list_of_hand():
        d = {}
        list = []
        pairs = []
        pairs = get_pairs_of_participants_handicap()
        for i in range(int(len(pairs)/2)):
            list.append(get_handicap(pairs[i*2],pairs[i*2+1]))


        d["handicap"] = list
        return  d


    def get_moneyline(index_of_hand,index_of_hand1,index_of_draw):
        moneyline = {}


        moneyline["firstparticipant"] = str(Convert(cell)['name'][index_of_hand])[
                                       :str(Convert(cell)['name'][index_of_hand]).index("(")].strip()
        moneyline["firstwin"] = Convert(cell)['coeffs'][index_of_hand]
        moneyline["href"] = None

        moneyline["secondparticipant"] = str(Convert(cell)['name'][index_of_hand1])[
                                        :str(Convert(cell)['name'][index_of_hand1]).index("(")].strip()
        moneyline["secondwin"] = Convert(cell)['coeffs'][index_of_hand1]
        moneyline["draw"] =Convert(cell)['coeffs'][index_of_draw]
        return moneyline
    def get_moneylinde_index():
        pairs = []
        uniq_pairs = []
        for j in range(len(events)):
            for i in range(len(Convert(cell)['name'])-2):
                if ((str(odd[i])=="RESULT") and (str(odd[i + 1])=="RESULT")and (str(odd[i + 2]) == "RESULT")):
                    if ((str(events[j]).find(str(Convert(cell)['name'][i])[str(Convert(cell)['name'][i]).index("(") + 1:str(
                            Convert(cell)['name'][i]).index(")")].strip()) != 1) and (str(events[j]).find(
                            str(Convert(cell)['name'][i + 2])[
                            str(Convert(cell)['name'][i + 2]).index("(") + 1:str(Convert(cell)['name'][i + 2]).index(
                                    ")")].strip()) != 1) and (str(Convert(cell)['name'][i + 1]).find("ничья")!=1)


                        ):
                        pairs.append(i)
                        pairs.append(i+1)
                        pairs.append(i + 2)
                    else:
                        pass
        for o in pairs:
            if (uniq_pairs.__contains__(o) == 0):
                uniq_pairs.append(o)
        return uniq_pairs
    def get_list_of_money():
        d = {}
        list = []
        pairs = []
        pairs = get_moneylinde_index()
        for i in range(int(len(pairs)/3)):
            list.append(get_moneyline(pairs[3*i],pairs[3*i+2],pairs[3*i+1]))


        d["vs"] = list
        return  d





    def get_result2way(index_of_hand, index_of_hand1):
        moneyline = {}

        moneyline["firstparticipant"] = remove_brackets(str(Convert(cell)['name'][index_of_hand]))
        moneyline["firstwin"] = Convert(cell)['coeffs'][index_of_hand]
        moneyline["href"] = None

        moneyline["secondparticipant"] = remove_brackets(str(Convert(cell)['name'][index_of_hand1]))
        moneyline["secondwin"] = Convert(cell)['coeffs'][index_of_hand1]
        return moneyline
    def get_result2way_index():
        pairs = []
        uniq_pairs = []
        for j in range(len(events)):
            for i in range(len(Convert(cell)['name'])-1):
                if ((str(odd[i]) == "RESULT_2WAY") and (str(odd[i + 1]) == "RESULT_2WAY")):
                    if (
                                (str(events[j]).find(remove_brackets(str(Convert(cell)['name'][i]) != 1)))

                            and (str(events[j]).find(remove_brackets(str(Convert(cell)['name'][i + 1] != 1))))
                    ):
                        pairs.append(i)
                        pairs.append(i + 1)

                    else:
                        pass
        for o in pairs:
            if (uniq_pairs.__contains__(o) == 0):
                uniq_pairs.append(o)
        return uniq_pairs
    def get_list_of_result2way():
        d = {}
        list = []
        pairs = []
        pairs = get_result2way_index()
        for i in range(int(len(pairs) / 2)):
            list.append(get_result2way(pairs[2 * i], pairs[2 * i + 1]))

        d["result_2way"] = list
        return d
    def remove_brackets(a):
        if (str(a).find('(') == -1):
            return str(a)
        else:
            return str(str(a)[:str(a).index("(")]).strip()

    def get_chance(index_of_hand, index_of_hand2, index_of_hand1):
        moneyline = {}

        moneyline["firstparticipant"] = remove_brackets(str(Convert(cell)['name'][index_of_hand]))
        moneyline["firstwin"] = Convert(cell)['coeffs'][index_of_hand]
        moneyline["href"] = None

        moneyline["secondparticipant"] = remove_brackets(str(Convert(cell)['name'][index_of_hand1]))
        moneyline["secondwin"] = Convert(cell)['coeffs'][index_of_hand1]

        moneyline["1or2"] = Convert(cell)['coeffs'][index_of_hand2]

        return moneyline

    def get_chance_index():
        pairs = []
        uniq_pairs = []
        for j in range(len(events)):
            for i in range(len(Convert(cell)['name'])-2):
                if ((str(odd[i]) == "DOUBLE_CHANCE") and (str(odd[i + 1]) == "DOUBLE_CHANCE") and (
                    str(odd[i + 2]) == "DOUBLE_CHANCE")):
                    if (
                                (str(events[j]).find(remove_brackets(str(Convert(cell)['name'][i]) != 1)))

                            and (str(events[j]).find(remove_brackets(str(Convert(cell)['name'][i + 2] != 1))))
                    ):
                        pairs.append(i)
                        pairs.append(i + 1)
                        pairs.append(i + 2)
                    else:
                        pass
        for o in pairs:
            if (uniq_pairs.__contains__(o) == 0):
                uniq_pairs.append(o)
        return uniq_pairs

    def get_list_of_chance():
        d = {}
        list = []
        pairs = []
        pairs = get_chance_index()
        for i in range(int(len(pairs) / 3)):
            list.append(get_chance(pairs[3 * i], pairs[3 * i + 1], pairs[3 * i + 2]))

        d["double_chance"] = list
        return d





    def unite_dict(dict1,dict2,dict3,dict4):
        dict1.update(dict2)
        dict1.update(dict3)
        dict1.update(dict4)
        return dict1


    return unite_dict(get_list_of_hand(),get_list_of_money(),get_list_of_result2way(),get_list_of_chance())



def bookmaker_id():
    return 2

"""DEPRICATED"""
def bookmaker_name():
    return "marathonbet"




#football
def football(url="https://www.marafonbet.info/en/live/26418"):
    url1 = "https://www.marathonplay.com/en/live/26418"

    cookie = {'panbet.sitestyle': 'MULTIMARKETS'}
    html_text = requests.get(url1, cookies=cookie).text
    doc = bs4.BeautifulSoup(html_text, "html.parser")

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

    handicap_list = []
    moneyline = []

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
        spans = ev.find_all("tbody", class_="")

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
            handicap["league"] = get_league(ev)
            handicap["secondwin"] = c[m][index_of_hand1]
            handicap["live"] = True
            handicap["href"] = "https://www.sportsbookmarafonbet.com/en/live/animation/" + str(hrefs[m])
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

        def get_moneyline(index_of_hand, index_of_hand1, index_of_draw, m):

            moneyline = {}

            moneyline["firstparticipant"] = remove_to_win(get_part_string(str(n[m][index_of_hand])))

            moneyline["sport"] = "football"

            moneyline["secondparticipant"] = remove_to_win(get_part_string(str(n[m][index_of_hand1])))
            moneyline["firstwin"] = c[m][index_of_hand]
            moneyline["league"] = get_league(ev)
            moneyline["secondwin"] = c[m][index_of_hand1]
            moneyline["draw"] = c[m][index_of_draw]
            moneyline["live"] = True
            moneyline["href"] = "https://www.marafonsportsbook.com/en/live/animation/" + str(hrefs[m])
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
                return str(a[int(a.index("(") + 1):int(str(a.index(")")))].strip())

        def get_part_string(a):
            if (is_forward_zero(a) == 0):
                return a
            else:
                return str(a[:int(str(a.index("(")))].strip())

        handicap_list.append(get_list_of_hand()["handicap"])
        moneyline.append(get_list_of_moneyline()["moneyline"])

    d = {}
    d["handicap"] = handicap_list
    d["moneyline"] = moneyline
    return d
def tennis(url="https://www.marafonbet.info/en/live/22723"):

    path = "bookmakers/er.html"
    h = open(path)
    url1 = "https://www.marathonplay.com/en/live/22723"

    cookie = {'panbet.sitestyle': 'MULTIMARKETS'}
    html_text = h.read()
    doc = bs4.BeautifulSoup(html_text, "html.parser")

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

    def remove_to_win(a):
        return a[:len(a) - 7]



    handicap_list = []
    moneyline = []

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
        spans = ev.find_all("tbody", class_="")
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
            handicap["sport"] = "tennis"
            handicap["firstforward"] = get_forward_string(str(n[m][index_of_hand]))

            handicap["firstparticipant"] = get_part_string(str(n[m][index_of_hand]))

            handicap["secondforward"] = get_forward_string(n[m][index_of_hand1])
            handicap["league"] = get_league(ev)
            handicap["secondparticipant"] = get_part_string(str(n[m][index_of_hand1]))
            handicap["firstwin"] = round(float(c[m][index_of_hand]),2)

            handicap["secondwin"] = round(float(c[m][index_of_hand1]),2)
            handicap["live"] = True
            handicap["href"] = "https://www.marafonsportsbook.com/en/live/animation/" + str(hrefs[m])
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

            result2way["firstparticipant"] = remove_to_win(get_part_string(str(n[m][index_of_hand])))
            result2way["sport"] = "tennis"
            result2way["secondparticipant"] = remove_to_win(get_part_string(str(n[m][index_of_hand1])))
            result2way["firstwin"] = c[m][index_of_hand]
            result2way["league"] = get_league(ev)
            result2way["secondwin"] = c[m][index_of_hand1]
            result2way["live"] = True
            result2way["href"] = "https://www.marafonsportsbook.com/en/live/animation/" + str(hrefs[m])
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
        handicap_list.append(get_list_of_hand()["handicap"])
        moneyline.append(get_list_of_result2way()["result2way"])

    d = {}
    d["handicap"] = handicap_list
    d["result_2way"] = moneyline
    return d
def baseball(url="https://www.marafonbet.info/en/live/120866"):

    url1 = "https://www.marathonplay.com/en/live/120866"

    cookie = {'panbet.sitestyle': 'MULTIMARKETS'}

    respose = requests.get(url1, cookies=cookie)
    html_text = respose.text
    if(respose.links['canonical']['url'].__contains__("popular") == True):
        return {}
    else:

        doc = bs4.BeautifulSoup(html_text, "html.parser")

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

        def remove_to_win(a):
            return a[:len(a) - 7]



        handicap_list = []
        moneyline = []

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
            spans = ev.find_all("tbody", class_="")
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
                handicap["sport"] = "baseball"
                handicap["firstparticipant"] = get_part_string(str(n[m][index_of_hand]))

                handicap["secondforward"] = get_forward_string(n[m][index_of_hand1])

                handicap["secondparticipant"] = get_part_string(str(n[m][index_of_hand1]))
                handicap["firstwin"] = c[m][index_of_hand]

                handicap["secondwin"] = c[m][index_of_hand1]
                handicap["live"] = True
                handicap["href"] = "https://www.marafonsportsbook.com/en/live/animation/" + str(hrefs[m])
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

                result2way["firstparticipant"] = remove_to_win(get_part_string(str(n[m][index_of_hand])))
                result2way['sport'] = "baseball"
                result2way["secondparticipant"] = remove_to_win(get_part_string(str(n[m][index_of_hand1])))
                result2way["firstwin"] = c[m][index_of_hand]

                result2way["secondwin"] = c[m][index_of_hand1]
                result2way["live"] = True
                result2way["href"] = "https://www.marafonsportsbook.com/en/live/animation/" + str(hrefs[m])
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
            handicap_list.append(get_list_of_hand()["handicap"])
            moneyline.append(get_list_of_result2way()["result2way"])

        d = {}
        d["handicap"] = handicap_list
        d["result_2way"] = moneyline
        return d
def basket(url="https://www.marathonplay.com/en/live/45356"):
    url1 = "https://www.marathonplay.com/en/live/45356"

    cookie = {'panbet.sitestyle': 'MULTIMARKETS'}
    html_text = requests.get(url1, cookies=cookie).text
    doc = bs4.BeautifulSoup(html_text, "html.parser")

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

    handicap_list = []
    moneyline = []

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
        spans = ev.find_all("tbody", class_="")

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

            odds[i] = span.find_all("td", {"data-market-type":True},
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
            handicap["sport"] = "basketball"
            handicap["firstparticipant"] = get_part_string(str(n[m][index_of_hand]))

            handicap["secondforward"] = get_forward_string(n[m][index_of_hand1])

            handicap["secondparticipant"] = get_part_string(str(n[m][index_of_hand1]))
            handicap["firstwin"] = c[m][index_of_hand]
            handicap["league"] = get_league(ev)
            handicap["secondwin"] = c[m][index_of_hand1]
            handicap["live"] = True
            handicap["href"] = "https://www.marafonsportsbook.com/en/live/animation/" + str(hrefs[m])
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

            result2way["firstparticipant"] = get_part_string(str(n[m][index_of_hand]))
            result2way["sport"] = "basketball"
            result2way["secondparticipant"] = get_part_string(str(n[m][index_of_hand1]))
            result2way["firstwin"] = c[m][index_of_hand]
            result2way["league"] = get_league(ev)
            result2way["secondwin"] = c[m][index_of_hand1]
            result2way["live"] = True
            result2way["href"] = "https://www.marafonsportsbook.com/en/live/animation/" + str(hrefs[m])
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

        moneyline.append(get_list_of_result2way()["result2way"])
        handicap_list.append(get_list_of_hand()["handicap"])

    d = {}
    d["result2way"] = moneyline
    d["handicap"] = handicap_list
    return d

def unite_dict(dict1, dict2):
    dict1.update(dict2)
    return dict1
def remove_to_win(a):
    return a[:len(a)-7]
def get_scraping_urls(self):
    return ["https://www.marafonbet.info/en/live/26418",
    "https://www.marafonsportsbook.com/en/live/45356",
    "https://www.marafonbet.info/en/live/22723",
    "https://www.marafonbet.info/en/live/120866"
    ]


def isfloat(value):
  try:
    float(value)
    return value
  except ValueError:
    return False
