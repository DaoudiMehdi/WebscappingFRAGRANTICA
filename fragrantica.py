
import requests
from bs4 import BeautifulSoup
import pandas as pd


headers = {
    'authority': 'i.clean.gg',
    'sec-ch-ua': '^\\^',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    'origin': 'https://www.fragrantica.com',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.fragrantica.com/',
    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
}


lien = requests.get("https://www.fragrantica.com/notes/" , headers=headers )
soup = BeautifulSoup(lien.text , 'lxml')
rows = soup.find_all('div' , class_="cell small-6 medium-4 large-3 text-center notebox")

mylist=[]
#fonction pour obtenir la description:
def descriptionfunc(url):
    try:
        url = str(url)
        lien1 = requests.get(url , headers=headers )
        soup1 = BeautifulSoup(lien1.text , 'lxml')
        desc = soup1.find('div' , class_="cell callout").text.split(': ')[1:]
        separator = " "
        description =(separator.join(desc))     
        return description
    except Exception:
        description = "NULL"
        return description

#fonction pour obtenir Groupe de note:
def Groupfunc(url):
    try:
        url = str(url)
        lien1 = requests.get(url , headers=headers )
        soup1 = BeautifulSoup(lien1.text , 'lxml')
        group =soup1.find('b').text     
        return group 
    except Exception:
        group = "NULL"
        return group 
    
for row in rows :

    #obtenir Fragrance Note  et les liens des images
    Note = row.find('img')['alt']
    Image = row.find('img')['src']

    #obtenir lien de chaque note
    url = row.find('a')['href']

    #obtenir la description et le group a partir de les liens
    Description =descriptionfunc(url)
    Group=Groupfunc(url)
    
    #ajouter ces derniers dans un dictionnaire

    data= {
        "Fragrance Note" : Note,
        "Image": Image,
        "Group" : Group,
        "Description" : Description,

    }
    #ajoutes les dictionnaires dans une liste
    mylist.append(data)



#ajouter la liste dans DATAFRAME a l'aide de pandas
df=pd.DataFrame(mylist)


#convertir en csv format
df.to_csv (r'./fragrantica.csv', index = False, header=True)


    






    

