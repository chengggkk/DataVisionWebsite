import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import rcParams
import warnings
warnings.filterwarnings('ignore')

# 設定中文字體支持
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 資料輸入
data = {
    '案類別': ['竊盜總數', '暴力犯罪總數', '贓物', '賭博', '一般傷害', '詐欺背信', 
             '違反毒品危害防制條例', '妨害自由', '駕駛過失', '妨害婚姻及家庭', 
             '一般妨害風化', '侵占', '違反槍砲彈藥刀械管制條例', '公共危險', 
             '就業服務法', '其他'],
    '總計': [38339, 442, 66, 3118, 14384, 39028, 36435, 15105, 23783, 295, 
             5677, 10744, 1038, 40039, 3, 46772],
    '0-2時': [2686, 47, 0, 488, 1026, 1629, 3541, 987, 475, 38, 715, 811, 88, 3591, 1, 3881],
    '2-4時': [2715, 32, 4, 58, 787, 318, 1562, 547, 207, 12, 377, 259, 34, 2646, 1, 1476],
    '4-6時': [2368, 30, 0, 32, 506, 191, 880, 337, 378, 8, 227, 273, 35, 2284, 0, 1040],
    '6-8時': [2701, 17, 1, 32, 661, 350, 1477, 644, 2491, 17, 173, 478, 72, 2703, 0, 1582],
    '8-10時': [3681, 24, 9, 304, 978, 2697, 2589, 1266, 3177, 30, 331, 977, 81, 2728, 0, 5050],
    '10-12時': [4089, 38, 7, 319, 1323, 5197, 3033, 1519, 2857, 16, 438, 1114, 119, 2755, 1, 5491],
    '12-14時': [3809, 42, 9, 322, 1261, 6039, 3340, 1572, 2530, 30, 578, 1571, 124, 2493, 0, 5841],
    '14-16時': [3888, 47, 11, 390, 1390, 5398, 3634, 1580, 2546, 17, 564, 1118, 117, 3459, 0, 5114],
    '16-18時': [3926, 31, 10, 406, 1723, 5376, 3888, 1797, 3527, 31, 585, 1298, 117, 5676, 0, 4928],
    '18-20時': [3385, 48, 3, 329, 1715, 5114, 4075, 1817, 2742, 34, 547, 1166, 85, 3876, 0, 4682],
    '20-22時': [2838, 35, 10, 266, 1644, 4428, 4292, 1696, 1749, 36, 552, 1004, 83, 3757, 0, 4272],
    '22-24時': [2253, 51, 2, 172, 1370, 2290, 4124, 1343, 1104, 26, 590, 675, 83, 4071, 0, 3415]
}

# 創建DataFrame
df = pd.DataFrame(data)
crime_types = df['案類別'].tolist()
time_periods = ['0-2時', '2-4時', '4-6時', '6-8時', '8-10時', '10-12時', 
                '12-14時', '14-16時', '16-18時', '18-20時', '20-22時', '22-24時']

# 設定圖表大小和樣式
plt.style.use('default')
colors = plt.cm.Set3(np.linspace(0, 1, len(crime_types)))

# 1. 各案類別總案件數比較（橫條圖）
def plot_total_cases_comparison():
    plt.figure(figsize=(12, 10))
    sorted_indices = df['總計'].argsort()
    bars = plt.barh(range(len(crime_types)), [df['總計'].iloc[i] for i in sorted_indices], 
             color=[colors[i] for i in sorted_indices])
    plt.yticks(range(len(crime_types)), [crime_types[i] for i in sorted_indices])
    plt.xlabel('案件數')
    plt.title('2023年各類刑事案件發生數比較', fontsize=16, fontweight='bold')
    plt.grid(axis='x', alpha=0.3)
    for i, v in enumerate([df['總計'].iloc[j] for j in sorted_indices]):
        plt.text(v + 500, i, f'{v:,}', va='center', fontsize=9)
    plt.tight_layout()
    plt.show()

plot_total_cases_comparison()

# 2. 各時段總犯罪案件分布（折線圖）
def plot_time_distribution():
    plt.figure(figsize=(14, 8))
    total_by_time = [sum(df[period]) for period in time_periods]
    plt.plot(time_periods, total_by_time, marker='o', linewidth=3, markersize=8, color='crimson')
    plt.xlabel('時段')
    plt.ylabel('總案件數')
    plt.title('2023年各時段刑事案件發生數分布', fontsize=16, fontweight='bold')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    for i, v in enumerate(total_by_time):
        plt.annotate(f'{v:,}', (i, v), textcoords="offset points", xytext=(0,10), ha='center')
    plt.tight_layout()
    plt.show()

plot_time_distribution()

# 3. 主要犯罪類型的時間分布熱力圖
def plot_heatmap():
    plt.figure(figsize=(16, 10))
    # 選擇案件數較多的前10類犯罪
    top_crimes = df.nlargest(10, '總計')['案類別'].tolist()
    heatmap_data = []
    for crime in top_crimes:
        crime_row = df[df['案類別'] == crime]
        time_data = [crime_row[period].iloc[0] for period in time_periods]
        heatmap_data.append(time_data)

    sns.heatmap(heatmap_data, 
                xticklabels=time_periods, 
                yticklabels=top_crimes,
                annot=True, 
                fmt='d', 
                cmap='YlOrRd',
                cbar_kws={'label': '案件數'})
    plt.title('主要犯罪類型時間分布熱力圖', fontsize=16, fontweight='bold')
    plt.xlabel('時段')
    plt.ylabel('犯罪類型')
    plt.tight_layout()
    plt.show()

plot_heatmap()

# 4. 各案類別佔總犯罪比例（圓餅圖）
def plot_pie_chart():
    plt.figure(figsize=(12, 12))
    # 合併較小的類別
    total_cases = df['總計'].sum()
    major_crimes = df[df['總計'] > 5000].copy()
    minor_crimes_sum = df[df['總計'] <= 5000]['總計'].sum()

    pie_data = major_crimes['總計'].tolist() + [minor_crimes_sum]
    pie_labels = major_crimes['案類別'].tolist() + ['其他類型合計']
    colors_pie = plt.cm.Set3(np.linspace(0, 1, len(pie_data)))

    plt.pie(pie_data, labels=pie_labels, autopct='%1.1f%%', colors=colors_pie, startangle=90)
    plt.title('2023年各類刑事案件佔總犯罪比例', fontsize=16, fontweight='bold')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

plot_pie_chart()

# 5. 各時段各案類別詳細分布（堆疊柱狀圖）
def plot_stacked_bar():
    plt.figure(figsize=(16, 10))
    bottom = np.zeros(len(time_periods))
    for i, crime in enumerate(crime_types):
        crime_data = [df[df['案類別'] == crime][period].iloc[0] for period in time_periods]
        plt.bar(time_periods, crime_data, bottom=bottom, label=crime, color=colors[i])
        bottom += crime_data

    plt.xlabel('時段')
    plt.ylabel('案件數')
    plt.title('各時段各類刑事案件詳細分布（堆疊圖）', fontsize=16, fontweight='bold')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

plot_stacked_bar()

# 6. 個別犯罪類型時間分布圖（分別生成）
def plot_individual_crimes():
    for crime in crime_types:
        plt.figure(figsize=(12, 6))
        crime_data = [df[df['案類別'] == crime][period].iloc[0] for period in time_periods]
        
        plt.subplot(1, 2, 1)
        plt.bar(time_periods, crime_data, color=colors[crime_types.index(crime)], alpha=0.7)
        plt.title(f'{crime} - 各時段分布（柱狀圖）')
        plt.xlabel('時段')
        plt.ylabel('案件數')
        plt.xticks(rotation=45)
        plt.grid(axis='y', alpha=0.3)
        
        plt.subplot(1, 2, 2)
        plt.plot(time_periods, crime_data, marker='o', linewidth=2, markersize=6, 
                 color=colors[crime_types.index(crime)])
        plt.title(f'{crime} - 各時段分布（折線圖）')
        plt.xlabel('時段')
        plt.ylabel('案件數')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

plot_individual_crimes()

# 7. 犯罪高峰時段分析
def plot_peak_hours_analysis():
    plt.figure(figsize=(14, 8))
    peak_hours = {}
    for crime in crime_types:
        crime_data = [df[df['案類別'] == crime][period].iloc[0] for period in time_periods]
        peak_hour = time_periods[crime_data.index(max(crime_data))]
        peak_hours[crime] = peak_hour

    # 計算每個時段是多少類犯罪的高峰期
    peak_count = {}
    for period in time_periods:
        peak_count[period] = list(peak_hours.values()).count(period)

    plt.bar(peak_count.keys(), peak_count.values(), color='orange', alpha=0.7)
    plt.xlabel('時段')
    plt.ylabel('作為高峰期的犯罪類型數量')
    plt.title('各時段作為犯罪高峰期的統計', fontsize=16, fontweight='bold')
    plt.xticks(rotation=45)
    plt.grid(axis='y', alpha=0.3)
    for i, (k, v) in enumerate(peak_count.items()):
        plt.text(i, v + 0.1, str(v), ha='center', va='bottom')
    plt.tight_layout()
    plt.show()

plot_peak_hours_analysis()

# 主執行函數
def main():
    print("=== 台灣刑事案件統計分析 ===")
    print(f"總犯罪案件數：{df['總計'].sum():,} 件")
    print(f"最多的犯罪類型：{df.loc[df['總計'].idxmax(), '案類別']} ({df['總計'].max():,} 件)")
    print(f"最少的犯罪類型：{df.loc[df['總計'].idxmin(), '案類別']} ({df['總計'].min():,} 件)")

    # 各時段犯罪統計
    time_stats = {period: sum(df[period]) for period in time_periods}
    peak_time = max(time_stats, key=time_stats.get)
    low_time = min(time_stats, key=time_stats.get)
    print(f"犯罪最高峰時段：{peak_time} ({time_stats[peak_time]:,} 件)")
    print(f"犯罪最低峰時段：{low_time} ({time_stats[low_time]:,} 件)")
    
    print("\n正在生成圖表...")

# 執行主函數
if __name__ == "__main__":
    main()