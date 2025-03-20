from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np
# 加载保存的模型
model = load_model('sjtz/gamble/gamble_model.keras')

# 使用加载的模型进行预测



test_data = pd.read_excel('sjtz/gamble/tjkj.xlsx')
X_test = test_data.iloc[:,:-1].values
predicted = model.predict(X_test)

test_data["predicted"] = predicted
test_data.to_excel("sjtz/gamble/tjkj_pre.xlsx", index=False)