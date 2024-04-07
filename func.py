import pandas as pd
import requests
import json
from datetime import datetime

COINS = {
    "Bitcoin (BTC)": 1,
    "Ethereum (ETH)": 1027,
    "EOS": 1765,
    "QnA3.AI (GPT)":29576,
    "Tether (USDt)":825,
}

def get_currency_response(id = 1,range = '7D'):
    params = {
        'id':id,
        "range":range
    }
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36','accept':'*/*'}
    url = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart"
    response = requests.get(url,headers = headers,params = params)
    if response.status_code == 200:
        return response
    else:
        raise AssertionError('данные не подгрузились')
def get_raw_data(response):
    data_raw = json.loads(response.text)
    return data_raw
def transform_data(data_raw):
    df = pd.DataFrame(data_raw['data']['points']).T
    df = df.reset_index(names=['date'])
    df['date'] = df['date'].astype(int).apply(datetime.fromtimestamp)
    
    df['price_v'] = df['v'].str[0].astype(float)
    df['vol_24h_v'] = df['v'].str[1].astype(float)
    df['market_cap_v'] = df['v'].str[2].astype(float)

    df['price_c'] = df['c'].str[0].astype(float)
    df['vol_24h_c'] = df['c'].str[1].astype(float)
    df['market_cap_c'] = df['c'].str[2].astype(float)

    return df[['date','price_v','vol_24h_v','market_cap_v']]

def get_one_coin(name = list(COINS.keys())[0] ,range = '7D'):
    id = COINS[name]
    response = get_currency_response(id = id,range =range)
    data_raw = get_raw_data(response)
    df = transform_data(data_raw)
    return df[['date','price_v']]


if __name__ =='__main__':
    response = get_currency_response()
    data_raw = get_raw_data(response)
    df = transform_data(data_raw)
    print(df)