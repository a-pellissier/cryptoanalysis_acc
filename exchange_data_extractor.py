import pandas as pd
import requests
import datetime
import csv
import sys
import ipdb
import time
from colorama import Fore, Back, Style

def exchange_data_extractor(days):
    base_url = "http://api.coingecko.com/api/v3"
    wait_time = 70

    with open('targets_lists/exchange_list.csv', newline=None) as f:
        reader = csv.reader(f)
        exchange_list = list(reader)

    if len(exchange_list) == 0:
        print('Please input at least one exchange id in exchange_list.csv')
        return None

    params_dict = {'days' : days}

    request_url = f"/exchanges/{exchange_list[0][0]}/volume_chart"
    response = requests.get(base_url + request_url, params = params_dict)
    while response.status_code != 200:
        print(Fore.RED + f"API error on {exchange_list[0][0]} - Error {response.status_code}")
        print(Fore.WHITE + f"Waiting for {wait_time} seconds")
        time.sleep(wait_time)
    count = 1
    exchange_data = response.json()
    exchange_volume_data_df = pd.DataFrame(data = exchange_data, index=None, columns=["Date", exchange_list[0][0]])
    print(Fore.GREEN + f"{count} - Successfully saved {exchange_list[0][0]} data")

    if len(exchange_list[0]) > 0:
        for exchange_id in exchange_list[0][1:]:
            request_url = f"/exchanges/{exchange_id}/volume_chart"
            response = requests.get(base_url + request_url, params = params_dict)
            while response.status_code != 200:
                print(Fore.RED + f"{count} - API error on {exchange_id} - Error {response.status_code}")
                print(Fore.WHITE + f"Waiting for {wait_time} seconds")
                time.sleep(wait_time)
                response = requests.get(base_url + request_url, params = params_dict)
            count += 1
            exchange_data = response.json()
            temp_exchange_df = pd.DataFrame(exchange_data, columns = ['Date', f'{exchange_id}'])
            exchange_volume_data_df = exchange_volume_data_df.merge(right = temp_exchange_df, on = 'Date', how = "left")
            print(Fore.GREEN + f"{count} - Successfully saved {exchange_id} data")

    exchange_volume_data_df.to_csv(f"exchange_data/exchange_volume_data.csv", index = False)

if __name__ == '__main__':
    exchange_data_extractor(sys.argv[1])