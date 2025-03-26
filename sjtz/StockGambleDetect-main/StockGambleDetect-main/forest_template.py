import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from joblib import dump, load
# 1. 读取数据
data = pd.read_excel(r'StockGambleDetect-main\StockGambleDetect-main\data\all_data.xlsx')
data.dropna(inplace=True)
# 2. 检查缺失值
print("缺失值统计:\n", data.isnull().sum())

# 3. 处理缺失值
data.fillna(data.mean(), inplace=True)

# 4. 准备特征和目标变量
X = data.iloc[:, 1:-1]  # 所有行，除了最后一列
y = data.iloc[:, -1]   # 目标变量 y

# 5. 拆分数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. 创建模型，并调整参数以减少过拟合
model = RandomForestClassifier(
    n_estimators=50,          # 减少树的数量
    max_depth=10,             # 限制树的深度
    min_samples_split=5,      # 增加最小样本分裂数
    min_samples_leaf=2,       # 增加最小叶子节点样本数
    random_state=42
)

# 7. 使用交叉验证评估模型
cv_scores = cross_val_score(model, X_train, y_train, cv=5)  # 5折交叉验证
print("交叉验证准确率:", cv_scores)
print("平均交叉验证准确率:", cv_scores.mean())

# 8. 训练模型
model.fit(X_train, y_train)

# 9. 进行预测
y_pred = model.predict(X_test)

# 10. 输出结果
print("测试集准确率:", accuracy_score(y_test, y_pred))
print("分类报告:\n", classification_report(y_test, y_pred))

dump(model, 'StockGambleDetect-main\StockGambleDetect-main\result\random_forest_model.joblib')

"""










code = "601777"
new_data = pd.read_excel(f'{code}data.xlsx')
test_data=new_data[new_data!='日期']
# 12. 检查新数据集的缺失值
print("新数据集缺失值统计:\n", new_data.isnull().sum())

# 13. 处理新数据集的缺失值
new_data.fillna(new_data.mean(), inplace=True)

# 14. 准备特征变量
test_data = new_data[new_data.columns[new_data.columns != '日期']]
print(test_data.head(10))
test_data = test_data[X.columns] 
X_new = test_data.iloc[:, :]

# 15. 进行预测
new_predictions = model.predict(X_new)

# 16. 将预测结果添加到新数据集中
new_data['Predicted'] = new_predictions

# 17. 保存结果到 Excel 文件
new_data.to_excel(f'data/{code}pred.xlsx', index=False)
print("预测结果已保存为 pred.xlsx")
"""