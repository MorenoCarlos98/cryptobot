import requests
from bs4 import BeautifulSoup
from firebase_admin import credentials, firestore

def delete_collection(db):
    print('DELETING OLD NEWS...')

    docs = db.collection("news-cryptocoins").stream()
    for doc in docs:
        doc.reference.delete()

def db_store(db, links_new, links_img, titles):
    print('ADDING NEWS...')

    for i in range(len(links_new)):
        response = requests.get(links_new[i])
        if response.status_code == 200:
            data = {"link_new": links_new[i], "link_img": links_img[i], "title": titles[i]}
            db.collection("news-cryptocoins").add(data)
            
    print('ALL ADDED')        


def getData(url, e, links_new, links_img, titles):
    link_new = e.find('a')['href']

    if link_new.startswith('/'):
        links_new.append(url + link_new)
    else:
        links_new.append(link_new)     

    links_img.append(e.find('img')['data-src'])
    titles.append(e.find('div', class_='props').find('h4').text)

    

if __name__ == '__main__':
    cred = credentials.Certificate("./serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    delete_collection(db)

    links_new = list()
    links_img = list()
    titles = list()

    url = "https://cryptonews.com/news"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')

    news = soup.find_all('div', class_='cn-list grid')

    for i in news:
        [getData(url, j, links_new, links_img, titles) for j in i.find_all('div', class_='cn-tile article')]

    news = soup.find_all('div', class_='cn-list cols limits')

    for i in news:
        [getData(url, j, links_new, links_img, titles) for j in i.find_all('div', class_='cn-tile article')]    

    db_store(db, links_new, links_img, titles)  
