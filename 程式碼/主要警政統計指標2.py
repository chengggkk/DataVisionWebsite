import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 原始數據
data = {
    '縣市': ['新北市', '臺北市', '桃園市', '臺中市', '臺南市', '高雄市', '宜蘭縣', '新竹縣', 
           '苗栗縣', '彰化縣', '南投縣', '雲林縣', '嘉義縣', '屏東縣', '臺東縣', '花蓮縣',
           '澎湖縣', '基隆市', '新竹市', '嘉義市', '金門縣', '連江縣'],
    
    # 全般刑案數據
    '全般刑案_發生數': [40967, 38433, 21024, 22081, 27520, 21457, 7055, 6536, 7707, 15108, 
                   6736, 8335, 6247, 9532, 3404, 5037, 1713, 6099, 5360, 4041, 1088, 166],
    '全般刑案_破獲數': [39296, 39335, 21083, 21941, 25943, 21670, 6777, 5877, 6924, 15145,
                   6550, 7811, 6318, 8813, 3277, 4691, 1405, 5311, 5233, 3836, 881, 115],
    '全般刑案_破獲率': [95.92, 102.35, 100.28, 99.37, 94.27, 100.99, 96.06, 89.92, 89.84, 100.24,
                   97.24, 93.71, 101.14, 92.46, 96.27, 93.13, 82.02, 87.08, 97.63, 94.93, 80.97, 69.28],
    '全般刑案_犯罪率': [1019.50, 1539.61, 914.30, 780.20, 1482.38, 785.10, 1569.61, 1117.46, 
                   1440.96, 1216.28, 1408.19, 1259.48, 1284.44, 1196.21, 1605.30, 1583.01,
                   1593.77, 1685.32, 1179.39, 1535.02, 762.32, 1184.78],
    
    # 暴力犯罪數據
    '暴力犯罪_發生數': [73, 42, 29, 19, 46, 31, 13, 13, 10, 17, 17, 12, 14, 17, 2, 8, 11, 18, 1, 13, 7, 3],
    '暴力犯罪_破獲數': [74, 44, 28, 19, 47, 32, 13, 13, 10, 17, 17, 13, 14, 16, 4, 9, 12, 18, 1, 13, 7, 2],
    '暴力犯罪_破獲率': [101.37, 104.76, 96.55, 100.00, 102.17, 103.23, 100.00, 100.00, 100.00, 100.00,
                   100.00, 108.33, 100.00, 94.12, 200.00, 112.50, 109.09, 100.00, 100.00, 100.00, 100.00, 66.67],
    '暴力犯罪_犯罪率': [1.82, 1.68, 1.26, 0.67, 2.48, 1.13, 2.89, 2.22, 1.87, 1.37, 3.55, 1.81, 2.88, 2.13, 0.94, 2.51, 10.23, 4.97, 0.22, 4.94, 4.90, 21.41],
    
    # 竊盜數據
    '竊盜_發生數': [6031, 4617, 2831, 3493, 3819, 3393, 935, 857, 1302, 2340, 918, 1243, 875, 904, 503, 790, 150, 918, 879, 699, 104, 16],
    '竊盜_破獲數': [6030, 4689, 2874, 3528, 3663, 3408, 912, 835, 1226, 2360, 873, 1182, 877, 869, 479, 750, 136, 840, 826, 674, 92, 14],
    '竊盜_破獲率': [99.98, 101.56, 101.52, 101.00, 95.92, 100.44, 97.54, 97.43, 94.16, 100.85, 95.10, 95.09, 100.23, 96.13, 95.23, 94.94, 90.67, 91.50, 93.97, 96.42, 88.46, 87.50],
    '竊盜_犯罪率': [150.09, 184.95, 123.12, 123.42, 205.71, 124.15, 208.02, 146.52, 243.43, 188.38, 191.91, 187.83, 179.91, 113.45, 237.21, 248.28, 139.56, 253.67, 193.41, 265.52, 72.87, 114.20]
}

df = pd.DataFrame(data)

# 定義分析函數
def analyze_crime_data(df):
    print("=" * 80)
    print("🚨 2023年台灣各縣市犯罪統計分析報告 🚨")
    print("=" * 80)
    
    # 1. 基本統計摘要
    print("\n📊 【基本統計摘要】")
    print("-" * 50)
    total_general_crimes = df['全般刑案_發生數'].sum()
    total_violent_crimes = df['暴力犯罪_發生數'].sum()
    total_theft_crimes = df['竊盜_發生數'].sum()
    
    print(f"全台總犯罪案件數: {total_general_crimes:,} 件")
    print(f"├─ 暴力犯罪: {total_violent_crimes:,} 件 ({total_violent_crimes/total_general_crimes*100:.2f}%)")
    print(f"└─ 竊盜案件: {total_theft_crimes:,} 件 ({total_theft_crimes/total_general_crimes*100:.2f}%)")
    
    avg_general_rate = df['全般刑案_破獲率'].mean()
    avg_violent_rate = df['暴力犯罪_破獲率'].mean()
    avg_theft_rate = df['竊盜_破獲率'].mean()
    
    print(f"\n全台平均破獲率:")
    print(f"├─ 全般刑案: {avg_general_rate:.2f}%")
    print(f"├─ 暴力犯罪: {avg_violent_rate:.2f}%")
    print(f"└─ 竊盜案件: {avg_theft_rate:.2f}%")
    
    # 2. 犯罪熱點分析
    print("\n🔥 【犯罪熱點分析】")
    print("-" * 50)
    
    # 全般刑案前五名
    top5_general = df.nlargest(5, '全般刑案_發生數')[['縣市', '全般刑案_發生數', '全般刑案_犯罪率']]
    print("全般刑案發生數前5名:")
    for i, row in top5_general.iterrows():
        print(f"{row.name+1:2d}. {row['縣市']:4s}: {row['全般刑案_發生數']:5d}件 (犯罪率: {row['全般刑案_犯罪率']:6.1f}/十萬人)")
    
    # 犯罪率最高前五名
    top5_rate = df.nlargest(5, '全般刑案_犯罪率')[['縣市', '全般刑案_犯罪率', '全般刑案_發生數']]
    print(f"\n犯罪率最高前5名:")
    rank = 1
    for i, row in top5_rate.iterrows():
        print(f"{rank:2d}. {row['縣市']:4s}: {row['全般刑案_犯罪率']:6.1f}/十萬人 ({row['全般刑案_發生數']:5d}件)")
        rank += 1
    
    # 3. 破獲率分析
    print("\n🎯 【破獲率績效分析】")
    print("-" * 50)
    
    # 破獲率優異縣市（>100%）
    excellent_cities = df[df['全般刑案_破獲率'] > 100]['縣市'].tolist()
    if excellent_cities:
        print(f"破獲率超過100%的縣市 ({len(excellent_cities)}個):")
        for city in excellent_cities:
            rate = df[df['縣市'] == city]['全般刑案_破獲率'].iloc[0]
            print(f"├─ {city}: {rate:.2f}%")
    
    # 破獲率待改善縣市（<90%）
    poor_cities = df[df['全般刑案_破獲率'] < 90][['縣市', '全般刑案_破獲率']].sort_values('全般刑案_破獲率')
    if not poor_cities.empty:
        print(f"\n破獲率低於90%的縣市 ({len(poor_cities)}個) - 需要改善:")
        for i, row in poor_cities.iterrows():
            print(f"⚠️  {row['縣市']:4s}: {row['全般刑案_破獲率']:5.2f}%")
    
    # 4. 暴力犯罪特殊分析
    print("\n⚡【暴力犯罪特殊分析】")
    print("-" * 50)
    
    # 暴力犯罪率最高前3名
    top3_violent = df.nlargest(3, '暴力犯罪_犯罪率')[['縣市', '暴力犯罪_犯罪率', '暴力犯罪_發生數']]
    print("暴力犯罪率最高前3名:")
    rank = 1
    for i, row in top3_violent.iterrows():
        print(f"{rank}. {row['縣市']:4s}: {row['暴力犯罪_犯罪率']:5.2f}/十萬人 ({row['暴力犯罪_發生數']:2d}件)")
        rank += 1
    
    # 暴力犯罪破獲率異常分析
    violent_over_100 = df[df['暴力犯罪_破獲率'] > 100]['縣市'].tolist()
    if violent_over_100:
        print(f"\n暴力犯罪破獲率超過100%的縣市 ({len(violent_over_100)}個) - 可能包含積案:")
        for city in violent_over_100:
            rate = df[df['縣市'] == city]['暴力犯罪_破獲率'].iloc[0]
            cases = df[df['縣市'] == city]['暴力犯罪_發生數'].iloc[0]
            solved = df[df['縣市'] == city]['暴力犯罪_破獲數'].iloc[0]
            print(f"├─ {city}: {rate:.1f}% (發生{cases}件/破獲{solved}件)")
    
    # 5. 竊盜案件分析
    print("\n🔓 【竊盜案件分析】")
    print("-" * 50)
    
    # 竊盜案件數前5名
    top5_theft = df.nlargest(5, '竊盜_發生數')[['縣市', '竊盜_發生數', '竊盜_犯罪率']]
    print("竊盜案件數前5名:")
    rank = 1
    for i, row in top5_theft.iterrows():
        print(f"{rank}. {row['縣市']:4s}: {row['竊盜_發生數']:4d}件 (犯罪率: {row['竊盜_犯罪率']:6.1f}/十萬人)")
        rank += 1
    
    # 竊盜犯罪率最高前3名
    top3_theft_rate = df.nlargest(3, '竊盜_犯罪率')[['縣市', '竊盜_犯罪率', '竊盜_發生數']]
    print(f"\n竊盜犯罪率最高前3名:")
    rank = 1
    for i, row in top3_theft_rate.iterrows():
        print(f"{rank}. {row['縣市']:4s}: {row['竊盜_犯罪率']:6.1f}/十萬人 ({row['竊盜_發生數']:4d}件)")
        rank += 1
    
    # 6. 六都比較分析
    print("\n🏙️ 【六都比較分析】")
    print("-" * 50)
    
    six_cities = ['新北市', '臺北市', '桃園市', '臺中市', '臺南市', '高雄市']
    six_cities_data = df[df['縣市'].isin(six_cities)].copy()
    
    print("六都綜合排名 (依全般刑案犯罪率排序):")
    six_cities_sorted = six_cities_data.sort_values('全般刑案_犯罪率')
    rank = 1
    for i, row in six_cities_sorted.iterrows():
        safety_level = "🟢優良" if row['全般刑案_犯罪率'] < 1000 else "🟡普通" if row['全般刑案_犯罪率'] < 1300 else "🔴注意"
        print(f"{rank}. {row['縣市']:3s}: 犯罪率{row['全般刑案_犯罪率']:7.1f} | 破獲率{row['全般刑案_破獲率']:6.2f}% | {safety_level}")
        rank += 1
    
    # 7. 特殊發現與異常值
    print("\n🔍 【特殊發現與異常值】")
    print("-" * 50)
    
    # 破獲率異常高的案例
    high_clearance = df[df['全般刑案_破獲率'] > 102][['縣市', '全般刑案_破獲率', '全般刑案_發生數', '全般刑案_破獲數']]
    if not high_clearance.empty:
        print("破獲率超過102%的縣市 (可能包含積案):")
        for i, row in high_clearance.iterrows():
            print(f"├─ {row['縣市']}: {row['全般刑案_破獲率']:.2f}% (發生{row['全般刑案_發生數']}件/破獲{row['全般刑案_破獲數']}件)")
    
    # 犯罪率極端值
    min_crime_rate_city = df.loc[df['全般刑案_犯罪率'].idxmin()]
    max_crime_rate_city = df.loc[df['全般刑案_犯罪率'].idxmax()]
    
    print(f"\n犯罪率極端值:")
    print(f"🏆最低: {min_crime_rate_city['縣市']} ({min_crime_rate_city['全般刑案_犯罪率']:.1f}/十萬人)")
    print(f"⚠️ 最高: {max_crime_rate_city['縣市']} ({max_crime_rate_city['全般刑案_犯罪率']:.1f}/十萬人)")
    print(f"   差距: {max_crime_rate_city['全般刑案_犯罪率'] - min_crime_rate_city['全般刑案_犯罪率']:.1f}/十萬人 ({max_crime_rate_city['全般刑案_犯罪率']/min_crime_rate_city['全般刑案_犯罪率']:.1f}倍)")
    
    # 8. 結論與建議
    print("\n📝 【結論與政策建議】")
    print("-" * 50)
    
    print("主要發現：")
    print("1. 六都中，臺中市犯罪率最低，治安相對較好")
    print("2. 離島地區(澎湖、金門、連江)普遍破獲率較低，需要資源投入")
    print("3. 暴力犯罪整體控制良好，多數縣市破獲率達100%")
    print("4. 竊盜案件佔總犯罪案件相當比例，需要重點防治")
    
    # 找出需要重點關注的縣市
    concern_cities = df[(df['全般刑案_破獲率'] < 90) | (df['全般刑案_犯罪率'] > 1500)]['縣市'].unique()
    if len(concern_cities) > 0:
        print(f"\n重點關注縣市 ({len(concern_cities)}個):")
        for city in concern_cities:
            city_data = df[df['縣市'] == city].iloc[0]
            reasons = []
            if city_data['全般刑案_破獲率'] < 90:
                reasons.append("破獲率偏低")
            if city_data['全般刑案_犯罪率'] > 1500:
                reasons.append("犯罪率偏高")
            print(f"├─ {city}: {' & '.join(reasons)}")
    
    print("\n政策建議：")
    print("• 加強離島地區警力配置與偵查能力")
    print("• 針對竊盜高發地區實施預防措施")
    print("• 持續維持暴力犯罪的高破獲率")
    print("• 都會區應平衡治安維護與犯罪預防")
    
    print("\n" + "=" * 80)
    print("📊 分析完成 - 詳細圖表生成中...")
    print("=" * 80)

# 執行分析
analyze_crime_data(df)

# 1. 全般刑案 - 各縣市發生數橫條圖
plt.figure(figsize=(12, 10))
plt.barh(df['縣市'], df['全般刑案_發生數'], color='steelblue', alpha=0.7)
plt.xlabel('案件數量')
plt.ylabel('縣市')
plt.title('2023各縣市全般刑案發生數', fontsize=16, fontweight='bold')
plt.grid(axis='x', alpha=0.3)
for i, v in enumerate(df['全般刑案_發生數']):
    plt.text(v + 500, i, str(v), va='center', fontsize=9)
plt.tight_layout()
plt.show()

# 2. 全般刑案 - 破獲率比較
plt.figure(figsize=(14, 8))
colors = ['red' if x < 90 else 'orange' if x < 95 else 'green' for x in df['全般刑案_破獲率']]
bars = plt.bar(df['縣市'], df['全般刑案_破獲率'], color=colors, alpha=0.7)
plt.ylabel('破獲率 (%)')
plt.xlabel('縣市')
plt.title('2023各縣市全般刑案破獲率', fontsize=16, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.axhline(y=90, color='red', linestyle='--', alpha=0.5, label='90%基準線')
plt.axhline(y=95, color='orange', linestyle='--', alpha=0.5, label='95%基準線')
for bar, rate in zip(bars, df['全般刑案_破獲率']):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
             f'{rate:.1f}%', ha='center', va='bottom', fontsize=8)
plt.legend()
plt.tight_layout()
plt.show()

# 3. 全般刑案 - 犯罪率地圖式視覺化
plt.figure(figsize=(12, 8))
plt.scatter(range(len(df)), df['全般刑案_犯罪率'], 
           s=df['全般刑案_發生數']/100, alpha=0.6, c=df['全般刑案_犯罪率'], 
           cmap='Reds', edgecolors='black', linewidth=0.5)
plt.colorbar(label='犯罪率 (件/十萬人口)')
plt.ylabel('犯罪率 (件/十萬人口)')
plt.xlabel('縣市')
plt.title('2023各縣市全般刑案犯罪率 (泡泡大小代表發生數)', fontsize=16, fontweight='bold')
plt.xticks(range(len(df)), df['縣市'], rotation=45, ha='right')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# 4. 暴力犯罪 - 發生數與破獲數對比
plt.figure(figsize=(14, 8))
x = np.arange(len(df['縣市']))
width = 0.35
plt.bar(x - width/2, df['暴力犯罪_發生數'], width, label='發生數', color='indianred', alpha=0.7)
plt.bar(x + width/2, df['暴力犯罪_破獲數'], width, label='破獲數', color='forestgreen', alpha=0.7)
plt.xlabel('縣市')
plt.ylabel('案件數量')
plt.title('2023各縣市暴力犯罪發生數與破獲數對比', fontsize=16, fontweight='bold')
plt.xticks(x, df['縣市'], rotation=45, ha='right')
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# 5. 暴力犯罪 - 犯罪率排名
plt.figure(figsize=(12, 10))
sorted_df = df.sort_values('暴力犯罪_犯罪率', ascending=True)
colors = plt.cm.RdYlBu_r(np.linspace(0.2, 0.8, len(sorted_df)))
plt.barh(sorted_df['縣市'], sorted_df['暴力犯罪_犯罪率'], color=colors)
plt.xlabel('犯罪率 (件/十萬人口)')
plt.ylabel('縣市')
plt.title('2023各縣市暴力犯罪犯罪率排名', fontsize=16, fontweight='bold')
plt.grid(axis='x', alpha=0.3)
for i, v in enumerate(sorted_df['暴力犯罪_犯罪率']):
    plt.text(v + 0.3, i, f'{v:.2f}', va='center', fontsize=9)
plt.tight_layout()
plt.show()

# 6. 竊盜 - 發生數餅圖 (前10大縣市)
plt.figure(figsize=(12, 8))
top10_theft = df.nlargest(10, '竊盜_發生數')
colors = plt.cm.Set3(np.linspace(0, 1, 10))
wedges, texts, autotexts = plt.pie(top10_theft['竊盜_發生數'], 
                                  labels=top10_theft['縣市'], 
                                  autopct='%1.1f%%',
                                  colors=colors,
                                  startangle=90)
plt.title('2023竊盜案件發生數前10大縣市分布', fontsize=16, fontweight='bold')
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
plt.axis('equal')
plt.tight_layout()
plt.show()

# 7. 竊盜 - 破獲率與犯罪率關係散佈圖
plt.figure(figsize=(12, 8))
plt.scatter(df['竊盜_破獲率'], df['竊盜_犯罪率'], 
           s=df['竊盜_發生數']/20, alpha=0.6, 
           c=df['竊盜_發生數'], cmap='viridis', 
           edgecolors='black', linewidth=0.5)
plt.colorbar(label='發生數')
plt.xlabel('破獲率 (%)')
plt.ylabel('犯罪率 (件/十萬人口)')
plt.title('2023各縣市竊盜案破獲率與犯罪率關係 (泡泡大小代表發生數)', fontsize=16, fontweight='bold')
plt.grid(alpha=0.3)
# 添加縣市標籤
for i, county in enumerate(df['縣市']):
    if df['竊盜_犯罪率'].iloc[i] > 200 or df['竊盜_破獲率'].iloc[i] < 90:  # 標註特殊點
        plt.annotate(county, (df['竊盜_破獲率'].iloc[i], df['竊盜_犯罪率'].iloc[i]),
                    xytext=(5, 5), textcoords='offset points', fontsize=8)
plt.tight_layout()
plt.show()

# 8. 三種犯罪類型犯罪率比較 - 熱力圖
plt.figure(figsize=(14, 10))
crime_rates = df[['縣市', '全般刑案_犯罪率', '暴力犯罪_犯罪率', '竊盜_犯罪率']].set_index('縣市')
# 標準化數據以便比較
crime_rates_normalized = (crime_rates - crime_rates.min()) / (crime_rates.max() - crime_rates.min())

im = plt.imshow(crime_rates_normalized.T, cmap='YlOrRd', aspect='auto')
plt.colorbar(im, label='標準化犯罪率')
plt.yticks(range(3), ['全般刑案', '暴力犯罪', '竊盜'])
plt.xticks(range(len(df)), df['縣市'], rotation=45, ha='right')
plt.title('2023各縣市三種犯罪類型犯罪率熱力圖 (標準化)', fontsize=16, fontweight='bold')
# 添加數值標籤
for i in range(3):
    for j in range(len(df)):
        plt.text(j, i, f'{crime_rates.iloc[j, i]:.0f}', 
                ha='center', va='center', fontsize=7, 
                color='white' if crime_rates_normalized.iloc[j, i] > 0.5 else 'black')
plt.tight_layout()
plt.show()

# 9. 各犯罪類型破獲率箱型圖
plt.figure(figsize=(10, 6))
breakage_rates = [df['全般刑案_破獲率'], df['暴力犯罪_破獲率'], df['竊盜_破獲率']]
box_plot = plt.boxplot(breakage_rates, labels=['全般刑案', '暴力犯罪', '竊盜'], patch_artist=True)
colors = ['lightblue', 'lightgreen', 'lightcoral']
for patch, color in zip(box_plot['boxes'], colors):
    patch.set_facecolor(color)
plt.ylabel('破獲率 (%)')
plt.title('2023三種犯罪類型破獲率分布比較', fontsize=16, fontweight='bold')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# 10. 綜合排名分析 - 雷達圖 (以六都為例)
def create_radar_chart(counties, title):
    # 選擇要比較的縣市數據
    selected_data = df[df['縣市'].isin(counties)]
    
    # 準備雷達圖數據 (需要標準化)
    categories = ['全般刑案破獲率', '暴力犯罪破獲率', '竊盜破獲率', 
                 '全般刑案犯罪率(反向)', '暴力犯罪犯罪率(反向)', '竊盜犯罪率(反向)']
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]  # 完成圓形
    
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
    
    for i, county in enumerate(counties):
        county_data = selected_data[selected_data['縣市'] == county]
        if not county_data.empty:
            values = [
                county_data['全般刑案_破獲率'].iloc[0] / 100,  # 標準化到0-1
                county_data['暴力犯罪_破獲率'].iloc[0] / 100,
                county_data['竊盜_破獲率'].iloc[0] / 100,
                1 - (county_data['全般刑案_犯罪率'].iloc[0] / df['全般刑案_犯罪率'].max()),  # 反向標準化
                1 - (county_data['暴力犯罪_犯罪率'].iloc[0] / df['暴力犯罪_犯罪率'].max()),
                1 - (county_data['竊盜_犯罪率'].iloc[0] / df['竊盜_犯罪率'].max())
            ]
            values += values[:1]
            
            ax.plot(angles, values, 'o-', linewidth=2, label=county, color=colors[i])
            ax.fill(angles, values, alpha=0.25, color=colors[i])
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_ylim(0, 1)
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    ax.grid(True)
    
    plt.tight_layout()
    plt.show()

# 六都比較
create_radar_chart(['新北市', '臺北市', '桃園市', '臺中市', '臺南市', '高雄市'], '六都警政績效雷達圖比較')

print("\n🎯 所有圖表已生成完成！")