import pandas as pd
import numpy as np

np.random.seed(42)

data = []
for i in range(2000):
    user_id = f"U{i+1:04d}"
    is_mule = np.random.choice([0, 1], p=[0.7, 0.3])
    
    if is_mule == 1:
        kyc_status = np.random.choice(['Student', 'Employee', 'Unemployed'], p=[0.5, 0.2, 0.3])
        deposit_amount = np.random.uniform(5000, 50000)
        withdrawal_ratio = np.random.uniform(0.95, 1.0)
        withdraw_time_diff = np.random.uniform(10, 600)
        ip_change_count = np.random.randint(5, 20)
        transaction_hour = np.random.choice(range(24), p=[0.15]*4 + [0.02]*20)
        network_distance = np.random.choice([1, 2], p=[0.7, 0.3])
    else:
        kyc_status = np.random.choice(['Student', 'Employee', 'Unemployed'], p=[0.2, 0.6, 0.2])
        deposit_amount = np.random.uniform(1000, 100000)
        withdrawal_ratio = np.random.uniform(0.1, 0.9)
        withdraw_time_diff = np.random.uniform(600, 86400)
        ip_change_count = np.random.randint(0, 5)
        transaction_hour = np.random.choice(range(24), p=[0.02]*4 + [0.046]*20)
        network_distance = np.random.choice([3, 4, 5], p=[0.5, 0.3, 0.2])
    
    data.append({
        'User_ID': user_id,
        'KYC_Status': kyc_status,
        'Deposit_Amount': round(deposit_amount, 2),
        'Withdrawal_Ratio': round(withdrawal_ratio, 3),
        'Withdraw_Time_Diff': int(withdraw_time_diff),
        'IP_Change_Count': ip_change_count,
        'Transaction_Hour': transaction_hour,
        'Network_Distance': network_distance,
        'Is_Mule': is_mule
    })

df = pd.DataFrame(data)
df.to_csv('blindspot_v1_data.csv', index=False)
print(f"已產生 {len(df)} 筆資料")
print(f"人頭戶數量: {df['Is_Mule'].sum()}")
print(f"\n資料預覽:\n{df.head(10)}")
