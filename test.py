import yfinance as yf
import pandas as pd
import numpy as np

# Replace 'AAPL' with your stock ticker symbol
ticker = "RELIANCE.NS"

data = yf.download(ticker, period="1y", interval="1d")

data['5_DMA'] = data['Close'].rolling(window=5).mean()
data['20_DMA'] = data['Close'].rolling(window=20).mean()
data['50_DMA'] = data['Close'].rolling(window=50).mean()
data['100_DMA'] = data['Close'].rolling(window=100).mean()
data['200_DMA'] = data['Close'].rolling(window=200).mean()

# Display the latest data with DMA values
latest_data = data[['Close', '5_DMA', '20_DMA', '50_DMA', '100_DMA', '200_DMA']].tail(1)
# Fetch the historical data for the past year (52 weeks)
# print(f"The 52-week high for {ticker} is: {latest_data} and high: {data['High'].max()}")
print("\n")
print("dd",data['5_DMA'].iloc[-1])
