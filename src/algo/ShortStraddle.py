from src.broker.fyers.fyers import Fyers
import time
from src.algo.FyerTrade import FyersTrade


# Short Stranddle
class ShortStraddle:
    def __init__(self, index="NSE:NIFTY50-INDEX", trade_mode="PAPER", qty=1, initial_sl_percent=30, trail_percent=5):
        self.index = index
        self.qty = qty
        self.initial_sl_percent = initial_sl_percent / 100
        self.trail_percent = trail_percent / 100
        self.trade_mode = trade_mode
        self.fyer_trade = FyersTrade(trade_mode, index)

    def trail_stop_loss(self, symbol, entry_price, initial_sl):
        """Implements trailing stop loss based on percentage."""
        sl_price = initial_sl  # Start with initial SL
        while True:
            try:
                data = self.fyers.quotes({"symbols": symbol})
                ltp = data["d"][0]["v"]["lp"]
                new_sl = ltp * (1 - self.trail_percent)

                if new_sl > sl_price:
                    sl_price = new_sl
                    print(f"🔄 SL Updated to {sl_price}")
                    self.log_trade(symbol, "SL Update", ltp, self.trail_percent, sl_price, "Trailing SL Updated")

                if ltp <= sl_price:
                    print(f"❌ Stop Loss {sl_price} hit! Closing position...")
                    self.log_trade(symbol, "STOP LOSS HIT", ltp, self.trail_percent, sl_price, "Exited")
                    self.close_position(symbol)
                    break

                time.sleep(5)

            except Exception as e:
                print(f"❌ Error in SL Trailing: {e}")

    def close_position(self, symbol):
        """Closes the open position and logs it."""
        order_data = {
            "symbol": symbol,
            "qty": self.qty,
            "type": 2,
            "side": 1,
            "productType": "INTRADAY",
            "validity": "DAY",
        }

        try:
            response = self.fyers.place_order(order_data)
            price = 95  # Assume exit price (Replace with actual API response)
            self.log_trade(symbol, "BUY", price, "-", "-", "Exited")
            return response
        except Exception as e:
            print(f"❌ Error exiting position: {e}")
            self.log_trade(symbol, "BUY", "-", "-", "-", "Exit Failed")
            return None

    def execute_trade(self):
        """Execute the strategy: Sell both CE & PE + Trail SL."""
        atm_strike = self.fyer_trade.get_atm_strike()

        if atm_strike:
            ce_symbol = f"NSE:{atm_strike}CE"
            pe_symbol = f"NSE:{atm_strike}PE"
            print(
                f"\n📢 {'Paper' if self.trade_mode.upper() == 'PAPER' else 'Real'} Trading - Selling ATM Options: {ce_symbol} & {pe_symbol}")

            # ce_order = self.fyer_trade.place_order(order_data={
            #     "symbol": ce_symbol,
            #     "qty": self.qty,
            #     "type": 2,  # Market Order
            #     "side": -1,  # Sell
            #     "productType": "MARGIN",
            #     "limitPrice": 0,
            #     "stopPrice": 0,
            #     "validity": "DAY",
            #     "disclosedQty": 0,
            #     "offlineOrder": False,
            #     "orderTag": "ATM_SELL"
            # }, initial_sl_percent=self.initial_sl_percent)
            # pe_order = self.fyer_trade.place_order(order_data={
            #     "symbol": pe_symbol,
            #     "qty": self.qty,
            #     "type": 2,  # Market Order
            #     "side": -1,  # Sell
            #     "productType": "MARGIN",
            #     "limitPrice": 0,
            #     "stopPrice": 0,
            #     "validity": "DAY",
            #     "disclosedQty": 0,
            #     "offlineOrder": False,
            #     "orderTag": "ATM_SELL"
            # }, initial_sl_percent=self.initial_sl_percent)

            # if ce_order and pe_order:
            #     # Run SL trailing in parallel for CE & PE
            #     from threading import Thread
        #         ce_thread = Thread(target=self.trail_stop_loss, args=(ce_symbol, ce_order["entry_price"], ce_order["sl_price"]))
        #         pe_thread = Thread(target=self.trail_stop_loss, args=(pe_symbol, pe_order["entry_price"], pe_order["sl_price"]))

        #         ce_thread.start()
        #         pe_thread.start()

        #         ce_thread.join()
        #         pe_thread.join()
