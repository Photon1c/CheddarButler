## from stocks and options programs, import list of symbols to execute buy trades for.
import pandas as pd
import datetime as dt
from config import CONSUMER_KEY, REDIRECT_URI, JSON_PATH
from td.client import TDClient
import lesl
import datetime as dt

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
mt = gm.loc[gm['last'] < 150]
gmt = gmt.append(gm2)
print("The top daily stock gainers are: ")
print(gm[['change','last', 'symbol', 'totalVolume']])
print("The top daily stock losers are: ")
print(gm2[['change','last', 'symbol', 'totalVolume']])
gm[['change','last', 'symbol', 'totalVolume']].to_csv(r'/home/lescua/projects/fin_suite/CheddarButler_v1/csvs/mover_gainers.csv')
gm2[['change','last', 'symbol', 'totalVolume']].to_csv(r'/home/lescua/projects/fin_suite/CheddarButler_v1/csvs/mover_losers.csv')
gmt['symbol'].to_csv(r'/[pathtomoverlistcsvfile]')
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
s_alt = pd.read_csv(r'[PATH]')
#Create Symbols From Dataset
Symbols = s_alt['symbol'].tolist()
target_symbols_long = []
target_symbols_short = []
# iterate over each symbol
dfs =pd.DataFrame()
for i in Symbols:  
    stock = TDSession.get_price_history(symbol=i, period_type='month', period= 1, frequency_type='daily', frequency=1)
    stock_df = pd.DataFrame(stock['candles'])
    df2 = pd.DataFrame()
    df2["Date"] = stock_df['datetime']
    df2["Close"] = stock_df['close']
    df2["Volume"] = stock_df['volume']
    df2["MA9"] = stock_df['close'].rolling(9).mean()
    df2["Symbol"] =stock['symbol']
    bool_long = df2["MA9"].iloc[-1] < df2["Close"].iloc[-1]  ##create Boolean to filter out stocks to go long on.
    if bool_long == True:
        target_list_long = stock['symbol']
        target_symbols_long.append(target_list_long)
        print("Stock ", i, "is within buying parameters. Dataframe: " , "\n")
        print(df2.tail(1))
    else:
        print("Stock", i, "is not within buying parameters")
    bool_short = df2["MA9"].iloc[-1] > df2["Close"].iloc[-1]  ##create second boolean to filter out stocks to short.
    if bool_short == True:
        target_list_short = stock['symbol']
        target_symbols_short.append(target_list_short)
        print("Stock ", i, "is within selling parameters. Dataframe: " , "\n")
        print(df2.tail(1))
    else:
        print("Stock", i, "is not within selling parameters")   
print("The aggregate mover list is: ", "\n", gmt)
print("The target symbols to go long on are: ")
print(target_symbols_long)
print("The target symbols to short are: ", "\n", target_symbols_short)
