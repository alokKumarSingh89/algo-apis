from fastapi import APIRouter, Body
from src.env import config
from src.broker.fyers.fyers import Fyers
from pydantic import BaseModel, Field
from typing import List
import requests

class Script(BaseModel):
    script: str = Field()
    expiry:str = Field()
    
    
fyers = Fyers().get()
option = APIRouter(prefix="/option", tags=["Option Data pull"] )

def get_ltp(script):
    requests.get("")

@option.post("")
def create_option_data(scripts: List[Script] = Body(...), broker="fyers"):
    for script in scripts:
        print(script.script,script.expiry)
    # data = {
    #     "symbol":"NSE:NIFTY50-INDEX",
    #     "strikecount":1,
    #     "timestamp": ""
    # }
    # response = fyers.optionchain(data=data);
    # option_list = [data["symbol"] for data in response["data"]["optionsChain"]]
    # print(option_list)