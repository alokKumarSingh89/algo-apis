from fastapi import APIRouter, HTTPException
from starlette import status
from fastapi.encoders import jsonable_encoder
from src.firebase.firebase import add_nse_code, load_code
from src.gfinance.helper import fetch_script_csl

consolidated_list = "nse_script"

gfinance: APIRouter = APIRouter(
    prefix="/gfinance",
    tags=["Google Finance"]
)

@gfinance.get("/")
def welcome():
    return {"title": "Welcome Google"}


@gfinance.post("/scripts")
def add_script(nsecode):
    try:
        add_nse_code(consolidated_list,"nsecode",nsecode)
        return {"nsecode":nsecode, "message":"added"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Not strategy avail for given input')
    
@gfinance.get("/consolidated_list_500")
def get_consolidated_list():
    data = load_code(consolidated_list,"nsecode")
    return fetch_script_csl(data)