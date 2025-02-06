from pydantic import BaseModel
from typing import List

class ScriptDetail(BaseModel):
    name: str
    diff: int
    lots: int
    key: str

class ScriptConfig(BaseModel):
    broker_name:str
    m_exp: str
    w_exp: str
    w_m: str
    m_m: str
    rows: List[ScriptDetail]

class OptionConfig(BaseModel):
    name: str
    expiry:str
    strick_count:int
    broker:str
    expiry_type:str