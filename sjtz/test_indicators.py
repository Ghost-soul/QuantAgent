import akshare as ak
import numpy
import talib
import datetime
import pandas as pd
def compute(code,period="daily",days=60):
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=days)
    #print(start_date,today)
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code, period=period, start_date=str(start_date).replace("-",""), end_date=str(today).replace("-",""), adjust="qfq")
    open = stock_zh_a_hist_df['开盘']
    high = stock_zh_a_hist_df['最高']
    low = stock_zh_a_hist_df['最低']
    close = stock_zh_a_hist_df['收盘']
    volume = stock_zh_a_hist_df['成交量']

    rsi = talib.RSI(close,timeperiod=14)
    macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    adx = talib.ADX(high, low, close, timeperiod=14)
    slowk, slowd = talib.STOCH(high, low, close, fastk_period=9, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    cci = talib.CCI(high, low, close, timeperiod=14)
    mfi = talib.MFI(high, low, close, volume, timeperiod=14)
    willr = talib.WILLR(high, low, close, timeperiod=14)
    dic = {"rsi":rsi[len(close)-1],"macd":macd[len(close)-1],
           "macdsignal":macdsignal[len(close)-1],"macdhist":macdhist[len(close)-1],
           "adx":adx[len(close)-1],"slowk":slowk[len(close)-1],"slowd":slowd[len(close)-1],
           "cci":cci[len(close)-1],"mfi":mfi[len(close)-1],"willr":willr[len(close)-1]}
    return dic
