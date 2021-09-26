from bs4 import BeautifulSoup
import requests
import json

character_info = []
names_list = []
def getnames():
    html_text = requests.get('https://genshin-impact.fandom.com/wiki/Genshin_Impact_Wiki').text

    soup = BeautifulSoup(html_text,'lxml')
    # checks the html for the class 'card_font' which only names have
    names = soup.find_all('span', class_='card_font')
    # creates a list of names
    for name in names:
        character_info.append({"name": name.text ,})
        names_list.append(name.text)

def getstars(name):
    html_text = requests.get(f'https://genshin-impact.fandom.com/wiki/{name}').text
    with open(f'./character/{name}.txt', 'w', encoding='utf-8') as f:
        f.write(html_text)
        f.close()
    soup = BeautifulSoup(html_text,'lxml')
    rating = soup.find('td', {"data-source":"rarity"})
    print(name, rating.img.attrs['alt'])
    character_info[names_list.index(name)]["rating"]=rating.img.attrs["alt"]



def jsondump():
    with open('info.json', 'w') as f:
        json.dump(character_info, f)
        f.close()

getnames()
for name in names_list:
    getstars(name)
jsondump()