import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
import seaborn as sns

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 讀取資料
df = pd.read_csv('主要警政統計指標1V.csv', encoding='utf-8')

# 資料清理和預處理
# 跳過前兩行標題，從第三行開始讀取實際數據
df = pd.read_csv('主要警政統計指標1V.csv', skiprows=2, encoding='utf-8')

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

# ================== 詳細資料分析結果 ==================
print("\n" + "="*80)
print("                      台灣警政統計資料分析報告")
print(f"                    分析期間：民國{df['民國年'].min()}年 - {df['民國年'].max()}年")
print("="*80)

# 1. 整體犯罪趨勢分析
print("\n【一、整體犯罪趨勢分析】")
print("-"*50)

# 全般刑案分析
total_start = df['全般刑案_發生數'].iloc[0]
total_end = df['全般刑案_發生數'].iloc[-1]
total_change_rate = ((total_end - total_start) / total_start) * 100
total_peak = df['全般刑案_發生數'].max()
total_peak_year = df.loc[df['全般刑案_發生數'].idxmax(), '民國年']

print(f"1. 全般刑案發生數趨勢：")
print(f"   • 起始年（民國{df['民國年'].min()}年）：{total_start:,} 件")
print(f"   • 結束年（民國{df['民國年'].max()}年）：{total_end:,} 件")
print(f"   • 整體變化：{'下降' if total_change_rate < 0 else '上升'} {abs(total_change_rate):.1f}%")
print(f"   • 高峰期：民國{total_peak_year}年，達 {total_peak:,} 件")

# 計算年平均變化率
years_span = df['民國年'].max() - df['民國年'].min()
annual_change_rate = (((total_end / total_start) ** (1/years_span)) - 1) * 100
print(f"   • 年平均變化率：{annual_change_rate:.2f}%")

# 2. 暴力犯罪深度分析
print(f"\n2. 暴力犯罪分析：")
violence_start = df['暴力犯罪_發生數'].iloc[0]
violence_end = df['暴力犯罪_發生數'].iloc[-1]
violence_change_rate = ((violence_end - violence_start) / violence_start) * 100
violence_peak = df['暴力犯罪_發生數'].max()
violence_peak_year = df.loc[df['暴力犯罪_發生數'].idxmax(), '民國年']

print(f"   • 起始年發生數：{violence_start:,} 件")
print(f"   • 結束年發生數：{violence_end:,} 件")
print(f"   • 整體變化：{'下降' if violence_change_rate < 0 else '上升'} {abs(violence_change_rate):.1f}%")
print(f"   • 高峰期：民國{violence_peak_year}年，達 {violence_peak:,} 件")

# 3. 竊盜犯罪分析
print(f"\n3. 竊盜犯罪分析：")
theft_start = df['竊盜_發生數'].iloc[0]
theft_end = df['竊盜_發生數'].iloc[-1]
theft_change_rate = ((theft_end - theft_start) / theft_start) * 100
theft_peak = df['竊盜_發生數'].max()
theft_peak_year = df.loc[df['竊盜_發生數'].idxmax(), '民國年']

print(f"   • 起始年發生數：{theft_start:,} 件")
print(f"   • 結束年發生數：{theft_end:,} 件")
print(f"   • 整體變化：{'下降' if theft_change_rate < 0 else '上升'} {abs(theft_change_rate):.1f}%")
print(f"   • 高峰期：民國{theft_peak_year}年，達 {theft_peak:,} 件")

# 二、破獲率分析
print("\n【二、破獲率分析】")
print("-"*50)

# 各類犯罪破獲率分析
crime_types = ['全般刑案', '暴力犯罪', '竊盜']
solve_rates = {}

for crime_type in crime_types:
    col_name = f'{crime_type}_破獲率'
    avg_rate = df[col_name].mean()
    max_rate = df[col_name].max()
    min_rate = df[col_name].min()
    max_year = df.loc[df[col_name].idxmax(), '民國年']
    min_year = df.loc[df[col_name].idxmin(), '民國年']
    
    solve_rates[crime_type] = {
        'avg': avg_rate,
        'max': max_rate,
        'min': min_rate,
        'max_year': max_year,
        'min_year': min_year
    }
    
    print(f"{crime_type}破獲率：")
    print(f"   • 平均破獲率：{avg_rate:.1f}%")
    print(f"   • 最高破獲率：{max_rate:.1f}%（民國{max_year}年）")
    print(f"   • 最低破獲率：{min_rate:.1f}%（民國{min_year}年）")
    print(f"   • 破獲率穩定性：{'穩定' if (max_rate - min_rate) < 10 else '波動較大'}（差距 {max_rate - min_rate:.1f}%）")
    print()

# 三、犯罪率分析（每十萬人口）
print("【三、犯罪率分析（每十萬人口）】")
print("-"*50)

for crime_type in crime_types:
    col_name = f'{crime_type}_犯罪率'
    start_rate = df[col_name].iloc[0]
    end_rate = df[col_name].iloc[-1]
    avg_rate = df[col_name].mean()
    rate_change = ((end_rate - start_rate) / start_rate) * 100
    
    print(f"{crime_type}犯罪率趨勢：")
    print(f"   • 起始年：{start_rate:.1f} 件/十萬人口")
    print(f"   • 結束年：{end_rate:.1f} 件/十萬人口")
    print(f"   • 平均值：{avg_rate:.1f} 件/十萬人口")
    print(f"   • 變化幅度：{'下降' if rate_change < 0 else '上升'} {abs(rate_change):.1f}%")
    print()

# 四、年度趨勢特徵分析
print("【四、年度趨勢特徵分析】")
print("-"*50)

# 找出顯著變化的年份
def find_significant_changes(series, threshold=0.15):
    """找出年變化率超過閾值的年份"""
    changes = []
    for i in range(1, len(series)):
        if pd.notna(series.iloc[i]) and pd.notna(series.iloc[i-1]):
            change_rate = (series.iloc[i] - series.iloc[i-1]) / series.iloc[i-1]
            if abs(change_rate) > threshold:
                changes.append({
                    'year': df.iloc[i]['民國年'],
                    'change_rate': change_rate * 100,
                    'direction': '大幅上升' if change_rate > 0 else '大幅下降'
                })
    return changes

print("顯著變化年份（年變化率超過15%）：")
for crime_type in crime_types:
    col_name = f'{crime_type}_發生數'
    changes = find_significant_changes(df[col_name])
    if changes:
        print(f"\n{crime_type}：")
        for change in changes:
            print(f"   • 民國{change['year']}年：{change['direction']} {abs(change['change_rate']):.1f}%")
    else:
        print(f"\n{crime_type}：無顯著年度變化")

# 五、相關性分析
print("\n【五、犯罪類型相關性分析】")
print("-"*50)

# 計算各類犯罪發生數的相關係數
crime_data = df[['全般刑案_發生數', '暴力犯罪_發生數', '竊盜_發生數']]
correlation_matrix = crime_data.corr()

print("各類犯罪發生數相關係數：")
print(f"• 全般刑案 vs 暴力犯罪：{correlation_matrix.iloc[0,1]:.3f}")
print(f"• 全般刑案 vs 竊盜：{correlation_matrix.iloc[0,2]:.3f}")
print(f"• 暴力犯罪 vs 竊盜：{correlation_matrix.iloc[1,2]:.3f}")

# 六、重要結論
print("\n【六、重要發現與結論】")
print("-"*50)

conclusions = []

# 整體趨勢結論
if total_change_rate < -20:
    conclusions.append(f"1. 整體犯罪情況顯著改善，全般刑案發生數在{years_span}年間下降了{abs(total_change_rate):.1f}%")
elif total_change_rate < -5:
    conclusions.append(f"1. 整體犯罪情況有所改善，全般刑案發生數呈現下降趨勢")
else:
    conclusions.append(f"1. 整體犯罪情況需要關注，發生數變化幅度為{total_change_rate:.1f}%")

# 破獲率結論
best_solve_rate = max(solve_rates.keys(), key=lambda x: solve_rates[x]['avg'])
worst_solve_rate = min(solve_rates.keys(), key=lambda x: solve_rates[x]['avg'])
conclusions.append(f"2. 破獲率表現：{best_solve_rate}破獲率最高（平均{solve_rates[best_solve_rate]['avg']:.1f}%），{worst_solve_rate}破獲率相對較低（平均{solve_rates[worst_solve_rate]['avg']:.1f}%）")

# 犯罪類型比重分析
latest_year_data = df.iloc[-1]
violence_ratio = (latest_year_data['暴力犯罪_發生數'] / latest_year_data['全般刑案_發生數']) * 100
theft_ratio = (latest_year_data['竊盜_發生數'] / latest_year_data['全般刑案_發生數']) * 100
conclusions.append(f"3. 最新年度犯罪結構：竊盜案件占全般刑案 {theft_ratio:.1f}%，暴力犯罪占 {violence_ratio:.1f}%")

# 警政效能結論
avg_total_solve_rate = solve_rates['全般刑案']['avg']
if avg_total_solve_rate > 85:
    conclusions.append(f"4. 警政執法效能良好，整體平均破獲率達 {avg_total_solve_rate:.1f}%")
else:
    conclusions.append(f"4. 警政執法效能有待提升，整體平均破獲率為 {avg_total_solve_rate:.1f}%")

for i, conclusion in enumerate(conclusions, 1):
    print(conclusion)

print("\n" + "="*80)
print("                        分析報告完成")
print("="*80)

# 原有的圖表繪製部分保持不變
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