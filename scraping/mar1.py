import requests
import bs4
import re
import sys
import os
from datetime import datetime


def events(url="https://www.mthbet.com/su/live/popular"):

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
        odd.append(odds[i]['data-market-type'].strip())
        cell.append(odds[i]['data-sel'].strip())


    for i in range(len(names)):
        events.append(names[i]['data-event-name'].strip())

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
            for i in range(len(Convert(cell)['name'])):
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
            for i in range(len(Convert(cell)['name'])):
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
            for i in range(len(Convert(cell)['name'])):
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
            for i in range(len(Convert(cell)['name'])):
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




