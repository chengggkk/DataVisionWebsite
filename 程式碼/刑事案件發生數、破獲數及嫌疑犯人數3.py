import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import font_manager
import warnings
warnings.filterwarnings('ignore')

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 手動輸入數據（基於CSV內容）
data = {
    '縣市': ['宜蘭縣', '新竹縣', '苗栗縣', '彰化縣', '南投縣', '雲林縣', '嘉義縣', '屏東縣', 
             '臺東縣', '花蓮縣', '澎湖縣', '基隆市', '新竹市', '嘉義市', '金門縣', '連江縣',
             '高雄市', '臺南市', '臺中市', '桃園市', '臺北市', '新北市'],
    '總計_發生數': [7055, 6536, 7707, 15108, 6736, 8335, 6247, 9532, 3404, 5037, 1713, 6099, 5360, 4041, 1088, 166, 21457, 27520, 22081, 21024, 38433, 40967],
    '總計_破獲數': [6777, 5877, 6924, 15145, 6550, 7811, 6318, 8813, 3277, 4691, 1405, 5311, 5233, 3836, 881, 115, 21670, 25943, 21941, 21083, 39335, 39296],
    '總計_嫌疑犯': [8181, 6139, 7316, 18323, 8457, 8821, 8085, 9648, 3387, 4123, 1612, 6322, 5924, 4911, 1391, 175, 24131, 29484, 28099, 20958, 44648, 35707],
    '竊盜_發生數': [935, 857, 1302, 2340, 918, 1243, 875, 904, 503, 790, 150, 918, 879, 699, 104, 16, 3393, 3819, 3493, 2831, 4617, 6031],
    '詐欺背信_發生數': [1166, 1227, 1291, 1929, 1240, 1671, 798, 638, 529, 723, 474, 818, 584, 893, 363, 87, 2569, 5494, 2439, 1983, 4498, 7366],
    '傷害_發生數': [347, 250, 330, 818, 392, 334, 317, 555, 201, 345, 101, 438, 351, 215, 55, 8, 969, 1191, 1157, 960, 2513, 2291],
    '毒品_發生數': [665, 1112, 1220, 1509, 753, 1077, 830, 1729, 350, 681, 108, 898, 458, 690, 49, 3, 3054, 2646, 3378, 5343, 3316, 6087],
    '駕駛過失_發生數': [867, 545, 580, 1548, 463, 664, 552, 934, 275, 172, 101, 280, 586, 2, 109, 6, 2132, 3102, 782, 1599, 3890, 3331]
}

df = pd.DataFrame(data)

print("="*80)
print("           犯罪數據分析報告")
print("="*80)

# 基本統計分析
print("\n【1. 基本統計摘要】")
print(f"• 全台總犯罪發生數：{df['總計_發生數'].sum():,} 件")
print(f"• 全台總犯罪破獲數：{df['總計_破獲數'].sum():,} 件")
print(f"• 全台總嫌疑犯人數：{df['總計_嫌疑犯'].sum():,} 人")
print(f"• 全台平均破獲率：{(df['總計_破獲數'].sum() / df['總計_發生數'].sum() * 100):.2f}%")

# 計算破獲率
df['破獲率'] = (df['總計_破獲數'] / df['總計_發生數'] * 100).round(2)

# 犯罪發生數排名分析
print("\n【2. 犯罪發生數排名分析】")
top_5_crime = df.nlargest(5, '總計_發生數')
bottom_5_crime = df.nsmallest(5, '總計_發生數')

print(f"• 犯罪發生數最高的5個縣市：")
for i, (idx, row) in enumerate(top_5_crime.iterrows(), 1):
    print(f"  {i}. {row['縣市']}：{row['總計_發生數']:,} 件")

print(f"• 犯罪發生數最低的5個縣市：")
for i, (idx, row) in enumerate(bottom_5_crime.iterrows(), 1):
    print(f"  {i}. {row['縣市']}：{row['總計_發生數']:,} 件")

print(f"• 最高與最低縣市差距：{top_5_crime.iloc[0]['總計_發生數'] - bottom_5_crime.iloc[0]['總計_發生數']:,} 件")

# 破獲率分析
print("\n【3. 破獲率分析】")
best_solve_rate = df.nlargest(5, '破獲率')
worst_solve_rate = df.nsmallest(5, '破獲率')

print(f"• 破獲率最高的5個縣市：")
for i, (idx, row) in enumerate(best_solve_rate.iterrows(), 1):
    print(f"  {i}. {row['縣市']}：{row['破獲率']:.2f}%")

print(f"• 破獲率最低的5個縣市：")
for i, (idx, row) in enumerate(worst_solve_rate.iterrows(), 1):
    print(f"  {i}. {row['縣市']}：{row['破獲率']:.2f}%")

high_solve_rate = df[df['破獲率'] >= 95].shape[0]
medium_solve_rate = df[(df['破獲率'] >= 90) & (df['破獲率'] < 95)].shape[0]
low_solve_rate = df[df['破獲率'] < 90].shape[0]

print(f"• 破獲率分布：")
print(f"  - 破獲率 ≥ 95%：{high_solve_rate} 個縣市")
print(f"  - 破獲率 90-95%：{medium_solve_rate} 個縣市")
print(f"  - 破獲率 < 90%：{low_solve_rate} 個縣市")

# 犯罪類型分析
print("\n【4. 犯罪類型分析】")
crime_totals = {
    '竊盜': df['竊盜_發生數'].sum(),
    '詐欺背信': df['詐欺背信_發生數'].sum(),
    '傷害': df['傷害_發生數'].sum(),
    '毒品': df['毒品_發生數'].sum(),
    '駕駛過失': df['駕駛過失_發生數'].sum()
}

sorted_crimes = sorted(crime_totals.items(), key=lambda x: x[1], reverse=True)
total_analyzed_crimes = sum(crime_totals.values())

print(f"• 主要犯罪類型排名：")
for i, (crime_type, count) in enumerate(sorted_crimes, 1):
    percentage = (count / total_analyzed_crimes * 100)
    print(f"  {i}. {crime_type}：{count:,} 件 ({percentage:.1f}%)")

print(f"• 分析的五大犯罪類型佔總犯罪數的比例：{(total_analyzed_crimes / df['總計_發生數'].sum() * 100):.1f}%")

# 六都vs其他縣市分析
print("\n【5. 六都 vs 其他縣市分析】")
six_municipalities = ['臺北市', '新北市', '桃園市', '臺中市', '臺南市', '高雄市']
df['城市類型'] = df['縣市'].apply(lambda x: '六都' if x in six_municipalities else '其他縣市')

six_cities_data = df[df['城市類型'] == '六都']
other_cities_data = df[df['城市類型'] == '其他縣市']

six_cities_total = six_cities_data['總計_發生數'].sum()
other_cities_total = other_cities_data['總計_發生數'].sum()
six_cities_avg = six_cities_data['總計_發生數'].mean()
other_cities_avg = other_cities_data['總計_發生數'].mean()

print(f"• 六都總犯罪數：{six_cities_total:,} 件 ({six_cities_total / df['總計_發生數'].sum() * 100:.1f}%)")
print(f"• 其他縣市總犯罪數：{other_cities_total:,} 件 ({other_cities_total / df['總計_發生數'].sum() * 100:.1f}%)")
print(f"• 六都平均犯罪數：{six_cities_avg:,.0f} 件")
print(f"• 其他縣市平均犯罪數：{other_cities_avg:,.0f} 件")
print(f"• 六都平均犯罪數是其他縣市的 {six_cities_avg / other_cities_avg:.1f} 倍")

# 特殊發現
print("\n【6. 重要發現與結論】")

# 找出破獲數超過發生數的縣市
over_solve = df[df['總計_破獲數'] > df['總計_發生數']]
if not over_solve.empty:
    print(f"• 破獲數超過發生數的縣市（可能包含積案破獲）：")
    for idx, row in over_solve.iterrows():
        excess = row['總計_破獲數'] - row['總計_發生數']
        print(f"  - {row['縣市']}：超出 {excess} 件")

# 嫌疑犯與案件比例分析
df['嫌疑犯案件比'] = (df['總計_嫌疑犯'] / df['總計_發生數']).round(2)
high_suspect_ratio = df.nlargest(3, '嫌疑犯案件比')
print(f"• 每案件平均嫌疑犯人數最高的3個縣市：")
for i, (idx, row) in enumerate(high_suspect_ratio.iterrows(), 1):
    print(f"  {i}. {row['縣市']}：每案 {row['嫌疑犯案件比']:.2f} 人")

# 各犯罪類型的熱點縣市
print(f"• 各犯罪類型發生數最高的縣市：")
crime_columns = ['竊盜_發生數', '詐欺背信_發生數', '傷害_發生數', '毒品_發生數', '駕駛過失_發生數']
crime_names = ['竊盜', '詐欺背信', '傷害', '毒品', '駕駛過失']

for crime_col, crime_name in zip(crime_columns, crime_names):
    top_city = df.loc[df[crime_col].idxmax()]
    print(f"  - {crime_name}：{top_city['縣市']} ({top_city[crime_col]:,} 件)")

print("\n" + "="*80)

# 以下是原有的圖表生成代碼...

# 1. 總體案件數量比較圖（橫條圖）
plt.figure(figsize=(14, 10))
df_sorted = df.sort_values('總計_發生數', ascending=True)
plt.barh(df_sorted['縣市'], df_sorted['總計_發生數'], color='steelblue', alpha=0.7)
plt.xlabel('案件數', fontsize=12)
plt.ylabel('縣市', fontsize=12)
plt.title('各縣市刑事案件總發生數排名', fontsize=16, fontweight='bold')
plt.grid(axis='x', alpha=0.3)
for i, v in enumerate(df_sorted['總計_發生數']):
    plt.text(v + 200, i, str(v), va='center', fontsize=9)
plt.tight_layout()
plt.show()

# 2. 發生數 vs 破獲數 vs 嫌疑犯人數比較圖（保留原版）
fig, ax = plt.subplots(figsize=(16, 10))
x = np.arange(len(df['縣市']))
width = 0.25

bars1 = ax.bar(x - width, df['總計_發生數'], width, label='發生數', color='lightcoral', alpha=0.8)
bars2 = ax.bar(x, df['總計_破獲數'], width, label='破獲數', color='lightgreen', alpha=0.8)
bars3 = ax.bar(x + width, df['總計_嫌疑犯'], width, label='嫌疑犯人數', color='lightskyblue', alpha=0.8)

ax.set_xlabel('縣市', fontsize=12)
ax.set_ylabel('案件數/人數', fontsize=12)
ax.set_title('各縣市刑事案件發生數、破獲數與嫌疑犯人數比較', fontsize=16, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(df['縣市'], rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

# 3. 破獲率分析圖
plt.figure(figsize=(14, 8))
colors = ['red' if x < 90 else 'orange' if x < 95 else 'green' for x in df['破獲率']]
bars = plt.bar(df['縣市'], df['破獲率'], color=colors, alpha=0.7)
plt.xlabel('縣市', fontsize=12)
plt.ylabel('破獲率 (%)', fontsize=12)
plt.title('各縣市刑事案件破獲率', fontsize=16, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.axhline(y=90, color='red', linestyle='--', alpha=0.5, label='90%基準線')
plt.axhline(y=95, color='orange', linestyle='--', alpha=0.5, label='95%基準線')
plt.legend()
plt.grid(axis='y', alpha=0.3)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'{height}%', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.show()

# 4. 主要犯罪類型分析 - 熱力圖
crime_data = df[['縣市', '竊盜_發生數', '詐欺背信_發生數', '傷害_發生數', '毒品_發生數', '駕駛過失_發生數']].set_index('縣市')
crime_data.columns = ['竊盜', '詐欺背信', '傷害', '毒品', '駕駛過失']

plt.figure(figsize=(12, 16))
sns.heatmap(crime_data, annot=True, cmap='YlOrRd', fmt='d', cbar_kws={'label': '案件數'})
plt.title('各縣市主要犯罪類型發生數熱力圖', fontsize=16, fontweight='bold')
plt.xlabel('犯罪類型', fontsize=12)
plt.ylabel('縣市', fontsize=12)
plt.tight_layout()
plt.show()

# 5. 各犯罪類型在不同縣市的分布 - 堆疊圖
plt.figure(figsize=(16, 10))
bottom = np.zeros(len(df))
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
crime_types = ['竊盜_發生數', '詐欺背信_發生數', '傷害_發生數', '毒品_發生數', '駕駛過失_發生數']
crime_labels = ['竊盜', '詐欺背信', '傷害', '毒品', '駕駛過失']

for i, crime_type in enumerate(crime_types):
    plt.bar(df['縣市'], df[crime_type], bottom=bottom, label=crime_labels[i], 
            color=colors[i], alpha=0.8)
    bottom += df[crime_type]

plt.xlabel('縣市', fontsize=12)
plt.ylabel('案件數', fontsize=12)
plt.title('各縣市主要犯罪類型案件數分布（堆疊圖）', fontsize=16, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# 6. 前10大縣市犯罪類型比較 - 雷達圖
top_10_cities = df.nlargest(10, '總計_發生數')

fig, axes = plt.subplots(2, 5, figsize=(20, 8), subplot_kw=dict(projection='polar'))
axes = axes.flatten()

crime_types = ['竊盜_發生數', '詐欺背信_發生數', '傷害_發生數', '毒品_發生數', '駕駛過失_發生數']
crime_labels = ['竊盜', '詐欺背信', '傷害', '毒品', '駕駛過失']

for i, (idx, city_data) in enumerate(top_10_cities.iterrows()):
    ax = axes[i]
    
    values = [city_data[crime_type] for crime_type in crime_types]
    values += values[:1]  # 閉合雷達圖
    
    angles = np.linspace(0, 2 * np.pi, len(crime_labels), endpoint=False).tolist()
    angles += angles[:1]
    
    ax.plot(angles, values, 'o-', linewidth=2, alpha=0.7)
    ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(crime_labels, fontsize=8)
    ax.set_title(city_data['縣市'], fontsize=10, fontweight='bold', pad=20)
    ax.grid(True)

plt.suptitle('前10大縣市犯罪類型分析雷達圖', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# 7. 犯罪密度分析 - 散點圖
plt.figure(figsize=(12, 8))
plt.scatter(df['總計_發生數'], df['總計_嫌疑犯'], 
           s=df['總計_破獲數']/50, alpha=0.6, c=df['破獲率'], cmap='RdYlGn')
plt.colorbar(label='破獲率 (%)')
plt.xlabel('總發生數', fontsize=12)
plt.ylabel('總嫌疑犯人數', fontsize=12)
plt.title('各縣市犯罪發生數 vs 嫌疑犯人數關係圖\n（氣泡大小代表破獲數，顏色代表破獲率）', 
          fontsize=14, fontweight='bold')

for i, txt in enumerate(df['縣市']):
    plt.annotate(txt, (df['總計_發生數'].iloc[i], df['總計_嫌疑犯'].iloc[i]),
                xytext=(5, 5), textcoords='offset points', fontsize=8, alpha=0.7)

plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 8. 各縣市各種犯罪類型發生數比較圖（新增）
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

crime_comparisons = [
    ('竊盜_發生數', '竊盜案件發生數', 'crimson'),
    ('詐欺背信_發生數', '詐欺背信案件發生數', 'darkorange'),
    ('傷害_發生數', '傷害案件發生數', 'forestgreen'),
    ('毒品_發生數', '毒品案件發生數', 'purple'),
    ('駕駛過失_發生數', '駕駛過失案件發生數', 'navy'),
    ('總計_發生數', '總計案件發生數', 'darkslategray')
]

for i, (crime_col, title, color) in enumerate(crime_comparisons):
    ax = axes[i]
    df_sorted = df.sort_values(crime_col, ascending=False)
    
    bars = ax.bar(range(len(df_sorted)), df_sorted[crime_col], color=color, alpha=0.7)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel('縣市', fontsize=10)
    ax.set_ylabel('案件數', fontsize=10)
    ax.set_xticks(range(len(df_sorted)))
    ax.set_xticklabels(df_sorted['縣市'], rotation=45, ha='right', fontsize=8)
    ax.grid(axis='y', alpha=0.3)
    
    # 在柱子上標註數值
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                   f'{int(height)}', ha='center', va='bottom', fontsize=7)

plt.suptitle('各縣市不同犯罪類型發生數比較分析', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# 9. 犯罪類型佔比分析圓餅圖
total_crimes = {
    '竊盜': df['竊盜_發生數'].sum(),
    '詐欺背信': df['詐欺背信_發生數'].sum(),
    '傷害': df['傷害_發生數'].sum(),
    '毒品': df['毒品_發生數'].sum(),
    '駕駛過失': df['駕駛過失_發生數'].sum()
}

plt.figure(figsize=(10, 8))
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
plt.pie(total_crimes.values(), labels=total_crimes.keys(), autopct='%1.1f%%',
        colors=colors, startangle=90, explode=(0.05, 0.05, 0.05, 0.05, 0.05))
plt.title('全台主要犯罪類型比例分析', fontsize=16, fontweight='bold')
plt.axis('equal')
plt.tight_layout()
plt.show()

# 10. 六都vs其他縣市比較
city_comparison = df.groupby('城市類型')[['總計_發生數', '總計_破獲數', '總計_嫌疑犯']].sum()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# 總數比較
city_comparison.plot(kind='bar', ax=ax1, color=['lightcoral', 'lightgreen', 'lightskyblue'])
ax1.set_title('六都 vs 其他縣市犯罪統計比較', fontsize=14, fontweight='bold')
ax1.set_xlabel('城市類型', fontsize=12)
ax1.set_ylabel('案件數/人數', fontsize=12)
ax1.legend(['發生數', '破獲數', '嫌疑犯人數'])
ax1.tick_params(axis='x', rotation=0)

# 平均數比較
city_avg = df.groupby('城市類型')[['總計_發生數', '總計_破獲數', '總計_嫌疑犯']].mean()
city_avg.plot(kind='bar', ax=ax2, color=['salmon', 'lightseagreen', 'skyblue'])
ax2.set_title('六都 vs 其他縣市平均犯罪統計比較', fontsize=14, fontweight='bold')
ax2.set_xlabel('城市類型', fontsize=12)
ax2.set_ylabel('平均案件數/人數', fontsize=12)
ax2.legend(['平均發生數', '平均破獲數', '平均嫌疑犯人數'])
ax2.tick_params(axis='x', rotation=0)

plt.tight_layout()
plt.show()

print("\n" + "="*80)
print("所有圖表已生成完成！")
print(f"總共生成了10種不同類型的分析圖表：")
print("1. 總體案件數量比較圖（橫條圖）")
print("2. 發生數 vs 破獲數 vs 嫌疑犯人數比較圖")
print("3. 破獲率分析圖")
print("4. 主要犯罪類型分析熱力圖")
print("5. 各犯罪類型在不同縣市的分布堆疊圖")
print("6. 前10大縣市犯罪類型雷達圖")
print("7. 犯罪密度分析散點圖")
print("8. 各縣市各種犯罪類型發生數比較圖")
print("9. 犯罪類型佔比分析圓餅圖")
print("10. 六都vs其他縣市比較圖")
print("="*80)