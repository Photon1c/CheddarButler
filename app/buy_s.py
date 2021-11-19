## from stocks and options programs, import list of symbols to execute buy trades for.
import pandas as pd
import datetime as dt
from config import CONSUMER_KEY, REDIRECT_URI, JSON_PATH
from td.client import TDClient
import lesl

#Create a new instance of the client
TDSession = TDClient(
    client_id= CONSUMER_KEY,
    redirect_uri= REDIRECT_URI,
    credentials_path= JSON_PATH
)
#get daily movers to a list
getmovers = TDSession.get_movers("$DJI", "up", "value")
getmovers2 = TDSession.get_movers("$DJI", "down", "value")
gm = pd.json_normalize(getmovers)
gm2 = pd.json_normalize(getmovers2)
gmt = gm.loc[gm['last'] < 80]
print("The top daily stock gainers are: ")
print(gm[['change','last', 'symbol', 'totalVolume']])
print("The top daily stock losers are: ")
print(gm2[['change','last', 'symbol', 'totalVolume']])
gm['symbol'].to_csv(r'C:\Users\Spark\Desktop\projects\tradesetandforget\csvs\mover_list.csv')
gm3 = pd.DataFrame()
gm4 = pd.DataFrame()
print("The cumulative gain for the up stocks is:")
gm3['Cumulative gain: '] = pd.DataFrame.sum(gm[["change"]])
print(gm3)
print("The cumulative loss for the down stocks is: ")
gm4['Cumulative loss: '] = pd.DataFrame.sum(gm2[["change"]])
print(gm4)


#source of many stocks:
#url = "https://www.sec.gov/include/ticker.txt"
#First source of stocks is url containing thousands of stocka, so it is disabled by default 
#s = pd.read_csv(url, sep = '\t', names=["Symbol", "cusip"])
#second source is csv file in project
s_alt = pd.read_csv(r'C:\Users\Spark\Desktop\projects\tradesetandforget\csvs\mover_list.csv')
#Create Symbols From Dataset
Symbols = s_alt['symbol'].tolist()
target_symbols = []
# iterate over each symbol
dfs =pd.DataFrame()
for i in Symbols:  
    stock = TDSession.get_price_history(symbol=i, period_type='month', period= 1, frequency_type='daily', frequency=1)
    stock_df = pd.DataFrame(stock['candles'])
    df2 = pd.DataFrame()
    df2["Date"] = stock_df['datetime']
    df2["Close"] = stock_df['close']
    df2["Volume"] = stock_df['volume']
    df2["MA10"] = stock_df['close'].rolling(4).mean()
    df2["Symbol"] =stock['symbol']
    bool = df2["MA10"].iloc[-1] < df2["Close"].iloc[-1]  ##create Boolean to filter out target stocks
    if bool == True:
        target_list = stock['symbol']
        target_symbols.append(target_list)
        #print("The testing dataframes look as follow: ")
        #print(df2.tail(1))
    else:
        print("Stock", i, "is not within buying parameters")
print("The target symbols are: ")
print(target_symbols)
print("Buy Stocks function complete. Initiating Buy Options function...")





    
#Set the target variable to the selected symbol in final candidate stock dataframe, ts


