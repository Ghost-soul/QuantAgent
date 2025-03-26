from matplotlib import pyplot as plt
import pandas as pd
import mplfinance as mpf
import akshare as ak
import numpy as np
import talib
import datetime
def boll(code,time):
    start_date = time - datetime.timedelta(days=180)
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=str(start_date).replace("-",""), end_date=str(time).replace("-",""), adjust="qfq")
    if len(stock_zh_a_hist_df) < 55:
        result = np.array([np.nan for i in range(30)]).reshape(1,-1)
        return result
    upperband, middleband, lowerband = talib.BBANDS(stock_zh_a_hist_df["收盘"], timeperiod=55, nbdevup=2, nbdevdn=2, matype=0)
    #print(stock_zh_a_hist_df)
    stock_zh_a_hist_df["Upper Band"] = upperband
    stock_zh_a_hist_df["Middle Band"] = middleband
    stock_zh_a_hist_df["Lower Band"] = lowerband
    stock_zh_a_hist_df['Avg_Volume'] = stock_zh_a_hist_df['成交量'].rolling(window=5).mean()
    stock_zh_a_hist_df["量比"] = stock_zh_a_hist_df["成交量"] / stock_zh_a_hist_df["Avg_Volume"]
    stock_zh_a_hist_df.index = pd.to_datetime(stock_zh_a_hist_df["日期"])
    #print(stock_zh_a_hist_df)
    stock_zh_a_hist_df["Upper Band Gap"] = stock_zh_a_hist_df["Upper Band"] - stock_zh_a_hist_df["收盘"]
    stock_zh_a_hist_df.columns = ['日期', '股票代码','Open', 'Close', 'High', 'Low', '成交量', 'Volume', '振幅', '涨跌幅', '涨跌额',
          '换手率', 'Upper Band', 'Middle Band', 'Lower Band','Avg_Volume',"量比","Upper Band Gap"]
    result = np.array(stock_zh_a_hist_df[['Close',"Upper Band Gap",'振幅','涨跌幅','换手率',"量比"]][-5:]).reshape(1,-1)
    return result

