from fastapi import FastAPI
from src.env import config
from src.gfinance.router import gfinance
app = FastAPI()

MODE = config("MODE", default="testing")

app.include_router(gfinance)

@app.get('/')
def home_page():
    return {"message": f"Hello ALok! {MODE}"}