import yfinance as yf
import pandas as pd
import ta
from config import PERIOD, INTERVAL, TICKERS  # Import all necessary variables

def get_intraday_data(ticker):
    """Fetch intraday data and calculate technical indicators."""
    data = yf.download(ticker, period=PERIOD, interval=INTERVAL)
    data['EMA9'] = ta.trend.ema_indicator(data['Close'], window=9)
    data['EMA21'] = ta.trend.ema_indicator(data['Close'], window=21)
    data['RSI'] = ta.momentum.rsi(data['Close'], window=14)
    macd = ta.trend.macd(data['Close'])
    data['MACD'] = macd
    data['MACD_Signal'] = ta.trend.macd_signal(data['Close'])
    data['MACD_Hist'] = ta.trend.macd_diff(data['Close'])
    data['ATR'] = ta.volatility.average_true_range(data['High'], data['Low'], data['Close'])
    return data
