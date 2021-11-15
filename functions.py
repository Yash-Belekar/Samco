import pandas as pd
import datetime as dt
from datetime import timedelta,date,datetime
import numpy as np
from snapi_py_client.snapi_bridge import StocknoteAPIPythonBridge
import requests,os,sys
import time

## Function used to get data of minimun 1min timeframe.timeframe == '1T'-1 min, '30T'-30 min etc.
def get_intraday_data(symbol,exchange,timeframe):
    try:
        yesterday = date.today()
        time=' 09:15:00'
        if symbol != '' or symbol != None:
            data=eval(samco.get_intraday_candle_data(symbol_name=symbol,exchange=samco.EXCHANGE_NSE, from_date=str(yesterday)+time))
            data=pd.DataFrame(data['intradayCandleData'])
            data['dateTime'] = pd.to_datetime(data['dateTime'])
            data = data.set_index('dateTime',drop=False)
            if timeframe != '1T':
                data['open']= data['open'].resample(timeframe).first()
                data['close']= data['close'].resample(timeframe).last()
                data['low']= data['low'].resample(timeframe).min()
                data['high']= data['high'].resample(timeframe).max()
                data['dateTime']=data['dateTime'].resample(timeframe).first()
            data= data.reindex(columns=data.columns)
            data.dropna(inplace=True)
            data=data.set_index(data['dateTime'])
            return data
    except Exception as e:
        print(e)

# Get historical data upto 5 years using this function. Can be used for stocks/options/futures or indexes. index_or_stock can be 'index' or anything else
def historical_data(stock,index_or_stock):
    today = str(date.today())
    prev_day = str(date.today() - timedelta(days=3200))
    if index_or_stock == 'index':
        data = eval(samco.get_index_candle_data(index_name=stock,
                                    from_date=prev_day,to_date=today))
    else:
        data=eval(samco.get_historical_candle_data(symbol_name=stock,
                    exchange=samco.EXCHANGE_NSE, from_date=prev_day,to_date=today))
    data = pd.DataFrame(data['indexCandleData'])
    data=data.rename(columns={"open": "Open", "close": "Close",
                              "high": "High", "low": "Low",'volume':'Volume'})
    data['Open']=data['Open'].astype(float)
    data['High']=data['High'].astype(float)
    data['Low']=data['Low'].astype(float)
    data['Close']=data['Close'].astype(float)
    data['Volume']=data['Volume'].astype(float)
    return data

# Connect function to connect to API
def connect():
    global samco
    samco=StocknoteAPIPythonBridge()
    login=samco.login(body={"userId":'',
                            'password':'',
                            'yob':''})
    samco.set_session_token(creds['sessionToken'])
    today=date.today()


