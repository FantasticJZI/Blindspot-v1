import boto3
from botocore.exceptions import ClientError

# 1. 建立 Bedrock 客戶端
client = boto3.client("bedrock-runtime", region_name="us-east-1") # 確保 region 與你開啟權限的區域一致

# 2. 設定模型 ID (這裡以 Claude 3 Haiku 為例)
model_id = "anthropic.claude-3-haiku-20240307-v1:0"

# 3. 準備你的模型特徵數據 (這是從你昨天的訓練結果拿到的)
user_data = {
    "ratio": 0.98,
    "time": 120,
    "ip_changes": 15,
    "status": "學生"
}

# 4. 設計 Prompt
prompt = f"""
你是一位專業的虛擬資產合規分析師。
請根據以下數據，為 Blindspot v1 系統生成一份『風險診斷書』：
- 提領比率: {user_data['ratio']}
- 資金停留時間: {user_data['time']} 秒
- IP 變動次數: {user_data['ip_changes']}
- 用戶身分: {user_data['status']}

請用繁體中文回答，包含：
1. 風險判定結果（高/中/低）
2. 行為異常點解釋
3. 具體建議處置方案（例如：暫停提領、要求人工覆核）
"""

# 5. 呼叫 API
try:
    response = client.converse(
        modelId=model_id,
        messages=[{"role": "user", "content": [{"text": prompt}]}]
    )
    
    # 6. 印出結果
    print("--- Blindspot v1 自動化報告 ---")
    print(response['output']['message']['content'][0]['text'])

except ClientError as e:
    print(f"呼叫出錯了: {e}")