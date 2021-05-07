import pandas as pd
import requests
import datetime
import csv
import sys
import ipdb
import time
from colorama import Fore, Back, Style


def apiRequestHandler(base_url, request_url, params_dict, count, object_id, wait_time):
    # All inputs are required. Handles the interface with the API.
    response = requests.get(base_url + request_url, params=params_dict)
    while response.status_code != 200:
        print(Fore.RED + f"{count} - API error on {object_id} - Error {response.status_code}")
        if response.status_code == 429:
            print(Fore.WHITE + f"Waiting for {wait_time} seconds")
            time.sleep(wait_time)
            response = requests.get(base_url + request_url, params=params_dict)
        else:
            return 'error'
    return response.json()


def coinDataBuilder(coin_data, coin_marketcap_data_df, coin_volume_data_df, coin_price_data_df, coin_id, count):
    # All inputs are required. Updates the dataframe with new coin data.
    temp_coin_mc = pd.DataFrame(coin_data['market_caps'], columns=['Date', f'{coin_id}'])
    coin_marketcap_data_df = coin_marketcap_data_df.merge(right=temp_coin_mc, on='Date', how='left')
    temp_coin_v = pd.DataFrame(coin_data['total_volumes'], columns=['Date', f'{coin_id}'])
    coin_volume_data_df = coin_volume_data_df.merge(right=temp_coin_v, on='Date', how='left')
    temp_coin_price = pd.DataFrame(coin_data['prices'], columns=['Date', f'{coin_id}'])
    coin_price_data_df = coin_price_data_df.merge(right=temp_coin_price, on='Date', how='left')
    print(Fore.GREEN + f"{count} - Successfully saved {coin_id} data")
    return coin_marketcap_data_df, coin_volume_data_df, coin_price_data_df


def exchangeDataBuilder(exchange_data, exchange_volume_data_df, exchange_id, count):
    # All inputs are required. Updates the dataframe with new exchange data.
    temp_exchange_df = pd.DataFrame(exchange_data, columns=["Date", f"{exchange_id}"])
    exchange_volume_data_df = exchange_volume_data_df.merge(right=temp_exchange_df, on="Date", how="left")
    print(Fore.GREEN + f"{count} - Successfully saved {exchange_id} data")
    return exchange_volume_data_df