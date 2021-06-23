from binance.client import Client
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

api_key="secret"
api_secret="secret"
client=Client(api_key,api_secret)



# fetch 30 minute klines for the last month of 2017
klines = client.get_historical_klines("BTTUSDT", Client.KLINE_INTERVAL_1HOUR, "1 Dec, 2020", "1 Jul, 2021")
my_data=[]

for item in klines:   
    my_data=my_data+[item[4]]


## convert to dataframe
my_data=pd.DataFrame(my_data)
my_data.rename(columns = {0: 'price'}, inplace = True)
exp1 = my_data.ewm(span=12, adjust=False).mean()
exp2 = my_data.ewm(span=26, adjust=False).mean()
macd = exp1-exp2
exp3 = macd.ewm(span=9, adjust=False).mean()

my_data["macd"]=macd
my_data["exp3"]=exp3
my_data["diff"]=my_data["macd"]-my_data["exp3"]



file=open("results.txt","w")

## export data
for index, row in my_data.iterrows():
    file.write(str(row['price'])+"   "+str(row['diff']))
    file.write('\n')

