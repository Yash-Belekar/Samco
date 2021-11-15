import pandas as pd
import pandas_datareader.data as web
import datetime
from datetime import date, timedelta
import numpy as np
from snapi_py_client.snapi_bridge import StocknoteAPIPythonBridge
import json
import requests
import os,sys
import math
import time
import websocket

# Connect function is used to connect to the API
def connect():
    global samco,session
    samco=StocknoteAPIPythonBridge()
    login=samco.login(body={"userId":'',
                            'password':'',
                            'yob':''})
    creds=eval(login)
    samco.set_session_token(creds['sessionToken'])
    session = (creds['sessionToken'])
    today=date.today()

connect()

## Message received on quote update is sent here as an msg.
def on_message(ws, msg):
    msg1 = json.loads(msg)
    sym = msg1['response']['data']['sym']
    ltp = float(msg1['response']['data']['ltp'])

        
def on_error(ws, error):
    print (error)

def on_close(ws):
    print ("Connection Closed")

## On open. Feed the symbolcode of the stock or instrument you want to subscribe to. here I have added 53595_NFO (Nifty future).
## Refer to scripmaster attached for symbolcode
def on_open(ws):
    print ("Sending json")
    global subscribe_list,symbol_dict
    symbol_dict,symbol_dict2,subscribe_list = {},{},[{'symbol':'53597_NFO'},{'symbol':'53595_NFO'}]
    data='{"request":{"streaming_type":"quote", "data":{"symbols":'+json.dumps(subscribe_list)+'}, "request_type":"subscribe", "response_format":"json"}}'
    ws.send(data)
    ws.send("\n")

headers = {'x-session-token': session }

websocket.enableTrace(True)

ws = websocket.WebSocketApp("wss://stream.stocknote.com", on_open = on_open, on_message = on_message, on_error = on_error, on_close = on_close, header = headers)

ws.run_forever()

   
    
