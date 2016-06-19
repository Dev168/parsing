import requests
import bs4
import re

url="https://www.marathonbet9.com/en/live/26418#cc=3255521,3255508,3262951,3255473"
cookie = {'panbet.sitestyle': 'MULTIMARKETS'}
html_text = requests.get(url,cookies=cookie).text

doc = bs4.BeautifulSoup(html_text, "html.parser")


a = doc.find_all("tbody")
