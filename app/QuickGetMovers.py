#successfully run on 9.15.21
import pandas as pd
from config import CONSUMER_KEY, REDIRECT_URI, JSON_PATH
from td.client import TDClient
import loghog

#Create a new instance of the broker client
TDSession = TDClient(
    client_id= CONSUMER_KEY,
    redirect_uri= REDIRECT_URI,
    credentials_path= JSON_PATH)
#Get daily movers whose price is below 80
getmovers = TDSession.get_movers("$DJI", "up", "value")
getmovers2 = TDSession.get_movers("$DJI", "down", "value")
gm = pd.json_normalize(getmovers)
gm2 = pd.json_normalize(getmovers2)
gm2.T
#gmt = gm.loc[gm['last'] < 80]
print(gm[['change','last', 'symbol', 'totalVolume']])
print(gm2[['change','last', 'symbol', 'totalVolume']])
#print(gmt)
#move to csv
gm['symbol'].to_csv(r'C:\Users\Spark\Desktop\projects\tradesetandforget\csvs\mover_list.csv')
#print(getmovers)

gm3 = pd.DataFrame()
gm4 = pd.DataFrame()
gm3['Cumulative gain'] = pd.DataFrame.sum(gm[["change"]])
gm4['Cumulative loss'] = pd.DataFrame.sum(gm2[["change"]])
print(gm3)
print(gm4)

loghog