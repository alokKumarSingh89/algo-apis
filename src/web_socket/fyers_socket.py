
from src.broker.fyers.fyers import Fyers
from src.firebase.firebase import load_code
from fyers_apiv3.FyersWebsocket import data_ws
from datetime import datetime

def start_socket(symbolList, fyer_token, socket_data):
    print("Start Point")
    for symbol in symbolList:
        socket_data[symbol] = {
            "open": [],
            "close": [],
            "high": [],
            "low": [],
            "date": [],
            "volumn": []
        }
    def onmessage(message):
        """Callback function to handle incoming messages from the FyersDataSocket WebSocket.Parameters:
        message (dict): The received message from the WebSocket."""
        
        try:
            if message.get("ltp") is not None:
                script_symbol = message.get("symbol")
                
                if message.get('last_traded_time') is not None:
                    last_traded_time = message.get('last_traded_time')
                    last_traded_date = datetime.fromtimestamp(last_traded_time).strftime('%d-%m-%y %H:%M:%S')
                    socket_data[script_symbol]["date"].append(last_traded_date)
                elif message.get("exch_feed_time") is not None:
                    last_traded_time = message.get('exch_feed_time')
                    last_traded_date = datetime.fromtimestamp(last_traded_time).strftime('%d-%m-%y %H:%M:%S')
                    socket_data[script_symbol]["date"].append(last_traded_date)
                ltp = message.get('ltp')
                vol_traded_today = message.get("vol_traded_today") or 0
                socket_data[script_symbol]["open"].append(ltp)
                socket_data[script_symbol]["close"].append(ltp)
                socket_data[script_symbol]["high"].append(ltp)
                socket_data[script_symbol]["low"].append(ltp)
                socket_data[script_symbol]["volumn"].append(vol_traded_today)
            print("Response:", ltp, script_symbol)
        except Exception as e:
            print(e)
        
    def onerror(message):
        """Callback function to handle WebSocket errors.Parameters:message (dict): The error message received from the WebSocket."""
        print("Error:", message) 
    
    def onclose(message):
        """Callback function to handle WebSocket connection close events."""
        print("Connection closed:", message)  
    
    def onopen():
        """Callback function to subscribe to data type and symbols upon WebSocket connection."""
            # Specify the data type and symbols you want to subscribe to
        # data_type = "OnGeneral"
        data_type = "SymbolUpdate"
        print("dd")
        fyers.subscribe(symbols=symbolList, data_type=data_type)
        fyers.keep_running()
        
    fyers = data_ws.FyersDataSocket(
        access_token=fyer_token,  # Access token in the format "appid:accesstoken"
        log_path="",  # Path to save logs. Leave empty to auto-create logs in the current directory.
        litemode=False,  # Lite mode disabled. Set to True if you want a lite response.
        write_to_file=False,  # Save response in a log file instead of printing it.
        reconnect=True,  # Enable auto-reconnection to WebSocket on disconnection.
        on_connect=onopen,  # Callback function to subscribe to data upon connection.
        on_close=onclose,  # Callback function to handle WebSocket connection close events.
        on_error=onerror,  # Callback function to handle WebSocket errors.
        on_message=onmessage  # Callback function to handle incoming messages from the WebSocket.
    )
    fyers.connect()
    return fyers
     
class FyerSocket():
    def __init__(self, socket_data):
        fyers = Fyers()
        self.fyer_data = fyers.get()
        self.fyer_token = fyers.get_save_token()
        self.isRuning = False
        self.script = load_code("options", "fyers")
        self.fyers = None
        self.symbolList = []
        self.socket_data = socket_data
        self.script_config = load_code("script_config", "fyers")
    def get_strick(self, value):
        response = self.fyer_data.optionchain(data = {
                "symbol":value,
                "strikecount":15,
                "timestamp": ""
            })
        symbolList = []
        
        for data in response["data"]["optionsChain"]:
            symbolList.append(data["symbol"])
        return symbolList
    
    def start(self):
        self.isRuning = True
        self.symbolList = []
        # print(self.script_config)
        for sc in self.script.values():
            if sc is None:
                continue
            exp = self.script_config[f'{sc["expiry_type"]}_exp']
            months = self.script_config[f'{sc["expiry_type"]}_month'].split(",")
            script = self.script_config[sc["name"]]
            expiry = sc["expiry"].split("-")
            Ex = script["key"].split(":")[0]
            Ex_UnderlyingSymbol = sc["name"]
            YY = expiry[0][-2:]
            M = expiry[0]
            print(sc, exp, months, script)
        # for key, value in self.script.items():
        #     data = self.get_strick(value)
        #     self.symbolList = self.symbolList + data
        # self.fyers = start_socket(self.symbolList, self.fyer_token, self.socket_data)
    def restart(self):
        if self.isRuning == True:
            self.stop()
            self.start();
        else:
            self.start();
            self.isRuning = True
    
    def stop(self):
        if self.fyers is not None and self.fyers.is_connected():
                self.fyers.unsubscribe()
        self.isRuning = False
        
    def get_socket_data(self):
        global socket_data
        return socket_data
    
    