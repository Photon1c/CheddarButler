#successfully run on 7.28.21
import pandas as pd
from config import CONSUMER_KEY, REDIRECT_URI, JSON_PATH
import lesl
from td.client import TDClient
import sell
#Create a new instance of the client
TDSession = TDClient(
    client_id= CONSUMER_KEY,
    redirect_uri= REDIRECT_URI,
    credentials_path= JSON_PATH)
