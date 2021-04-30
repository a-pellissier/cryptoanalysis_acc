import pandas as pd
import requests
import datetime
import csv
import sys
import ipdb
import time
from colorama import Fore, Back, Style


def coin_data_extractor(currency, year_start, month_start, day_start, year_end, month_end, day_end):
    #This is the main api url
    base_url = "http://api.coingecko.com/api/v3"
    wait_time = 60

    #We start by reading all the desired coins, and storing them in a list
    with open('targets_lists/coin_list.csv', newline=None) as f:
        reader = csv.reader(f)
        coin_list = list(reader)
    
    if len(coin_list) == 0:
        print('Please input at least one coin id in coin_list.csv')
        return None

    start_date = datetime.datetime(year_start, month_start, day_start)
    end_date = datetime.datetime(year_end, month_end, day_end)
    params_dict = {"vs_currency" : currency,
                    "from" : datetime.datetime.timestamp(start_date),
                    "to" : datetime.datetime.timestamp(end_date)}
    
    #Instantiates the outpout dataframe with the data of the first coin
    request_url = f"/coins/{coin_list[0][0]}/market_chart/range"
    response = requests.get(base_url + request_url, params = params_dict)
    if response.status_code != 200:
        print(Fore.RED + f"API error on {coin_list[0][0]} - Error {response.status_code}")
    else:
        coin_data = response.json()
        coin_marketcap_data_df = pd.DataFrame(data = coin_data["market_caps"], index=None, columns=["Date", coin_list[0][0]])
        coin_volume_data_df = pd.DataFrame(data = coin_data["total_volumes"], index=None, columns=["Date", coin_list[0][0]])
        coin_price_data_df = pd.DataFrame(data = coin_data["prices"], index=None, columns=["Date", coin_list[0][0]])
        print(Fore.GREEN + f"1 - Successfully saved {coin_list[0][0]} data")

    #Iterates over each id in the coin list and outputs a csv of historical marketcap data
    if len(coin_list[0]) > 0:
        count = 1
        for coin_id in coin_list[0][1:]:
            request_url = f"/coins/{coin_id}/market_chart/range"
            response = requests.get(base_url + request_url, params = params_dict)
            count += 1
            if response.status_code != 200:
                print(Fore.RED + f"{count+1} - API error on {coin_id} - Error {response.status_code}")
            else:
                coin_data = response.json()
                coin_mc = [day[1] for day in coin_data["market_caps"]]
                coin_v = [day[1] for day in coin_data["total_volumes"]]
                coin_p = [day[1] for day in coin_data["prices"]]
                coin_marketcap_data_df[[f'{coin_id}']] = pd.DataFrame(coin_mc, index=None)
                coin_volume_data_df[[f'{coin_id}']] = pd.DataFrame(coin_v, index=None)
                coin_price_data_df[[f'{coin_id}']] = pd.DataFrame(coin_p, index=None)
                print(Fore.GREEN + f"{count+1} - Successfully saved {coin_id} data")
            if count%20 == 0:
                print(Fore.WHITE + f"Waiting for {wait_time} seconds")
                time.sleep(60)
    
    coin_marketcap_data_df.to_csv(f"coin_data/coin_marketcap_data.csv", index = False)
    coin_volume_data_df.to_csv(f"coin_data/coin_volume_data.csv", index = False)
    coin_price_data_df.to_csv(f"coin_data/coin_price_data.csv", index = False)

if __name__ == "__main__":
    coin_data_extractor(sys.argv[1],
                        int(sys.argv[2]),
                        int(sys.argv[3]),
                        int(sys.argv[4]),
                        int(sys.argv[5]),
                        int(sys.argv[6]), 
                        int(sys.argv[7]))