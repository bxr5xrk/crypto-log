from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start': '1',
    'limit': '20',
    'convert': 'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '1a8f0f27-c231-4adf-ae04-da90603e8a60',
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)

    result = response.json()

    with open('data.json', 'w') as f:
        json.dump(result, f, sort_keys=False, indent=4)

except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
