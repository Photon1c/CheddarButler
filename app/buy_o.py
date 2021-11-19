## from stocks and options programs, import list of symbols to execute buy trades for.
import pandas as pd
import datetime as dt
from config import CONSUMER_KEY, REDIRECT_URI, JSON_PATH
from td.client import TDClient
import lesl
from sell import cash, marketvalue
from buy_s import target_symbols

#Create a new instance of the client
TDSession = TDClient(client_id= CONSUMER_KEY,
    redirect_uri= REDIRECT_URI,
    credentials_path= JSON_PATH)
o_df = pd.DataFrame()

target_symbols_o = []

def get_optionchain():
    for i in target_symbols:
        o_dict1 = TDSession.get_options_chain(option_chain={'symbol': i, 'strikeCount': 1, '2021-11-19': '2021-11-26'})
        o_df1 = pd.DataFrame.from_dict(o_dict1)
        o_series1 = o_df1['callExpDateMap']
        o_dict2 = o_series1.to_dict()
        o_df2 = pd.DataFrame(o_dict1, columns=["Symbol",'Expiration Date', 'Strike Price' , 'Ask Price', 'Volatility'])
        o_df2["Symbol"] = o_df1['symbol']
        o_df2["Expiration Date"] =  o_df1.index
        o_df3 = pd.DataFrame.from_dict(o_dict2, orient="index").stack().to_frame()
        # to break out the lists into columns
        o_df4 = pd.DataFrame(o_df3[0].values.tolist(), index=o_df3.index)
        o_array = o_df4.values
        o_dict3 = dict(enumerate(o_array.flatten(),))
        asklists = []
        volatilitys = []
        strikeprices = []
        for row in o_dict3:
            a = o_dict3[row]['ask']
            asklists.append(a)
            v = o_dict3[row]['volatility']
            volatilitys.append(v)
            st = o_dict3[row]['strikePrice']
            strikeprices.append(st)
        o_df2["Strike Price"] = strikeprices
        o_df2["Ask Price"] = asklists
        o_df2["Volatility"] = volatilitys    
        o_df2_o = o_df2.loc[o_df2["Ask Price"] < .75]
        o_df.append(o_df2_o)
        target_list_o = o_df2_o['Symbol']
        target_symbols_o.append(target_list_o)
        if o_df2_o.empty:             
            print("Stock option for ", i, " is not within buying parameters")
        else:
            print(o_df2_o)
            o_df2_o.to_csv(r"C:\Users\Spark\Desktop\projects\tradesetandforget\app\logs\optionblueberries.csv", 'a')

def execute_optionbuy():

        order_template = buy_limit_enter =  {
        "complexOrderStrategyType": "NONE",
        "orderType": "LIMIT",
        "session": "NORMAL",
        "price": 3,
        "duration": "DAY",
        "orderStrategyType": "SINGLE",
        "orderLegCollection": [
            {
            "instruction": "BUY_TO_OPEN",
            "quantity": int(cash/marketvalue),
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
        order= order_template
        )
        # Print the Response.
        pprint.pprint(order_response)
    #executesell_o()

if __name__ == '__main__':
    try:
        get_optionchain()
    except TypeError:
        get_optionchain()
    print('There is currently {}% '.format(int(cash)//int(marketvalue)), 'of cash in portfolio')
    print(cash//marketvalue)

