import pandas as pd
import requests
import datetime
import csv
import sys
import ipdb


def exchange_data_extractor(days):
    base_url = "http://api.coingecko.com/api/v3"

    with open('targets_lists/exchange_list.csv', newline=None) as f:
        reader = csv.reader(f)
        exchange_list = list(reader)

    if len(exchange_list) == 0:
        print('Please input at least one exchange id in exchange_list.csv')
        return None

    params_dict = {'days' : days}

    request_url = f"/exchanges/{exchange_list[0][0]}/volume_chart"
    response = requests.get(base_url + request_url, params = params_dict)
    if response.status_code != 200:
        print(f"API error on {exchange_list[0][0]}")
    else:
        exchange_data = response.json()
        exchange_volume_data_df = pd.DataFrame(data = exchange_data, index=None, columns=["Date", exchange_list[0][0]])
        print(f"Successfully saved {exchange_list[0][0]} data")

    if len(exchange_list[0]) > 0:
        for exchange_id in exchange_list[0][1:]:
            request_url = f"/exchanges/{exchange_id}/volume_chart"
            response = requests.get(base_url + request_url, params = params_dict)
            if response.status_code != 200:
                print(f"API error on {exchange_id}")
            else:
                exchange_data = response.json()
                exchange_v = [day[1] for day in exchange_data]
                exchange_volume_data_df[[f'{exchange_id}']] = pd.DataFrame(exchange_v, index=None)
                print(f"Successfully saved {exchange_id} data")

    exchange_volume_data_df.to_csv(f"exchange_data/exchange_volume_data.csv", index = False)

if __name__ == '__main__':
    exchange_data_extractor(sys.argv[1])