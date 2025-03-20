import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout

data = pd.read_excel('sjtz/gamble/all_data.xlsx')
X_train = data.iloc[:, :-2].values
y_train = data.iloc[:, -1].values

# 数据归一化
model = Sequential([
    Conv1D(filters=34, kernel_size=3, activation='sigmoid', 
           input_shape=(X_train.shape[1], 1)),
    MaxPooling1D(pool_size=2),
    Dropout(0.2),
    
    Conv1D(filters=16, kernel_size=3, activation='sigmoid'),
    MaxPooling1D(pool_size=2),
    Dropout(0.2),
    
    Flatten(),
    Dense(1, activation='sigmoid'),
])

model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# 训练模型
history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=32,
    validation_split=0.1,
    verbose=1
)
model.save('sjtz/gamble/gamble_model.keras')
