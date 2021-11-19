#successful fun on 8.31.21

import pandas as pd
from config import CONSUMER_KEY, REDIRECT_URI, JSON_PATH
from lesl import td_account
from td.client import TDClient
import datetime
import loghog


#Create a new instance of the client
TDSession = TDClient(
    client_id= CONSUMER_KEY,
    redirect_uri= REDIRECT_URI,
    credentials_path= JSON_PATH)

def quickgetpricehistoryfast():
    #source of many stocks:
    #url = "https://www.sec.gov/include/ticker.txt"
    #First source of stocks is url containing thousands of stocka, so it is disabled by default 
    #s = pd.read_csv(url, sep = '\t', names=["Symbol", "cusip"])
    #second source is csv file in project
    s_alt_path = r'C:\Users\Spark\Desktop\projects\tradesetandforget\csvs\q7.csv'
    s_alt = pd.read_csv(s_alt_path)
    #Create Symbols From Dataset
    Symbols = s_alt['symbol'].tolist()
    target_symbols =[]
    # iterate over each symbol
    dfs =pd.DataFrame()
    for i in Symbols:  

        stock = TDSession.get_price_history(symbol=i, period_type='month', period= 1, frequency_type='daily', frequency=1)
        stock_df = pd.DataFrame(stock['candles'])
        df2 = pd.DataFrame()
        df2["Date"] = stock_df['datetime']
        df2["Date"] = pd.to_numeric(df2["Date"])
        df2["Date"] = pd.to_datetime(df2["Date"], unit='ms')
        df2["Close"] = stock_df['close']
        df2["Volume"] = stock_df['volume']
        df2["MA10"] = stock_df['close'].rolling(4).mean().round(2)
        df2["Symbol"] =stock['symbol']
        bool = df2["MA10"].iloc[-1] < df2["Close"].iloc[-1]  ##create Boolean to filter out target stocks
        if bool == True:
            target_list = stock['symbol']
            print("The target dataframe is: ")    
            print(df2.tail(1))
        else:
            print("Stock", i, "is not within the target parameters")

if __name__ == '__main__':
    try:
        quickgetpricehistoryfast()
    except TypeError:
        quickgetpricehistoryfast()
