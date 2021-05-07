import pandas as pd
import requests
import datetime
import csv
import sys
import time
from colorama import Fore, Back, Style

from tools import apiRequestHandler, exchangeDataBuilder


def exchange_data_extractor(days):
    base_url = "http://api.coingecko.com/api/v3"
    wait_time = 70

    with open("targets_lists/exchange_list.csv", newline=None) as f:
        reader = csv.reader(f)
        exchange_list = list(reader)

    if len(exchange_list) == 0:
        print("Please input at least one exchange id in exchange_list.csv")
        return None

    params_dict = {"days": days}

    request_url = f"/exchanges/{exchange_list[0][0]}/volume_chart"
    count = 1
    exchange_data = apiRequestHandler(base_url, request_url, params_dict, count, exchange_list[0][0], wait_time)
    exchange_volume_data_df = pd.DataFrame(data=exchange_data, index=None, columns=["Date", exchange_list[0][0]])
    print(Fore.GREEN + f"{count} - Successfully saved {exchange_list[0][0]} data")

    if len(exchange_list[0]) > 0:
        for exchange_id in exchange_list[0][1:]:
            request_url = f"/exchanges/{exchange_id}/volume_chart"
            count += 1
            exchange_data = apiRequestHandler(base_url, request_url, params_dict, count, exchange_list[0][0], wait_time)

            exchange_volume_data_df = exchangeDataBuilder(exchange_data, exchange_volume_data_df, exchange_id, count)

    exchange_volume_data_df.to_csv(f"exchange_data/exchange_volume_data.csv", index=False)


if __name__ == "__main__":
    exchange_data_extractor(sys.argv[1])
