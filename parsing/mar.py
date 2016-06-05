import requests
import bs4
import re

html_text = requests.get("https://www.marathonbet6.com/su/live/popular").text

doc = bs4.BeautifulSoup(html_text, "html.parser")






events = []
odd  =  [] # тип события
cell = []

team =[]







teams = doc.find_all("div", class_="live-today-member-name")
odds =doc.find_all("td",class_="price height-column-with-price ")




names = doc.find_all("tbody",class_="")

for i in range(len(odds)):
    odd.append(doc.find_all("td",class_="price height-column-with-price ")[i]['data-market-type'].strip())
    cell.append(doc.find_all("td",class_="price height-column-with-price ")[i]['data-sel'].strip())


for i in range(len(names)):
    events.append(doc.find_all("tbody", class_="")[i]['data-event-name'].strip())

for i in range(len(teams)):
    team.append(doc.find_all("div", class_="live-today-member-name")[i].contents[0].strip())





def coeff(cell):
    q=[]
    q = re.split('[,]+', cell)



    for i in range(len(q)):
        if (q[i].__contains__("epr")):
            coeff = q[i][7:]

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



uniq_odds = []

for o in  odd:
    if(uniq_odds.__contains__(o)==0):
        uniq_odds.append(o)





