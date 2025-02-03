from fastapi import FastAPI, Depends
from src.env import config
from typing_extensions import Annotated
from src.gfinance.router import gfinance
from src.algo.routers import algo
from src.web_socket.routers import socket
from src.option_data.routers import option

app = FastAPI()
from functools import lru_cache

app.include_router(gfinance)
app.include_router(algo)
app.include_router(socket)
app.include_router(option)



@app.get('/')
def home_page():
    return {"message": f"Hello ALok!"}



