from fastapi import APIRouter, HTTPException
import pandas as pd
from datetime import datetime

from src.config import settings
from src.web_socket.fyers_socket import FyerSocket
socket = APIRouter(
    prefix="/socket",
    tags=["Socket API"])


# TEsting
socket_data = {}
web_socket = FyerSocket(socket_data)
MODE = settings.MODE

@socket.get("")
def start_socket(mode):
    # Need to change the logic
    print(mode)
    if mode == "socket":
        web_socket.restart()
    else:
        return "Not enable"
  
  
@socket.get("/data")
def return_socket_data():
    return socket_data

@socket.get("/script")
def get_ltp(script_name: str):
    if script_name in socket_data:
        return {"ltp":socket_data[script_name]["close"][-1]}
    return {"ltp":-1000}

@socket.get("/script_ltps")
def get_script_data(script_name: str):
    if script_name in socket_data:
        return socket_data[script_name]
    return None

@socket.get("/save")
def save_socket_data():
    records = None
    dataframe = None
    if len(socket_data.keys()) == 0:
        return "No Data"
    for key, value in socket_data.items():
        if records is None:
            records = value;
        else:
            records["scripts"] = records["scripts"] + value["scripts"]
            records["open"] =records["open"] + value["open"]
            records["close"] = records["close"] +value["close"]
            records["low"] = records["low"] + value["low"]
            records["high"] = records["high"] + value["high"]
            records["volumn"] =  records["volumn"]+value["volumn"]
            records["date"] = records["date"] + value["date"]
    
    try:
        dataframe = pd.DataFrame(records)
        dataframe.fillna('')
        filename = datetime.today().strftime('%Y:%m:%d')
        dataframe.to_csv(f"{filename}.csv")
    except Exception as e:
        print(e)
    
    return records
