import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# 讀取CSV檔案，跳過前3行（標題和空白行）
df = pd.read_csv("刑事案件嫌疑犯人數－按職業別1.csv", skiprows=3, encoding='utf-8')

# 清理數據：去除空白列和無效行
df = df.dropna(how='all')
df = df.iloc[:, :20]  # 只保留前20列（有效數據列）

# 設定列名（從原始CSV中提取）
columns = ['Year', 'Total', 'Representatives_Managers', 'Professionals', 'Technicians', 
           'Clerical_Support', 'Service_Workers', 'Sales_Workers', 'Agricultural_Workers', 
           'Security_Workers', 'Craft_Workers', 'Machine_Operators', 'Elementary_Workers', 
           'Students', 'Unemployed', 'Others']
df.columns = columns

# 清理Year列（去除"民國"和西元年份）
df['Year'] = df['Year'].str.extract(r'(\d+)')[0].astype(int)

# 將所有數值列中的逗號去除並轉換為數值
numeric_cols = df.columns[1:]
for col in numeric_cols:
    df[col] = df[col].str.replace(',', '').astype(float)

# 繪製堆疊柱狀圖
plt.figure(figsize=(14, 8))
colors = plt.cm.tab20.colors  # 使用豐富的顏色區分職業類別

# 選擇要堆疊的職業類別（排除Total）
stack_cols = columns[2:]
df[stack_cols].plot.bar(stacked=True, color=colors, width=0.8, ax=plt.gca())

# 設定圖表標題和標籤
plt.title('Taiwan Criminal Cases Offenders by Occupation (1998-2022)', fontsize=14, pad=20)
plt.xlabel('Year (Republic of China Calendar)', fontsize=12)
plt.ylabel('Number of Offenders', fontsize=12)
plt.xticks(range(len(df)), df['Year'], rotation=45, ha='right')

# 調整圖例位置和大小
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)

# 格式化Y軸標籤（顯示千位分隔符）
plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

# 調整布局
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()