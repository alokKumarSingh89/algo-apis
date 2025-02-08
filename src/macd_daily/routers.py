from fastapi import APIRouter
from src.firebase.firebase import add_collection, load_code
from src.etf.models import Etf
from src.gfinance.helper import fetch_script
from datetime import datetime
import pandas as pd
import os
from src.etf.helper import save_file, folder_name, paper_detail
from src.broker.fyers.fyers import Fyers
from src.gfinance.helper import gf_ltp

fyers = Fyers().get()
macd_d = APIRouter(prefix="/macd_d", tags=["MACD Based Buying"] )


@macd_d.get("")
def welcome():
    data:dict = load_code("stock_script","stocks")
    filename = f'etf_{datetime.now().strftime("%Y-%m-%d")}.csv'
    
    try:
        if os.path.exists(folder_name+"/"+filename):
            df = pd.read_csv(folder_name+"/"+filename)
            df = df.fillna('')
            df = df.drop(columns=["Unnamed: 0"])
            best_for_today = df.nsmallest(10, 'change_in_per')
            return {"small":best_for_today.to_dict(orient='records')}
        else:
            df  = fetch_script(data)
            save_file(df, filename)
            return {"data":"df"}
        
    except Exception as e:
        return {"message":e.with_traceback()}


@macd_d.post("")
def add_etf(body: Etf):
    if body.name == "":
        return {"message":"fails"}
    key = body.name.split(":")[1].split("-")[0]
    add_collection("stock_script","etf",{key: body.name})
    

@macd_d.post("/paper")
def buy_etf(etf: Etf):
    if etf.name == "":
        return {"message":"fails"}
    data:dict = paper_detail()
    print(data.get("last_trade_day"))
    if data.get("last_trade_day") is not None and data.get("last_trade_day") == str(datetime.now().date()):
        return {"message":"Done for day"}
    name = etf.name.split(".")[0]
    symbol = f"NSE:{name}-EQ"
    resp =fyers.quotes({"symbols":symbol})
    ltp = resp["d"][0]["v"]["lp"]
    amount_allowed = data["capital"]/data["div"]
    number_allowed = int(amount_allowed/ltp)
    add_collection("etf","paper",{"last_trade_day": str(datetime.now().date()),"remain_amount":(data["capital"]- number_allowed*ltp), name: {
        "number_allowed": number_allowed,
        "last_trade_day": datetime.today(),
        "price":ltp,
        "last_buy":ltp,
        "symbol":symbol,
        "invetment": number_allowed*ltp,
        "isOpen":True
    }})
    return {"message":f"{number_allowed} bought today"}

@macd_d.get("/paper")
def get_paper_detail():
    data:dict = paper_detail()
    for key, value in data.items():
        if key not in ["capital", "div", "last_trade_day"]:
            ltp = gf_ltp(key+".NS")
            data[key]["current_price"] = ltp
    
    return data
    


# Run script to save the nse code for macd:
# def execute():
#     for i in ["CIPLA","ADANIPORTS","ITCOTELS","DREDDY","HFCLIFE","TECHM","INFY","AXISBANK","BRTANNIA","BPCL","HCLTECH","TTACONSUM","HDCBANK","RASIM","ELIANCE","INUSINDBK","ICIIBANK","SUNHARMA","KOTKBANK","WIPRO","BAJFINANCE","TCS","MARUTI","ESTLEIND","SILIFE","JWSTEEL","BAAJFINSV","ASIAPAINT","SHRIAMFIN","HIDALCO","HIDUNILVR","ADNIENT","LT","HEROMOTOCO","TATAOTORS","COAINDIA","ULTACEMCO","APOLOHOSP",\
# "POWRGRID","ITC","EICHERMOT","TATSTEEL","SBIN","NTPC","ONGC","TITAN",\
# "BHARTIARTL","BEL","TRENT"]:
#         add_collection("stock_script","stocks",{i: i})
# execute()