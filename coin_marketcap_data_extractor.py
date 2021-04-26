import pandas as pd
import requests
import datetime
import csv
import sys
import ipdb
def coin_marketcap_data_extractor(currency, year_start, month_start, day_start, year_end, month_end, day_end):
    #This is the main api url
    base_url = "http://api.coingecko.com/api/v3"

    #We start by reading all the desired coins, and storing them in a list
    with open('coin_list.csv', newline=None) as f:
        reader = csv.reader(f)
        coin_list=list(reader)

    start_date = datetime.datetime(year_start, month_start, day_start)
    end_date = datetime.datetime(year_end, month_end, day_end)
    params_dict = {"vs_currency" : currency,
                    "from" : datetime.datetime.timestamp(start_date),
                    "to" : datetime.datetime.timestamp(end_date)}
    
    #Instantiates the outpout dataframe with the data of the first coin
    request_url = f"/coins/{coin_list[0][0]}/market_chart/range"
    response = requests.get(base_url + request_url, params = params_dict)
    if response.status_code != 200:
        print(f"Error on {coin_list[0][0]}")
    coin_data = response.json()
    coin_data_df = pd.DataFrame(data = coin_data["market_caps"], index=None, columns=["Date", coin_list[0][0]])
    print(f"Successfully saved {coin_list[0][0]} data")

    #Iterates over each id in the coin list and outputs a csv of historical marketcap data
    for coin_id in coin_list[0][1:]:
        request_url = f"/coins/{coin_id}/market_chart/range"
        response = requests.get(base_url + request_url, params = params_dict)
        if response.status_code != 200:
            print(f"Error on {coin_id}")
        coin_data = response.json()
        coin_mc = [day[1] for day in coin_data["market_caps"]]
        coin_data_df[[f'{coin_id}']] = pd.DataFrame(coin_mc, index=None)
        print(f"Successfully saved {coin_id} data")
    coin_data_df.to_csv(f"coin_data/marketcap_data.csv", index = False)

if __name__ == "__main__":
    coin_marketcap_data_extractor(sys.argv[1],
        int(sys.argv[2]),
        int(sys.argv[3]),
        int(sys.argv[4]),
        int(sys.argv[5]),
        int(sys.argv[6]), 
        int(sys.argv[7]))