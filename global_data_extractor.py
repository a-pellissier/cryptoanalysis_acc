import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import csv
import time
import rfc3339
import iso8601
import sys
from colorama import Fore, Back, Style


def getAndFormatNomics(start_date, base_url, params_dict, request_url, endpoint):
    response = requests.get(base_url + request_url, params=params_dict)
    data = [[datetime.datetime.timestamp(iso8601.parse_date(day['timestamp'])),
             int(day[endpoint])] for day in response.json()]
    data_df = pd.DataFrame(data=data, index=None, columns=["Date", endpoint])
    return data_df


def globalDataExtractor(year_start, month_start, day_start):
    start_date = datetime.datetime(year_start, month_start, day_start).isoformat('T') + 'Z'
    base_url = "https://api.nomics.com/v1"
    params_dict = {
        "key": "b845b528a86218340118ff165bfc2947",
        "start": start_date,
    }

    # Market cap data
    request_url = "/market-cap/history"
    global_data_df = getAndFormatNomics(start_date, base_url, params_dict, request_url, 'market_cap')
    print(Fore.GREEN + f"Successfully saved global marketcap data")

    # Add volume_data
    request_url = "/volume/history"
    global_volume_data_df = getAndFormatNomics(start_date, base_url, params_dict, request_url, 'volume')
    print(Fore.GREEN + f"Successfully saved global volume data")
    global_data_df = global_data_df.merge(right=global_volume_data_df, on='Date', how='left')

    #Save the dataframe as a CSV
    global_data_df.to_csv('global_data/global_data.csv')


if __name__ == '__main__':
    globalDataExtractor(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))