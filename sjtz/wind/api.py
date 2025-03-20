from WindPy import w
from call_model import call_model
import datetime
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
dir = os.path.dirname(__file__)
today = datetime.date.today()
#print(today)
w.start() # 默认命令超时时间为120秒，如需设置超时时间可以加入waitTime参数，例如waitTime=60,即设置命令超时时间为60秒 
begin = today - datetime.timedelta(days=30)
w.isconnected() # 判断WindPy是否已经登录成功
data = w.edb(["S0114145","S0069669","S0031645","S0035819"],str(begin), end_date=str(today),Fill="Previous",usedf = True)[1]#comex黄金库存，comex黄金库存市值,黄金现货价（伦敦市场）#上海金交所黄金现货价
z = np.around(np.multiply(data['S0114145'].values,data['S0069669'].values)/(10**9),decimals=2)
fig, ax = plt.subplots()
ax.plot(data.index.values, data['S0114145'].values, color='green')
ax.set_ylabel('蛊司')
ax.set_xlabel('时间')
ax.spines['right'].set_visible(False) # ax右轴隐藏

z_ax = ax.twinx() # 创建与轴群ax共享x轴的轴群z_ax
z_ax.plot(data.index.values, z, color='blue')
z_ax.set_ylabel('Billion')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.title('COMEX交易所黄金库存水平及市值')
plt.savefig(os.path.join(dir,'plot.png'))

prompt = f"""这是近一个月COMEX交易所黄金库存量的数据：{data['S0114145']}
这是近一个月COMEX交易所黄金库存市值的数据(单位billian)：{z}
这是近一个月伦敦市场黄金现货价格数据：{data['S0031645']}
这是近一个月上海金交所黄金现货价格数据：{data['S0035819']}
任务：请根据上述结果分析判断近期是否存在套利策略。
请使用Markdown格式回答，但不要用任何代码块（如 ```）包裹内容。
"""
data.columns = ["comex黄金库存量","comex黄金库存市值","黄金现货价（伦敦市场）","上海金交所黄金现货价"]
new_data = data.to_markdown()
result = call_model(prompt)
result+="\n"+"![图](plot.png)"
result+="\n"+new_data
with open(os.path.join(dir,"stragety.md"), "w", encoding="utf-8") as file:
            file.write(result)