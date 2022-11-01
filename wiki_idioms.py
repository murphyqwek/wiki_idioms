from random import randint
import requests
from bs4 import BeautifulSoup as bs

def skip_idiom(c):
    if randint(0, c) == 0: return 0
    else: return 1

def generate_(tables, chance, count_):
    idioms = []
    for table in tables:
        rows = table.findChildren("tr" , recursive=True)
        count = 0
        for i in range(1, len(rows)):
            if count == count_: break
            if skip_idiom(chance): continue
            row = rows[i].findChildren("td")
            if row[0].text.lower()[0] == 'ё': break
            if len(row) >= 2:
                if len(row[1].text) > 2:
                    description = row[1].text
                    description = description.replace('\n', '')
                    if description[-1] != '.': description += '.'
                    if not(description.isdigit()) and description[0] != "(" and description.lower().find('см.') == -1 and description.lower().find('предик.,') == -1 and description != "??" and description.lower() != row[0].text.lower():
                        idioma = [row[0].text, description]
                        idioms.append(idioma)
            count += 1
    return idioms

wiki_url = 'https://ru.wiktionary.org/wiki/%D0%9F%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5:%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%84%D1%80%D0%B0%D0%B7%D0%B5%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D0%B7%D0%BC%D0%BE%D0%B2_%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%BE%D0%B3%D0%BE_%D1%8F%D0%B7%D1%8B%D0%BA%D0%B0'

r = requests.get(wiki_url)

soup = bs(r.text, "html.parser")

tables = soup.find_all('table', class_='wikitable sortable')

n = int(input("Введите количество файлов: "))
chance = int(input("Введите шанс: "))
count = int(input("Введите максимальное количество идиом, начинающиеся на одну букву: "))

for kk in range(n):
    uju = generate_(tables, chance, count)
    with open(f"idioms_{kk}.txt", 'w', encoding="utf-8") as f:
        for n in uju:
            desc = n[1][0].lower() + n[1][1:]
            if(n[0].lower != desc[-1]):
                f.write(f"{n[0].capitalize()} - {desc}\n") 
