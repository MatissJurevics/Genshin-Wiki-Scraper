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

def getinfo(name):
    html_text = requests.get(f'https://genshin-impact.fandom.com/wiki/{name}').text
    ## writes web content to text file
    with open(f'./character/{name}.txt', 'w', encoding='utf-8') as f:
        f.write(html_text)
        f.close()
    soup = BeautifulSoup(html_text,'lxml')

    ## Gets Rating
    rating = soup.find('td', {"data-source":"rarity"})
    print(name, rating.img.attrs['alt'])
    character_info[names_list.index(name)]["Rating"]=rating.img.attrs["alt"]

    ## Gets Weapon
    weapon = soup.find('td', {"data-source":"weapon"})
    print(name, weapon.span.a.attrs['title'])
    character_info[names_list.index(name)]["Weapon"] = weapon.span.a.attrs['title']

    ## Gets Gender
    gender = soup.find('div', {"data-source":"sex"})
    ## try except because traveler's gender is structured a bit differently
    try: 
        print(name, gender.div.a.text)
    except:
        print(name, gender.div.text)
    try: 
        character_info[names_list.index(name)]["Gender"] = gender.div.a.text
    except:
        character_info[names_list.index(name)]["Gender"] = gender.div.text

    ## gets element
    element = soup.find('td', {"data-source":"element"})
    try:
        print(name, element.span.a.attrs['title'])
    except:
        print(name, element.text)
    try:
        character_info[names_list.index(name)]["Element"] = element.span.a.attrs['title']
    except: 
        character_info[names_list.index(name)]["Element"] = element.text
    
    ## Gets Special Dish
    dish = soup.find('div', {"data-source":"dish"})
    try:
        print(name, dish.div.a.attrs['title'])
    except:
        print("none")
    try: 
        character_info[names_list.index(name)]["Dish"] = dish.div.a.attrs['title']
    except:
        character_info[names_list.index(name)]["Dish"] = "None"
    try:
        dish_wiki_link_rel = dish.div.a.attrs['href']
        dish_wiki_link = f'https://genshin-impact.fandom.com{dish_wiki_link_rel}'
        character_info[names_list.index(name)]["Dish-Link"] = dish_wiki_link
    except:
        pass
    
        

def jsondump():
    with open('info.json', 'w') as f:
        json.dump(character_info, f)
        f.close()

getnames()
for name in names_list:
    getinfo(name)
jsondump()