import pandas as pd
import akshare as ak
import numpy as np
import talib
import datetime


def boll(code,time):
    start_date = time - datetime.timedelta(days=365)
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=str(start_date).replace("-",""), end_date=str(time).replace("-",""), adjust="qfq")
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



code = "601777"
tem_data = ak.stock_zh_a_hist(symbol=code, period="daily", start_date="20240310", end_date="20250310", adjust="qfq")
tem_data["日期"] = pd.to_datetime(tem_data["日期"])
test_data = []
for i in tem_data.index:
    time = tem_data["日期"][i]
    test_data.append(boll(code,time))

#market_data=ak.stock_zh_a_spot_em()
#market_data_code=market_data[market_data['代码'] == code]

test = np.concatenate(test_data, axis=0)
alls = pd.DataFrame(test,columns=["Close","Upper Band Gap","振幅","涨跌幅","换手率","量比",
                                      "Close1","Upper Band Gap1","振幅1","涨跌幅1","换手率1","量比1",
                                      "Close2","Upper Band Gap2","振幅2","涨跌幅2","换手率2","量比2",
                                      "Close3","Upper Band Gap3","振幅3","涨跌幅3","换手率3","量比3",
                                      "Close4","Upper Band Gap4","振幅4","涨跌幅4","换手率4","量比4"
                                      ])
alls["日期"] = tem_data["日期"]
    # 财务信息


alls.to_excel(f"{code}data.xlsx",index = False)

'''
alls['市盈率-动态']=market_data_code['市盈率-动态']
alls['市净率']=market_data_code['市净率']
alls['总市值']=market_data_code['总市值']
alls['流通市值']=market_data_code['流通市值']
alls['涨速']=market_data_code['涨速']
alls['5分钟涨跌']=market_data_code['5分钟涨跌']
alls['60日涨跌幅']=market_data_code['60日涨跌幅']
alls['年初至今涨跌幅']=market_data_code['年初至今涨跌幅']
'''