from bs4 import BeautifulSoup
from requests_html import HTMLSession
import time
from firebase_admin import credentials, firestore

def db_store(coins, prices, market_caps, total_exchange_volumes, returns_24h, total_supply, categories, value_proposition):
    cred = credentials.Certificate("./serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    print('UPDATING VALUES..')
    for i in range(len(coins)):
        data = {"name": coins[i], "price": prices[i], "market_cap": market_caps[i], "total_exchange":total_exchange_volumes[i], "return": returns_24h[i], "total_supply": total_supply[i],"category": categories[i], "value_proposition": value_proposition[i]}
        db.collection("current-cryptocoins").document(ids[i]).set(data)
    print('ALL UPDATED')    

if __name__ == '__main__':
    print('GETTING VALUES...')

    url = 'https://www.coindesk.com/coindesk20'
    session = HTMLSession()
    page = session.get(url)
    time.sleep(2)
    page.html.render()
    soup = BeautifulSoup(page.html.html, 'lxml')

    moneda = soup.find_all('section', class_ = 'tr-section')

    ids=list()
    coins=list()
    prices=list()
    market_caps=list()
    total_exchange_volumes=list()
    returns_24h=list()
    total_supply=list()
    categories=list()
    value_proposition=list()

    for m in moneda:
        datos = m.find('div', class_ = 'tr-right').find_all('span', class_ = 'cell')
        ids.append(m.find('span', class_ = 'cell-asset-iso').text)
        coins.append(m.find('strong', class_ = 'cell-asset-title').text)
        prices.append(datos[0].text)
        market_caps.append(datos[1].text)
        total_exchange_volumes.append(datos[2].text)

        if 'price-down' in datos[3]['class']:
            returns_24h.append('-' + datos[3].text)
        else:
            returns_24h.append('+'+datos[3].text)
            
        total_supply.append(datos[4].text)
        categories.append(datos[5].text)
        value_proposition.append(datos[6].text)

    db_store(coins, prices, market_caps, total_exchange_volumes, returns_24h, total_supply, categories, value_proposition)
