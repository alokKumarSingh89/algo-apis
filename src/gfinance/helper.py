import yfinance as yf
import pandas as pd
from fastapi.responses import JSONResponse

def gf_ltp(symbol):
    data_frame = yf.download(symbol, period="1y", interval="1d")
    return round(data_frame.iloc[-1]["Close"].to_dict()[symbol],2)

# Fetch consolidated stock list for 500
def fetch_script_csl(data):
    stock_list = {
        "script":[],
        "current":[],
        "5DMA":[],
        "20DMA":[],
        "50DMA":[],
        "100DMA":[],
        "200DMA":[],
        "52_high":[],
        "52_low":[],
        "date_high":[],
        "date_low":[],
    }
    count = 0
    for key, value in data.items():
        a = value.split(":")
        script_name = ""
        
        if len(a) == 1:
            script_name = a[0]+".NS"
        else:
            script_name = a[1]+".NS"
        try:
            data_frame = yf.download(script_name, period="1y", interval="1d")
            data_frame['5_DMA'] = data_frame['Close'].rolling(window=5).mean()
            data_frame['20_DMA'] = data_frame['Close'].rolling(window=20).mean()
            data_frame['50_DMA'] = data_frame['Close'].rolling(window=50).mean()
            data_frame['100_DMA'] = data_frame['Close'].rolling(window=100).mean()
            data_frame['200_DMA'] = data_frame['Close'].rolling(window=200).mean()
            
            stock_list["current"].append(data_frame['Close'].iloc[-1].to_dict()[script_name])

            stock_list["5DMA"].append(data_frame['5_DMA'].iloc[-1])
            stock_list["20DMA"].append(data_frame['20_DMA'].iloc[-1])
            stock_list["50DMA"].append(data_frame['50_DMA'].iloc[-1])
            stock_list["100DMA"].append(data_frame['100_DMA'].iloc[-1])
            stock_list["200DMA"].append(data_frame['200_DMA'].iloc[-1])
            stock_list["52_high"].append(data_frame['High'].max().iloc[-1])
            stock_list["52_low"].append(data_frame['Low'].min().iloc[-1])
            stock_list["date_high"].append(data_frame['High'].idxmax().iloc[-1])
            stock_list["date_low"].append(data_frame['Low'].idxmin().iloc[-1])
            stock_list["script"].append(script_name)
        except Exception  as e:
            print(script_name, e)
    df = pd.DataFrame(stock_list)
    df["date_high"] = df['date_high'].dt.strftime('%Y-%m-%d')
    df["date_low"] = df['date_low'].dt.strftime('%Y-%m-%d')
    df = df.fillna('')
    return df


def fetch_script(data, period="1y", interval="1d"):
    for key, value in data.items():
        a = value.split(":")
        script_name = ""
        
        if len(a) == 1:
            script_name = a[0]+".NS"
        else:
            script_name = a[1]+".NS"
        try:
            data_frame = yf.download(script_name, period=period, interval=interval)
            data_frame = data_frame.fillna('')
            return data_frame
        except Exception  as e:
            print(script_name, e)
    
    
    