import pandas as pd
import requests
import datetime
import csv
import sys

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
    
    #Iterates over each id in the coin list and outputs a csv of historical marketcap data
    for coin_id in coin_list[0]:
        request_url = f"/coins/{coin_id}/market_chart/range"
        response = requests.get(base_url + request_url,
                            params = params_dict)
        if response.status_code != 200:
            print(f"Error on {coin_id}")
        coin_data = response.json()
        coin_data_df = pd.DataFrame(coin_data["market_caps"])
        coin_data_df.to_csv(f"coin_data/{coin_id}", index = False, header = False)
        print(f"Successfully saved {coin_id} data")

if __name__ == "__main__":
    coin_marketcap_data_extractor(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]), int(sys.argv[7]))