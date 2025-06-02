import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
import seaborn as sns

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 讀取資料
df = pd.read_csv('主要警政統計指標1.csv', encoding='utf-8')

# 資料清理和預處理
# 跳過前兩行標題，從第三行開始讀取實際數據
df = pd.read_csv('主要警政統計指標1.csv', skiprows=2, encoding='utf-8')

# 手動定義欄位名稱（根據CSV結構）
columns = ['年別', '西元年', '全般刑案_發生數', '全般刑案_破獲數', '全般刑案_破獲率', 
           '全般刑案_嫌疑犯', '全般刑案_犯罪率', '全般刑案_犯罪人口率',
           '暴力犯罪_發生數', '暴力犯罪_破獲數', '暴力犯罪_破獲率', '暴力犯罪_嫌疑犯', '暴力犯罪_犯罪率',
           '竊盜_發生數', '竊盜_破獲數', '竊盜_破獲率', '竊盜_嫌疑犯', '竊盜_犯罪率']

df.columns = columns

# 清理數據，移除逗號並轉換為數值
for col in df.columns:
    if col not in ['年別', '西元年']:
        df[col] = df[col].astype(str).str.replace(',', '').replace('', np.nan)
        df[col] = pd.to_numeric(df[col], errors='coerce')

# 移除空行
df = df.dropna(subset=['西元年'])

# 確保年份為整數
df['西元年'] = df['西元年'].astype(int)
df['民國年'] = df['西元年'] - 1911

print("資料概況:")
print(df.head())
print(f"資料範圍: {df['西元年'].min()} - {df['西元年'].max()}")

# 1. 複製您提供的圖表：暴力犯罪發生數與破獲率趨勢
fig, ax1 = plt.subplots(figsize=(14, 8))

# 左軸：發生數（柱狀圖）
color = 'tab:blue'
ax1.set_xlabel('民國年份')
ax1.set_ylabel('發生數 (件)', color=color)
bars = ax1.bar(df['民國年'], df['暴力犯罪_發生數'], color='lightblue', alpha=0.7, label='發生數')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_ylim(0, df['暴力犯罪_發生數'].max() * 1.1)

# 在柱狀圖上方標示數值
for i, v in enumerate(df['暴力犯罪_發生數']):
    if not pd.isna(v):
        ax1.text(df['民國年'].iloc[i], v + 200, f'{int(v):,}', 
                ha='center', va='bottom', fontsize=8)

# 右軸：破獲率（線圖）
ax2 = ax1.twinx()
color = 'tab:orange'
ax2.set_ylabel('破獲率 (%)', color=color)
line = ax2.plot(df['民國年'], df['暴力犯罪_破獲率'], color='orange', marker='o', 
                linewidth=2, markersize=4, label='破獲率')
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylim(50, 110)

# 在線圖上標示數值
for i, v in enumerate(df['暴力犯罪_破獲率']):
    if not pd.isna(v):
        ax2.text(df['民國年'].iloc[i], v + 2, f'{v:.1f}%', 
                ha='center', va='bottom', fontsize=8, color='orange')

plt.title('民國92-112年刑案發生與破獲率趨勢分析 - 暴力犯罪', fontsize=16, fontweight='bold')
ax1.set_xticks(df['民國年'][::2])  # 每兩年顯示一個刻度
ax1.grid(True, alpha=0.3)

# 添加圖例
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.tight_layout()
plt.show()

# 2. 全般刑案趨勢分析
fig, ax1 = plt.subplots(figsize=(14, 8))

color = 'tab:red'
ax1.set_xlabel('民國年份')
ax1.set_ylabel('發生數 (件)', color=color)
bars = ax1.bar(df['民國年'], df['全般刑案_發生數'], color='lightcoral', alpha=0.7, label='發生數')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:green'
ax2.set_ylabel('破獲率 (%)', color=color)
line = ax2.plot(df['民國年'], df['全般刑案_破獲率'], color='green', marker='s', 
                linewidth=2, markersize=4, label='破獲率')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('民國92-112年全般刑案發生數與破獲率趨勢', fontsize=16, fontweight='bold')
ax1.set_xticks(df['民國年'][::2])
ax1.grid(True, alpha=0.3)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.tight_layout()
plt.show()

# 3. 三種犯罪類型發生數比較
plt.figure(figsize=(14, 8))
plt.plot(df['民國年'], df['全般刑案_發生數'], marker='o', linewidth=2, label='全般刑案')
plt.plot(df['民國年'], df['暴力犯罪_發生數'], marker='s', linewidth=2, label='暴力犯罪')
plt.plot(df['民國年'], df['竊盜_發生數'], marker='^', linewidth=2, label='竊盜')

plt.title('民國92-112年各類犯罪發生數趨勢比較', fontsize=16, fontweight='bold')
plt.xlabel('民國年份')
plt.ylabel('發生數 (件)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(df['民國年'][::2], rotation=45)
plt.tight_layout()
plt.show()

# 4. 破獲率比較
plt.figure(figsize=(14, 8))
plt.plot(df['民國年'], df['全般刑案_破獲率'], marker='o', linewidth=2, label='全般刑案')
plt.plot(df['民國年'], df['暴力犯罪_破獲率'], marker='s', linewidth=2, label='暴力犯罪')
plt.plot(df['民國年'], df['竊盜_破獲率'], marker='^', linewidth=2, label='竊盜')

plt.title('民國92-112年各類犯罪破獲率趨勢比較', fontsize=16, fontweight='bold')
plt.xlabel('民國年份')
plt.ylabel('破獲率 (%)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(df['民國年'][::2], rotation=45)
plt.ylim(50, 105)
plt.tight_layout()
plt.show()

# 5. 犯罪率趨勢（每十萬人口）
plt.figure(figsize=(14, 8))
plt.plot(df['民國年'], df['全般刑案_犯罪率'], marker='o', linewidth=2, label='全般刑案犯罪率')
plt.plot(df['民國年'], df['暴力犯罪_犯罪率'], marker='s', linewidth=2, label='暴力犯罪犯罪率')
plt.plot(df['民國年'], df['竊盜_犯罪率'], marker='^', linewidth=2, label='竊盜犯罪率')

plt.title('民國92-112年各類犯罪率趨勢 (每十萬人口)', fontsize=16, fontweight='bold')
plt.xlabel('民國年份')
plt.ylabel('犯罪率 (件/十萬人口)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(df['民國年'][::2], rotation=45)
plt.tight_layout()
plt.show()

# 6. 熱力圖：年度-犯罪類型矩陣
# 準備熱力圖資料
heatmap_data = df[['民國年', '全般刑案_發生數', '暴力犯罪_發生數', '竊盜_發生數']].set_index('民國年')
heatmap_data.columns = ['全般刑案', '暴力犯罪', '竊盜']

# 正規化數據以便比較
heatmap_normalized = heatmap_data.div(heatmap_data.max(axis=0), axis=1)

plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_normalized.T, annot=True, cmap='YlOrRd', fmt='.2f', 
            cbar_kws={'label': '相對發生數 (正規化)'})
plt.title('各類犯罪發生數相對比較熱力圖', fontsize=16, fontweight='bold')
plt.xlabel('民國年份')
plt.ylabel('犯罪類型')
plt.tight_layout()
plt.show()

# 7. 統計摘要
print("\n=== 統計摘要 ===")
print(f"暴力犯罪發生數:")
print(f"  最高: {df['暴力犯罪_發生數'].max():,} 件 (民國{df.loc[df['暴力犯罪_發生數'].idxmax(), '民國年']}年)")
print(f"  最低: {df['暴力犯罪_發生數'].min():,} 件 (民國{df.loc[df['暴力犯罪_發生數'].idxmin(), '民國年']}年)")
print(f"  平均: {df['暴力犯罪_發生數'].mean():.0f} 件")

print(f"\n暴力犯罪破獲率:")
print(f"  最高: {df['暴力犯罪_破獲率'].max():.1f}% (民國{df.loc[df['暴力犯罪_破獲率'].idxmax(), '民國年']}年)")
print(f"  最低: {df['暴力犯罪_破獲率'].min():.1f}% (民國{df.loc[df['暴力犯罪_破獲率'].idxmin(), '民國年']}年)")
print(f"  平均: {df['暴力犯罪_破獲率'].mean():.1f}%")

print(f"\n全般刑案發生數:")
print(f"  最高: {df['全般刑案_發生數'].max():,} 件 (民國{df.loc[df['全般刑案_發生數'].idxmax(), '民國年']}年)")
print(f"  最低: {df['全般刑案_發生數'].min():,} 件 (民國{df.loc[df['全般刑案_發生數'].idxmin(), '民國年']}年)")
print(f"  減少幅度: {((df['全般刑案_發生數'].iloc[-1] - df['全般刑案_發生數'].iloc[0]) / df['全般刑案_發生數'].iloc[0] * 100):.1f}%")