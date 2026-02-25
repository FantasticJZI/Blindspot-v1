# Blindspot v1 - 人頭戶偵測系統

虛擬資產平台人頭戶偵測系統，結合機器學習模型與 AWS Bedrock 生成式 AI 進行風險分析。

## 專案結構

```
aws_prac/
├── generate_blindspot_v1_data.py  # 資料生成腳本
├── train_blindspot_v1.py          # 模型訓練腳本
├── test_bedrock.py                # AWS Bedrock 測試腳本
├── blindspot_v1_data.csv          # 生成的訓練資料
└── README.md                      # 專案說明文件
```

## 環境建置

### 1. Python 環境
- Python 3.8 或以上版本

### 2. 安裝相依套件

```bash
pip install pandas numpy scikit-learn boto3
```

### 3. AWS 設定（僅執行 test_bedrock.py 需要）

#### 3.1 獲得 AWS 憑證

1. 登入 [AWS Management Console](https://aws.amazon.com/console/)
2. 點擊右上角帳戶名稱 → 選擇「Security credentials」
3. 向下捲動至「Access keys」區塊
4. 點擊「Create access key」
5. 選擇使用案例（建議選擇「Command Line Interface (CLI)」）
6. 勾選確認框後點擊「Next」
7. 設定描述標籤（選填）後點擊「Create access key」
8. **重要**：立即複製或下載 CSV 檔案保存憑證
   - Access Key ID（範例：AKIAIOSFODNN7EXAMPLE）
   - Secret Access Key（範例：wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY）
   - Secret Access Key 僅顯示一次，請妥善保存

#### 3.2 配置 AWS 憑證

```bash
aws configure
```

輸入以下資訊：
- AWS Access Key ID：貼上步驟 3.1 取得的 Access Key ID
- AWS Secret Access Key：貼上步驟 3.1 取得的 Secret Access Key
- Default region name: `us-east-1`
- Default output format: `json`

#### 3.3 啟用 Bedrock 服務

1. 在 AWS Console 搜尋「Bedrock」
2. 選擇 `us-east-1` 區域
3. 點擊左側選單「Model access」
4. 點擊「Enable specific models」或「Modify model access」
5. 勾選「Claude 3 Haiku」
6. 點擊「Save changes」等待審核通過（通常即時生效）

## 執行過程

### 步驟 1：生成訓練資料

```bash
python generate_blindspot_v1_data.py
```

**功能說明：**
- 生成 2000 筆模擬用戶交易資料
- 人頭戶比例約 30%
- 特徵包含：KYC 狀態、存款金額、提領比率、IP 變動次數等

### 步驟 2：訓練機器學習模型

```bash
python train_blindspot_v1.py
```

**功能說明：**
- 使用隨機森林分類器訓練模型
- 80/20 切分訓練集與測試集
- 輸出 F1-Score、混淆矩陣和特徵重要度

### 步驟 3：測試 AWS Bedrock 整合

```bash
python test_bedrock.py
```

**功能說明：**
- 呼叫 AWS Bedrock Claude 3 Haiku 模型
- 根據用戶特徵生成繁體中文風險診斷報告
- 提供風險判定與處置建議

## 執行結果說明

### 1. 資料生成結果

```
已產生 2000 筆資料
人頭戶數量: 600
```

生成的 CSV 檔案包含以下欄位：
- User_ID：用戶編號
- KYC_Status：身分狀態（Student/Employee/Unemployed）
- Deposit_Amount：存款金額
- Withdrawal_Ratio：提領比率
- Withdraw_Time_Diff：資金停留時間（秒）
- IP_Change_Count：IP 變動次數
- Transaction_Hour：交易時段
- Network_Distance：網路距離
- Is_Mule：是否為人頭戶（0/1）

### 2. 模型訓練結果

```
==================================================
Blindspot v1 模型訓練結果
==================================================

F1-Score: 0.9XXX

混淆矩陣:
              預測 0    預測 1
實際 0         XXX       XXX
實際 1         XXX       XXX

前三個最重要特徵:
Withdrawal_Ratio         : 0.XXXX
Withdraw_Time_Diff       : 0.XXXX
IP_Change_Count          : 0.XXXX
==================================================
```

**指標解讀：**
- F1-Score 接近 1 表示模型效果良好
- 混淆矩陣顯示真陽性、假陽性、真陰性、假陰性數量
- 提領比率、資金停留時間、IP 變動次數為關鍵風險特徵

### 3. AWS Bedrock 輸出範例

```
--- Blindspot v1 自動化報告 ---

1. 風險判定結果：高風險

2. 行為異常點解釋：
   - 提領比率 0.98 極高，幾乎全額提領
   - 資金停留時間僅 120 秒，符合快進快出特徵
   - IP 變動次數 15 次異常頻繁
   - 學生身分與高額交易不符

3. 具體建議處置方案：
   - 立即暫停該帳戶提領功能
   - 要求人工覆核並補充身分證明文件
   - 調查資金來源與交易對手方
```

## 技術架構

- **資料處理**：Pandas, NumPy
- **機器學習**：Scikit-learn (Random Forest)
- **生成式 AI**：AWS Bedrock (Claude 3 Haiku)
- **雲端服務**：AWS Boto3

## 注意事項

- test_bedrock.py 會產生 AWS API 呼叫費用
- 確保 AWS 憑證具備 bedrock:InvokeModel 權限
- 模型訓練結果會因隨機種子而略有差異
