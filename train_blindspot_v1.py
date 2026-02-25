import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

# 讀取資料
df = pd.read_csv('blindspot_v1_data.csv')

# One-hot Encoding for KYC_Status
df = pd.get_dummies(df, columns=['KYC_Status'], prefix='KYC')

# 準備特徵和標籤
X = df.drop(['User_ID', 'Is_Mule'], axis=1)
y = df['Is_Mule']

# 切分訓練集和測試集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 訓練隨機森林模型
model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
model.fit(X_train, y_train)

# 預測
y_pred = model.predict(X_test)

# 評估指標
f1 = f1_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

print("=" * 50)
print("Blindspot v1 模型訓練結果")
print("=" * 50)
print(f"\nF1-Score: {f1:.4f}")
print(f"\n混淆矩陣:")
print(f"              預測 0    預測 1")
print(f"實際 0      {cm[0][0]:6d}    {cm[0][1]:6d}")
print(f"實際 1      {cm[1][0]:6d}    {cm[1][1]:6d}")

# 特徵重要度
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)

print(f"\n前三個最重要特徵:")
for i, row in feature_importance.head(3).iterrows():
    print(f"{row['Feature']:25s}: {row['Importance']:.4f}")
print("=" * 50)
