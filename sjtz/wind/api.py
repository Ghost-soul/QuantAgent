from WindPy import w
from call_model import call_model
import datetime
import os
import matplotlib.pyplot as plt
dir = os.path.dirname(__file__)
today = datetime.date.today()
#print(today)
w.start() # 默认命令超时时间为120秒，如需设置超时时间可以加入waitTime参数，例如waitTime=60,即设置命令超时时间为60秒 
begin = today - datetime.timedelta(days=365)
w.isconnected() # 判断WindPy是否已经登录成功
data = w.edb("S0114145",str(begin), end_date=str(today),usedf = True)
plt.plot(data[1].index.values,data[1])
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.xlabel('时间')
plt.ylabel('蛊司')
plt.title('COMEX交易所黄金库存水平')
plt.savefig(os.path.join(dir,'plot.png'))
prompt = f"""这是近一年COMEX交易所黄金库存量的数据：{data[1]}
请根据上述结果分析判断近期是否存在套利策略。
请使用Markdown格式回答，但不要用任何代码块（如 ```）包裹内容。
"""
result = call_model(prompt)
result+="![示例图](plot.png)"
with open(os.path.join(dir,"stragety.md"), "w", encoding="utf-8") as file:
            file.write(result)