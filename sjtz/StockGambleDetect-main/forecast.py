import akshare as ak
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from joblib import dump, load
from boll import boll
import datetime
import numpy as np
today = datetime.date.today()
loaded_model = load('random_forest_model.joblib')
# 使用加载的模型进行预测
stock_sh_a_spot_em_df = ak.stock_sh_a_spot_em()
stock_sz_a_spot_em_df = ak.stock_sz_a_spot_em()

data1 = stock_sh_a_spot_em_df[(stock_sh_a_spot_em_df["流通市值"]<10**10)&(stock_sh_a_spot_em_df["换手率"]>3)]
data2 = stock_sz_a_spot_em_df[(stock_sz_a_spot_em_df["流通市值"]<10**10)&(stock_sz_a_spot_em_df["换手率"]>3)]

codes = pd.concat([data1["代码"],data2["代码"]],axis=0)
codes.reset_index(drop=True,inplace=True)
tem_data = [boll(codes[i],today) for i in codes.index]
X = pd.DataFrame(np.concatenate(tem_data, axis=0),columns=["Close","Upper Band Gap","振幅","涨跌幅","换手率","量比",
                                      "Close1","Upper Band Gap1","振幅1","涨跌幅1","换手率1","量比1",
                                      "Close2","Upper Band Gap2","振幅2","涨跌幅2","换手率2","量比2",
                                      "Close3","Upper Band Gap3","振幅3","涨跌幅3","换手率3","量比3",
                                      "Close4","Upper Band Gap4","振幅4","涨跌幅4","换手率4","量比4"])

predictions = loaded_model.predict(X)

res = pd.DataFrame({'code': codes, 'Predicted': predictions})
res = res[res["Predicted"]==1]
res.to_excel(r"StockGambleDetect-main\StockGambleDetect-main\result\predictions.xlsx")