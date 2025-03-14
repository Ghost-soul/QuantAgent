from matplotlib import pyplot as plt
import pandas as pd
import mplfinance as mpf
import akshare as ak
import numpy as np
import talib
import datetime
dataset = pd.read_csv('data.csv')


start_date = today - datetime.timedelta(days=365)
#print(start_date,today)
stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="002126", period="daily", start_date=str(start_date).replace("-",""), end_date=str(today).replace("-",""), adjust="qfq")
upperband, middleband, lowerband = talib.BBANDS(stock_zh_a_hist_df["收盘"], timeperiod=55, nbdevup=2, nbdevdn=2, matype=0)
stock_zh_a_hist_df["Upper Band"] = upperband
stock_zh_a_hist_df["Middle Band"] = middleband
stock_zh_a_hist_df["Lower Band"] = lowerband
stock_zh_a_hist_df.index = pd.to_datetime(stock_zh_a_hist_df["日期"])
#print(stock_zh_a_hist_df)
stock_zh_a_hist_df.columns = ['日期', '股票代码','Open', 'Close', 'High', 'Low', '成交量', 'Volume', '振幅', '涨跌幅', '涨跌额',
       '换手率', 'Upper Band', 'Middle Band', 'Lower Band']


def plot_kline_with_bollinger_bands(data):
    # 添加布林带数据
    apds = [
        mpf.make_addplot(data['Upper Band'], color='blue'),
        mpf.make_addplot(data['Middle Band'], color='orange'),
        mpf.make_addplot(data['Lower Band'], color='blue'),
    ]
    
    # 绘制K线图和布林带
    mpf.plot(data, type='candle', addplot=apds, style='charles', title='Bollinger Bands', volume=True)

plot_kline_with_bollinger_bands(stock_zh_a_hist_df)