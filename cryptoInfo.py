import json
from bs4 import BeautifulSoup
import requests
from datetime import date

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

orange, white = '\u001b[33m', '\u001b[37m'
red, green = '\u001b[31m', '\u001b[32m'

parameters = {
    'start': '1',
    'limit': '20',
    'convert': 'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '1a8f0f27-c231-4adf-ae04-da90603e8a60',
}

session = requests.Session()
session.headers.update(headers)

response = session.get(url, params=parameters)

data = json.loads(response.text)

today_date_temp = date.today()
today_date = today_date_temp.day
date_for_news = today_date_temp.strftime("%d.%m")
if today_date in range(1, 11):
    today_date = f'0{today_date}'


def banner_title():
    print(f'+{"-"*68}+')
    print(f'|{" "*68}|')
    print(f'|{" "*28}{orange}CRYPTO NEWS{white}{" "*29}|')
    print(f'|{" "*68}|')
    print(f'+{"-"*68}+')
    print('|   name   |  price   |   1d   |   7d   |  30d   |   60d   |   90d   |')
    print(f'+{"-"*68}+')


def banner_price(*id):

    banner_title()

    for item in data["data"]:
        id_list = id

        if item['id'] in id_list:
            def price(time_interval):
                price_returned = item["quote"]["USD"][time_interval]
                return "{:.2f}".format(price_returned)

            temp_coin_price = item["quote"]["USD"]["price"]
            coin_price = "{:.2f}".format(temp_coin_price)

            # dynamic space
            a = ''
            if len(coin_price) < 8:
                a += ' '*(8-len(coin_price))
            b = ''
            if len(item["name"]) < 8:
                b += ' '*(8-len(item["name"]))

            price1d = price("percent_change_24h")
            if price1d[0] != '-':
                price1d = '+'+price("percent_change_24h")
            if len(price1d) < 6:
                price1d += ' '*(6-len(price1d))

            price7d = price("percent_change_7d")
            if price7d[0] != '-':
                price7d = '+'+price("percent_change_7d")
            if len(price7d) < 6:
                price7d += ' '*(6-len(price7d))

            price30d = price("percent_change_30d")
            if price30d[0] != '-':
                price30d = '+'+price("percent_change_30d")
            if len(price30d) < 6:
                price30d += ' '*(6-len(price30d))

            price60d = price("percent_change_60d")
            if price60d[0] != '-':
                price60d = '+'+price("percent_change_60d")
            if len(price60d) < 7:
                price60d += ' '*(7-len(price60d))

            price90d = price("percent_change_90d")
            if price90d[0] != '-':
                price90d = '+'+price("percent_change_90d")
            if len(price90d) < 7:
                price90d += ' '*(7-len(price90d))

            if price1d[0] == '-':
                price1d = red+price1d+white
            else:
                price1d = f'{green}{price1d}{white}'
            if price7d[0] == '-':
                price7d = red+price7d+white
            else:
                price7d = f'{green}{price7d}{white}'
            if price30d[0] == '-':
                price30d = red+price30d+white
            else:
                price30d = f'{green}{price30d}{white}'
            if price60d[0] == '-':
                price60d = red+price60d+white
            else:
                price60d = f'{green}{price60d}{white}'
            if price90d[0] == '-':
                price90d = red+price90d+white
            else:
                price90d = f'{green}{price90d}{white}'

            one_part = f'| {orange}{item["name"]}{white}{b} | {coin_price}{a} '
            two_part = f'| {price1d} | {price7d} | {price30d} '
            three_part = f'| {price60d} | {price90d} |'
            print(one_part+two_part+three_part)
            print(f'+{"-"*68}+')
    print()


def print_news():
    news_site = 'https://beincrypto.ru/news/'
    headers = {'user_agent': 'Mozilla/5.0 (X11; Linux x86_64)'}
    req = requests.get(url=news_site, headers=headers)

    soup = BeautifulSoup(req.text, 'lxml')

    news = soup.find_all(class_='multi-news-card bb-1 d-lg-flex flex-lg-column mb-5')

    n = 1
    global results
    results = []
    for item in news:
        news_date = item.find('span', class_="date").get_text(strip=True)

        if int(news_date[4:6]) == int(today_date):
            news_title = item.find(class_='title h-100').get_text(strip=True)
            news_desc = item.find(class_='tpw').get_text(strip=True)
            news_href = item.a.get('href')

            print(f'{n}. {green}{date_for_news}{white} {news_desc}')
            print(f'{orange}{news_title}{white}\n')
            n += 1
            results.append({
                'title': news_title,
                'desc': news_desc,
                'href': news_href,
            })


def get_link_for_news():
    again = 'y'

    def get_link():
        get_link = int(input('enter number to get link: '))
        print()
        q = 1
        for item in results:
            if q == get_link:
                print(f'{q}. {green}{date_for_news}{white} {item["desc"]}')
                print(f'{orange}{item["title"]}\n{white}{item["href"]}\n')
                break
            else:
                q += 1
                continue

    while again == 'y':
        get_link()
        again = input('do you want another link? (y, n): ')
        if again == 'y':
            continue
        else:
            break


banner_price(1, 3890, 1027, 5426, 2010)
print_news()
get_link_for_news()
