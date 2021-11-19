#from list of symbols and instruments (stocks or options), generate search
#from search generate list of symbols and instruments (stocks and options) to sell.

#working 10.21.21

import pandas as pd
import datetime as dt
from config import CONSUMER_KEY, REDIRECT_URI, JSON_PATH
from td.client import TDClient
import lesl
import pprint

#Create a new instance of the client
TDSession = TDClient(
    client_id= CONSUMER_KEY,
    redirect_uri= REDIRECT_URI,
    credentials_path= JSON_PATH
)
#Retrieve position data, export to iterable list in file
Sell1 = TDSession.get_accounts(account=lesl.td_account, fields=['positions'])
try:
    Sell2 = pd.json_normalize(Sell1)
except AttributeError as err:
    Sell2 = pd.json_normalise(Sell1)
except TypeError as err:
    Sell2 = pd.json_normalise(Sell1)    

Sell3 = pd.json_normalize(Sell1['securitiesAccount']['positions'])
Sell4 = pd.DataFrame(Sell2['securitiesAccount.positions'])
Sell5cash = pd.DataFrame(Sell2['securitiesAccount.initialBalances.totalCash'])
cash = Sell5cash['securitiesAccount.initialBalances.totalCash']
marketvalue = sum(Sell3['marketValue'])
GPB4_symbol = pd.DataFrame(Sell3['instrument.symbol'])
GPB4_quantity = pd.DataFrame(Sell3['previousSessionLongQuantity'])
GPB4_assettype = pd.DataFrame(Sell3['instrument.assetType'])
GPB5_mv= pd.DataFrame(Sell3['marketValue'])
GPB6_mvs = GPB5_mv.join(GPB4_symbol)
GPB7_mvs = GPB6_mvs.join(GPB4_quantity)
GPB8_mvs = GPB7_mvs.join(GPB4_assettype)
GPB8 = pd.DataFrame(GPB8_mvs)
#revised dataframes
GPB_S = GPB8[(GPB8['instrument.assetType'] == 'EQUITY')]
GPB_S.to_csv(r'[PATH]')
GPB_O = GPB8[(GPB8['instrument.assetType'] == 'OPTION')]
GPB_S.to_csv(r'[PATH]')
GPB_C = GPB8[(GPB8['instrument.symbol'] == 'MMDA1')]

#optional date variables to import from listener.py
#start = lb.s_date_list
#end = lb.e_date_list
#dates = pd.date_range(start, end)
#df1 = pd.DataFrame(index=dates)

#STOCK DATAFRAME (for buy function only, commended out but kept to preserve as a backup)
#url = "https://www.sec.gov/include/ticker.txt"
#First source of stocks is url containing thousands of stocks, so it is disabled by default 
#s = pd.read_csv(url, sep = '\t', names=["Symbol", "cusip"])
#second source is positions dataframe output from above, accessing targetvariables csv
stock_list_s = pd.read_csv(r'[PATH]')
stock_list_o = pd.read_csv(r'[PATH]')
#Create Symbols From Dataset
Symbols_s = stock_list_s['instrument.symbol'].tolist()
Symbols_o = stock_list_o['instrument.symbol'].tolist()
#create a target symbols empty list
target_symbols_s = []
target_symbols_o = []
# create empty dataframe

# process historical price dataframes for stocks and options, produce target symbols
for i in Symbols_s:  
    stock = TDSession.get_price_history(symbol=i, period_type='month', period= 1, frequency_type='daily', frequency=1)
    stock_df = pd.DataFrame(stock['candles'])
    df2 = pd.DataFrame()
    df2["Date"] = stock_df['datetime']
    df2["Close"] = stock_df['close']
    df2["Volume"] = stock_df['volume']
    df2["MA10"] = stock_df['close'].rolling(4).mean()
    df2["Symbol"] =stock['symbol']
    bool = df2["MA10"].iloc[-1] > df2["Close"].iloc[-1]  ##create Boolean to filter out target stocks
    if bool == True:
            target_list = stock['symbol']
            target_symbols_s.append(target_list)

try:            
    for i in Symbols_o:
        stock = TDSession.get_price_history(symbol=i, period_type='month', period= 1, frequency_type='daily', frequency=1)
        stock_df = pd.DataFrame(stock['candles'])
        df2 = pd.DataFrame()
        df2["Date"] = stock_df['datetime']       
        df2["Close"] = stock_df['close']
        df2["Volume"] = stock_df['volume']
        df2["MA10"] = stock_df['close'].rolling(4).mean()
        df2["Symbol"] =stock['symbol']
        bool = df2["MA10"].iloc[-1] > df2["Close"].iloc[-1]  ##create Boolean to filter out target stocks
        if bool == True:
                target_list = stock['symbol']
                target_symbols_o.append(target_list)            

except KeyError as err:
    print("No owned options to sell at the moment")

try:
    for i in target_symbols_s:
        quotes_response_s = TDSession.get_quotes(instruments = [i])
        quotes_df_s = quotes_response_s[i]['bidPrice']
    for i in target_symbols_o:
        quotes_response_o = TDSession.get_quotes(instruments = [i])
        quotes_df_o = quotes_response_o[i]['bidPrice']
except KeyError as err:
    print("No symbols warranting selling")



# Define order templates to call later in buying and selling

for i in target_symbols_s:  #this is the order template for placing a stock sale

    def executesell_s():
        order_template_s = sell_limit_enter = {
        "orderType": "LIMIT",
        "session": "NORMAL",
        "duration": "DAY",
        "price": quotes_df_s,
        "orderStrategyType": "SINGLE",
        "orderLegCollection": [
            {
                "instruction": "SELL",
                "quantity": GPB4_quantity,
                "instrument": {
                    "symbol": i,
                    "assetType": "EQUITY"
                }
                }
            ]
        }
        # Place the Order.
        order_response = TDSession.place_order(
        account=lesl.td_account,
        order= order_template_s
        )
        # Print the Response.
        pprint.pprint(order_response)
    executesell_s()

#Now define second template for selling options in portfolio:

for i in target_symbols_o:  #this is the order template for placing an option sale

    def executesell_o():
        order_template_o = sell_limit_enter = {
        "complexOrderStrategyType": "NONE",
        "orderType": "LIMIT",
        "session": "NORMAL",
        "price": quotes_df_o,
        "duration": "DAY",
        "orderStrategyType": "SINGLE",
        "orderLegCollection": [
            {
            "instruction": "SELL_TO_CLOSE",
            "quantity": GPB4_quantity,
            "instrument": {
                "symbol": i,
                "assetType": "OPTION"
                }
            }
        ]
        }
                # Place the Order.
        order_response = TDSession.place_order(
        account=lesl.td_account,
        order= order_template_o
        )
        # Print the Response.
        pprint.pprint(order_response)
        executesell_o()



def print_sell_log():
    print("Initializing Sell.py: Analyzing portfolio...")
    print("The market value of the portfolio is: ")
    print(marketvalue)
    print("The contents of portfolio are: ")
    print(GPB8)
    print("The current cash balance is: ")
    print(cash)
    print("The revised dataframe for stocks is: ")
    print(GPB_S)
    print("The revised dataframe for options is: ")
    print(GPB_O)
    print("The revised dataframe for cash is: ")
    print(GPB_C)
    print("The target symbols of owned stocks are: ")
    if GPB_S.empty:
        print("There are no owned stocks at the moment")
    else:
        print(GPB_S)
    print("The options owned are: ")
    if GPB_O.empty:
        print("There are no owned options")
    else:
        print(GPB_O)
    print("The revised dataframe for cash is: ")
    print(GPB_C)
    print("The target symbols of owned stocks are: ")
    if len(target_symbols_s) == 0:
        print("No target symbols of owned stocks")
    else:
        print(target_symbols_s)        
    print("The target quote prices for the target symbols of owned stocks are: ")
    try:
        print(target_symbols_s,": ",quotes_df_s)
    except NameError:
        print("No symbols of owned stocks in portfolio warranting selling")
    print("The passed symbols of owned stocks to sell are: ")    
    if len(target_symbols_s) == 0:
        print("No target quote prices of owned stocks to sell")   
    else:
        print(target_symbols_s,": ",df2.tail(5))
    print("The target symbols of owned options are: ")
    if len(target_symbols_o) == 0:
        print("No owned stock options in target symbols")
    else:
        print(target_symbols_o)
    print("The target quote prices for the target symbols of owned options are: ")
    try:
        print(target_symbols_o,": ",quotes_df_o)
    except NameError:
        print("No symbols in portfolio warranting selling")
    print("The passed symbols of owned options to sell are: ")    
    if len(target_symbols_o) == 0:
        print("No target quote prices in owned options")
    else:
        print(target_symbols_o,": ",df2.tail(5))
  
    print("Initiating stock and option buy order execution function...")

print_sell_log()
