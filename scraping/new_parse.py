import requests
import bs4
import re
url="https://www.marathonbet9.com/en/live/26418#cc=3255521,3255508,3262951,3255473"

cookie = {'panbet.sitestyle': 'MULTIMARKETS'}
html_text = requests.get(url, cookies=cookie).text

doc = bs4.BeautifulSoup(html_text, "html.parser")

# price height-column-with-price first-in-main-row


events = []
odd = []  # тип события
cell = []
hrefs = []
href = []
team = []
hrefs = doc.find_all("tr", class_="broadcasts-menu-container-tr all-regions")

for i in range(len(hrefs)):
    href.append(hrefs[i].a['href'])

teams = doc.find_all("div", class_="live-today-member-name")
odds = doc.find_all("td",
                    {'class': lambda x: x
                                        and 'price' in x.split()
                     }
                    )
names = doc.find_all("tbody", class_="")

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

def Convert(cell):
    d = dict.fromkeys(['coeffs', 'res', 'name'])
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
    a = "None"
    for i in range(len(events)):
        if ((str(events[i]).find(team1) != -1) and (str(events[i]).find(team2) != -1)):
            a =  href[i]
    return a

uniq_odds = []

for o in odd:
    if (uniq_odds.__contains__(o) == 0):
        uniq_odds.append(o)

def get_handicap(index_of_hand, index_of_hand1):

    handicap = {}

    handicap["firstforward"] = get_forward_string(str(Convert(cell)['name'][index_of_hand]))

    handicap["firstparticipant"] = get_part_string(str(Convert(cell)['name'][index_of_hand]))

    handicap["secondforward"] = get_forward_string(str(Convert(cell)['name'][index_of_hand1]))

    handicap["secondparticipant"] = get_part_string(str(Convert(cell)['name'][index_of_hand1]))
    handicap["firstwin"] = Convert(cell)['coeffs'][index_of_hand]

    handicap["secondwin"] = Convert(cell)['coeffs'][index_of_hand1]
    handicap["live"] = "True"
    handicap["href"] = get_url(
        get_part_string(str(Convert(cell)['name'][index_of_hand])),
        get_part_string(str(Convert(cell)['name'][index_of_hand1])))
    return handicap

def get_pairs_of_participants_handicap():
    pairs = []
    uniq_pairs = []

    for j in range(len(events)):
        for i in range(len(Convert(cell)['name']) - 1):
            if ((str(odd[i]) == 'HANDICAP') and (str(odd[i + 1]) == 'HANDICAP')):

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
    for i in range(int(len(pairs) / 2)):
        list.append(get_handicap(pairs[i * 2], pairs[i * 2 + 1]))

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



