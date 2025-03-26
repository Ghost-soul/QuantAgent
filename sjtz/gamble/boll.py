from matplotlib import pyplot as plt
import pandas as pd
import mplfinance as mpf
import akshare as ak
import numpy as np
import talib
import datetime
dataset = pd.read_excel('gamble/gamble.xlsx',dtype=str)
#today = datetime.date.today()
dataset["start_date"] = pd.to_datetime(dataset["start_date"])
dataset.ffill(inplace=True)
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

def plot_kline_with_bollinger_bands(data):
    # 添加布林带数据
    apds = [
        mpf.make_addplot(data['Upper Band'], color='blue'),
        mpf.make_addplot(data['Middle Band'], color='orange'),
        mpf.make_addplot(data['Lower Band'], color='blue'),
    ]
    
    # 绘制K线图和布林带
    mpf.plot(data, type='candle', addplot=apds, style='charles', title='Bollinger Bands', volume=True)

tem_data1 = [boll(dataset["code"][i],dataset["start_date"][i]) for i in dataset.index]
new_data1 = np.concatenate(tem_data1, axis=0)

tem_data2 = [boll(dataset["code"][i],dataset["start_date"][i]- datetime.timedelta(days=5)) for i in dataset.index]
new_data2 = np.concatenate(tem_data2, axis=0)

tem_data3 = [boll(dataset["code"][i],dataset["start_date"][i]- datetime.timedelta(days=10)) for i in dataset.index]
new_data3 = np.concatenate(tem_data3, axis=0)

tem_data4 = [boll(dataset["code"][i],dataset["start_date"][i]- datetime.timedelta(days=15)) for i in dataset.index]
new_data4 = np.concatenate(tem_data4, axis=0)

tem_data5 = [boll(dataset["code"][i],dataset["start_date"][i]- datetime.timedelta(days=20)) for i in dataset.index]
new_data5 = np.concatenate(tem_data5, axis=0)

tem_data6 = [boll(dataset["code"][i],dataset["start_date"][i]- datetime.timedelta(days=25)) for i in dataset.index]
new_data6 = np.concatenate(tem_data6, axis=0)

tem_data7 = [boll(dataset["code"][i],dataset["start_date"][i]- datetime.timedelta(days=30)) for i in dataset.index]
new_data7 = np.concatenate(tem_data7, axis=0)

tem_data8 = [boll(dataset["code"][i],dataset["start_date"][i]- datetime.timedelta(days=35)) for i in dataset.index]
new_data8 = np.concatenate(tem_data8, axis=0)

tem_data9 = [boll(dataset["code"][i],dataset["start_date"][i]- datetime.timedelta(days=40)) for i in dataset.index]
new_data9 = np.concatenate(tem_data9, axis=0)

tem_data10 = [boll(dataset["code"][i],dataset["start_date"][i]- datetime.timedelta(days=45)) for i in dataset.index]
new_data10 = np.concatenate(tem_data10, axis=0)

all_data = np.concatenate([new_data1,new_data2,new_data3,new_data4,new_data5,new_data6,new_data7,new_data8,new_data9,new_data10],axis=0)

ones = np.ones(1002*1, dtype=int)
# 生成2的部分（3000个2）
twos = np.zeros(1002*9, dtype=int)
# 合并数组
array = np.concatenate([ones, twos])


alls = pd.DataFrame(all_data,columns=["Close","Upper Band Gap","振幅","涨跌幅","换手率","量比",
                                      "Close1","Upper Band Gap1","振幅1","涨跌幅1","换手率1","量比1",
                                      "Close2","Upper Band Gap2","振幅2","涨跌幅2","换手率2","量比2",
                                      "Close3","Upper Band Gap3","振幅3","涨跌幅3","换手率3","量比3",
                                      "Close4","Upper Band Gap4","振幅4","涨跌幅4","换手率4","量比4"])
alls["y"] = array
alls.to_excel("gamble/all_data.xlsx")

                                