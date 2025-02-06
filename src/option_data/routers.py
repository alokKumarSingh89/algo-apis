from fastapi import APIRouter, Body
from src.env import config
from src.broker.fyers.fyers import Fyers
from pydantic import BaseModel, Field
from typing import List
from src.firebase.firebase import add_collection, load_code, get_all_document, delete_field
from src.option_data.model import ScriptConfig, OptionConfig, ScriptDetail
import json


    
    
fyers = Fyers().get()
option = APIRouter(prefix="/option", tags=["Option Data pull"] )

@option.post("")
def create_option_data(scripts: List[OptionConfig] = Body(...)):
    try:
        for script in scripts:
            add_collection("options", script.broker,{f'{script.expiry}-{script.name}': script.model_dump()})
    except Exception as e:
        return {"message": e.with_traceback()}
    
    
@option.get("")
def get_option_list():
    return get_all_document("options")
    
@option.delete("/{id}")
def delete_option(id:str, broker:str):
    delete_field("options", broker, id)
    return {"messeage":"success"}
    

@option.post("/script_config")
def create_script_config(data: ScriptConfig):
    collection_name = "script_config"
    document = data.broker_name
    collection = {
        "W_exp":data.w_exp,
        "W_month":data.w_m,
        "M_exp":data.m_exp,
        "M_month":data.m_m}
    for sc in data.model_dump()["rows"]:
        collection[sc["name"]]  = sc
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
    