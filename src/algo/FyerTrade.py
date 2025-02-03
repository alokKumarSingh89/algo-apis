import time
import csv
import os
import requests
from datetime import datetime
from src.broker.fyers.fyers import Fyers


class FyersTrade():
    def __init__(self, tade_type, symbol):
        self.tade_type = tade_type
        # CSV Log File
        self.symbol = symbol
        today = datetime.now().strftime("%Y-%m-%d")
        self.log_file = f"{today}_{tade_type}_trade_log.csv"
        self.fyers = Fyers().get()
        self.initialize_csv()

    def initialize_csv(self):
        """Creates a CSV log file with headers if it doesn’t exist."""
        if not os.path.exists(self.log_file):
            with open(self.log_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["Timestamp", "symbol", "Order Type", "Quantity","Entry Price","SL %", "SL Price", "Status"])

    def log_trade(self, option_symbol, order_type, qty , entry_price, sl_percent, sl_price, status):
        """Logs trade details to a CSV file."""
        with open(self.log_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                option_symbol,
                order_type,
                qty,
                entry_price,
                f"{sl_percent * 100}%",
                sl_price,
                status
            ])
        print(
            f"📝 Trade logged: {order_type} {option_symbol} @ {entry_price} | SL: {sl_price} ({sl_percent * 100}%) | {status}")

    @staticmethod
    def get_ltp(symbol):
        resp = requests.get("http://localhost:9000/socket/script?script_name=" + symbol)
        return resp.json()

    def get_atm_strike(self):
        """Fetches the ATM strike price for the selected index."""
        try:
            data = self.get_ltp(self.symbol)
            atm_strike = round(data["ltp"] / 50) * 50
            print(f"✅ ATM Strike Price for {self.symbol}: {atm_strike} and current: {data['ltp']}")
            return atm_strike
        except Exception as e:
            print(f"❌ Error fetching ATM Strike: {e}")
            return None

    def get_strike_ltp(self, symbol):
        """Fetches the ltp strike price for the selected index."""
        try:
            data = self.get_ltp(symbol)
            print(f"✅ LPT Strike Price for {symbol}: {data['ltp']}")
            return data['ltp']
        except Exception as e:
            print(f"❌ Error fetching LTP Strike: {e}")
            return None

    def place_sell_order(self, order_data, initial_sl_percent):
        """Places a market sell order and logs the trade."""
        try:
            response = self.fyers.place_order(order_data)
            # Assume filled price is 100 (Replace with actual API response)
            entry_price = self.get_ltp(order_data["symbol"]["ltp"])
            sl_price = entry_price * (1 - initial_sl_percent)  # SL calculation in %

            self.log_trade(order_data["symbol"], "SELL", order_data["qty"], entry_price, initial_sl_percent, sl_price,
                           "Executed")
            return {"entry_price": entry_price, "sl_price": sl_price, "id": response["id"]}
        except Exception as e:
            print(f"❌ Error placing sell order: {e}")
            self.log_trade(order_data["symbol"], "SELL", order_data["qty"], "-", initial_sl_percent, "-", "Failed")
            return None

    def place_sell_paper_order(self, order_data, initial_sl_percent):
        """Places a market sell order and logs the trade."""
        try:
            entry_price = self.get_ltp(order_data["symbol"]["ltp"])
            sl_price = entry_price * (1 - initial_sl_percent)  # SL calculation in %

            self.log_trade(order_data["symbol"], "SELL", order_data["qty"], entry_price, initial_sl_percent, sl_price,
                           "Executed")
            return {"entry_price": entry_price, "sl_price": sl_price, "id": -1000}
        except Exception as e:
            print(f"❌ Paper Trading Error placing sell order: {e}")
            self.log_trade(order_data["symbol"], "SELL", order_data["qty"], "-", initial_sl_percent, "-", "Failed")
            return None

    def place_order(self, order_data, initial_sl_percent):
        if self.tade_type == "PAPER":
            return self.place_sell_paper_order(order_data, initial_sl_percent)
        elif self.tade_type == "REAL":
            return self.place_sell_order(order_data, initial_sl_percent)
        else:
            print(f"❌ Sorry, trade_order not defined")
            return None
