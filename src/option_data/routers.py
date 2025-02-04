from fastapi import APIRouter, Body
from src.env import config
from src.broker.fyers.fyers import Fyers
from pydantic import BaseModel, Field
from typing import List
from src.firebase.firebase import add_collection, load_code
from src.option_data.model import ScriptConfig, OptionConfig, ScriptDetail
import json


    
    
fyers = Fyers().get()
option = APIRouter(prefix="/option", tags=["Option Data pull"] )

script_config = {
    
    "Fyers":{
        "W":{"exp":"{Ex}:{Ex_UnderlyingSymbol}{YY}{M}{dd}{Strike}{Opt_Type}","month":["1","2","3","4","5","6","7","8","9","O","N","D"]},
        "M":{"exp":"{Ex}:{Ex_UnderlyingSymbol}{YY}{MMM}{Strike}{Opt_Type}","month":["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]},
        "Bank Nifty":{"name":"NSE:NIFTYBANK-INDEX", "diff":100,"key":"BANKNIFTY"},
        "Nifty":{"name":"NSE:NIFTY50-INDEX", "diff":50, "key":"NIFTY"}
    }
}



@option.post("")
def create_option_data(scripts: List[OptionConfig] = Body(...)):
    try:
        broker_list = [script.broker for script in scripts]
        script_list = [script.name for script in scripts]
        broker_configs = {}
        for broker in broker_list:
            broker_config = get_script_config(broker)
            broker_configs[broker] = broker_config

        data = {
            "symbols":",".join(script_list)
        }
        respose = fyers.quotes(data)
        
        
        ltps = {}
        for symbol in respose['d']:
            ltps[symbol['n']] = symbol['v']['lp']

        for script in scripts:
            broker_config: dict = broker_configs[script.broker]
            date = script.expiry.split("-")
            current_script: ScriptDetail = broker_config[script.expiry]
            strick_diff  = current_script['diff']
            script_name = f'{current_script["exchange"]}:{current_script["name"]}'
            ltp = ltps[script_name]
            atm_strike = round(ltp / strick_diff) * strick_diff
            exp: str = broker_config[script.expiry_type]["exp"]
            months = broker_config[script.expiry_type]["month"].split(",")
            Ex = current_script["exchange"]
            selected_month = int(date[1])
            Ex_UnderlyingSymbol = current_script['key']
            YY = date[0][-2:]
            M = months[selected_month-1]
            MMM = months[selected_month-1]
            dd = date[-1]
            dd = dd.zfill(2)
            strick_list = {} 
            strick_list[script_name] = script_name
            for i in range(script.strick_count):
                ce = atm_strike + i*strick_diff
                pe = atm_strike - i*strick_diff
                ce_strick = exp.format(Ex=Ex,Ex_UnderlyingSymbol=Ex_UnderlyingSymbol,YY=YY, M=M, MMM=MMM,dd=dd,Strike=ce,Opt_Type="CE")
                pe_strick = exp.format(Ex=Ex,Ex_UnderlyingSymbol=Ex_UnderlyingSymbol,YY=YY, M=M, MMM=MMM,dd=dd,Strike=pe,Opt_Type="PE")
                strick_list[str(ce)] = ce_strick
                strick_list[str(pe)] = pe_strick
            add_collection("options", script.broker,{script.expiry: strick_list})
    except Exception as e:
        return {"message": e.with_traceback()}
    
    


@option.post("/script_config")
def create_script_config(data: ScriptConfig):
    collection_name = "script_config"
    document = data.broker_name
    collection = {
        "W":{
            "exp":data.w_exp,
            "month":data.w_m
        },
        "M":{
            "exp":data.m_exp,
            "month":data.m_m
        },
        
    }
    for sc in data.model_dump()["rows"]:
        collection[sc["expiry"]]  = sc
    add_collection(collection_name,document, collection)

@option.get("/script_config")
def get_script_config(broker):
    if broker is None:
        return {}
    collection_name = "script_config"
    data = load_code(collection_name, broker)
    return data

@option.get("/broker_list")
def get_broker_list():
    data = load_code("broker","list")
    return data
    