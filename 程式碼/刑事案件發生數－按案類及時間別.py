import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import rcParams
import pandas as pd

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 時間段標籤
time_periods = ['0-2時', '2-4時', '4-6時', '6-8時', '8-10時', '10-12時', 
                '12-14時', '14-16時', '16-18時', '18-20時', '20-22時', '22-24時']

# 原始資料
crime_time_data = {
    '總計': [20004, 11035, 8589, 13399, 23922, 28316, 29561, 29273, 33319, 29618, 26662, 21569],
    '竊盜總數': [2686, 2715, 2368, 2701, 3681, 4089, 3809, 3888, 3926, 3385, 2838, 2253],
    '暴力犯罪總數': [47, 32, 30, 17, 24, 38, 42, 47, 31, 48, 35, 51],
    '賭博': [488, 58, 32, 32, 304, 319, 322, 390, 406, 329, 266, 172],
    '一般傷害': [1026, 787, 506, 661, 978, 1323, 1261, 1390, 1723, 1715, 1644, 1370],
    '詐欺背信': [1629, 318, 191, 350, 2697, 5197, 6039, 5398, 5376, 5114, 4428, 2290],
    '違反毒品危害防制條例': [3541, 1562, 880, 1477, 2589, 3033, 3340, 3634, 3888, 4075, 4292, 4124],
    '妨害自由': [987, 547, 337, 644, 1266, 1519, 1572, 1580, 1797, 1817, 1696, 1343],
    '駕駛過失': [475, 207, 378, 2491, 3177, 2857, 2530, 2546, 3527, 2742, 1749, 1104],
    '一般妨害風化': [715, 377, 227, 173, 331, 438, 578, 564, 585, 547, 552, 590],
    '侵占': [811, 259, 273, 478, 977, 1114, 1571, 1118, 1298, 1166, 1004, 675],
    '違反槍砲彈藥刀械管制條例': [88, 34, 35, 72, 81, 119, 124, 117, 117, 85, 83, 83],
    '公共危險': [3591, 2646, 2284, 2703, 2728, 2755, 2493, 3459, 5676, 3876, 3757, 4071],
    '其他': [3881, 1476, 1040, 1582, 5050, 5491, 5841, 5114, 4928, 4682, 4272, 3415]
}

# 1. 全天24小時犯罪總數分布折線圖
def plot_total_crime_by_time():
    plt.figure(figsize=(14, 8))
    total_crimes = crime_time_data['總計']
    
    plt.plot(time_periods, total_crimes, marker='o', linewidth=3, markersize=8, 
             color='darkred', alpha=0.8)
    plt.fill_between(time_periods, total_crimes, alpha=0.3, color='lightcoral')
    
    plt.title('2023年刑事案件24小時分布趨勢', fontsize=16, fontweight='bold')
    plt.xlabel('時間段')
    plt.ylabel('案件發生數')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    
    # 標註最高峰和最低谷
    max_idx = total_crimes.index(max(total_crimes))
    min_idx = total_crimes.index(min(total_crimes))
    
    plt.annotate(f'高峰期\n{max(total_crimes):,}件', 
                xy=(time_periods[max_idx], max(total_crimes)),
                xytext=(max_idx-1, max(total_crimes)+2000),
                arrowprops=dict(arrowstyle='->', color='red'),
                fontsize=12, ha='center')
    
    plt.annotate(f'低谷期\n{min(total_crimes):,}件', 
                xy=(time_periods[min_idx], min(total_crimes)),
                xytext=(min_idx+1, min(total_crimes)+5000),
                arrowprops=dict(arrowstyle='->', color='blue'),
                fontsize=12, ha='center')
    
    plt.tight_layout()
    plt.show()

# 2. 主要犯罪類型時間分布熱力圖
def plot_crime_heatmap():
    # 選擇主要犯罪類型
    major_crimes = ['竊盜總數', '詐欺背信', '違反毒品危害防制條例', '一般傷害', 
                    '妨害自由', '駕駛過失', '公共危險']
    
    # 準備熱力圖資料
    heatmap_data = []
    for crime in major_crimes:
        heatmap_data.append(crime_time_data[crime])
    
    plt.figure(figsize=(16, 8))
    
    # 正規化資料以便比較
    heatmap_data_normalized = []
    for row in heatmap_data:
        total = sum(row)
        normalized = [x/total*100 for x in row]
        heatmap_data_normalized.append(normalized)
    
    sns.heatmap(heatmap_data_normalized, 
                xticklabels=time_periods,
                yticklabels=major_crimes,
                annot=True, fmt='.1f', cmap='YlOrRd',
                cbar_kws={'label': '占該犯罪類型比例(%)'})
    
    plt.title('主要犯罪類型24小時分布熱力圖 (比例)', fontsize=16, fontweight='bold')
    plt.xlabel('時間段')
    plt.ylabel('犯罪類型')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# 3. 特定犯罪類型時間分布比較
def plot_specific_crimes_comparison():
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 竊盜案件時間分布
    ax1.bar(time_periods, crime_time_data['竊盜總數'], color='steelblue', alpha=0.7)
    ax1.set_title('竊盜案件時間分布', fontweight='bold')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(axis='y', alpha=0.3)
    
    # 詐欺背信案件時間分布
    ax2.bar(time_periods, crime_time_data['詐欺背信'], color='orange', alpha=0.7)
    ax2.set_title('詐欺背信案件時間分布', fontweight='bold')
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(axis='y', alpha=0.3)
    
    # 駕駛過失案件時間分布
    ax3.bar(time_periods, crime_time_data['駕駛過失'], color='green', alpha=0.7)
    ax3.set_title('駕駛過失案件时间分布', fontweight='bold')
    ax3.tick_params(axis='x', rotation=45)
    ax3.grid(axis='y', alpha=0.3)
    
    # 毒品犯罪案件時間分布
    ax4.bar(time_periods, crime_time_data['違反毒品危害防制條例'], color='purple', alpha=0.7)
    ax4.set_title('毒品犯罪案件時間分布', fontweight='bold')
    ax4.tick_params(axis='x', rotation=45)
    ax4.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# 4. 犯罪高峰時段分析圓餅圖
def plot_peak_hours_analysis():
    # 將24小時分為4個時段
    time_groups = {
        '深夜時段(22-6時)': sum([crime_time_data['總計'][i] for i in [0, 1, 2, 11]]),
        '上午時段(6-12時)': sum([crime_time_data['總計'][i] for i in [3, 4, 5]]),
        '下午時段(12-18時)': sum([crime_time_data['總計'][i] for i in [6, 7, 8]]),
        '晚間時段(18-22時)': sum([crime_time_data['總計'][i] for i in [9, 10]])
    }
    
    plt.figure(figsize=(10, 8))
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
    
    wedges, texts, autotexts = plt.pie(time_groups.values(), 
                                       labels=time_groups.keys(),
                                       colors=colors,
                                       autopct='%1.1f%%',
                                       startangle=90)
    
    plt.title('刑事案件時段分布比例', fontsize=16, fontweight='bold')
    
    # 添加圖例
    plt.legend(wedges, [f'{label}: {value:,}件' for label, value in time_groups.items()],
               title="時段統計", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    
    plt.tight_layout()
    plt.show()

# 5. 多種犯罪類型疊加面積圖
def plot_stacked_area_chart():
    major_crimes = ['竊盜總數', '詐欺背信', '違反毒品危害防制條例', '一般傷害', 
                    '妨害自由', '駕駛過失']
    
    plt.figure(figsize=(16, 10))
    
    # 準備資料
    data_matrix = np.array([crime_time_data[crime] for crime in major_crimes])
    
    # 創建疊加面積圖
    colors = plt.cm.Set3(np.linspace(0, 1, len(major_crimes)))
    plt.stackplot(range(len(time_periods)), *data_matrix, 
                  labels=major_crimes, colors=colors, alpha=0.8)
    
    plt.title('主要犯罪類型24小時疊加分布圖', fontsize=16, fontweight='bold')
    plt.xlabel('時間段')
    plt.ylabel('案件數量')
    plt.xticks(range(len(time_periods)), time_periods, rotation=45)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# 6. 特殊犯罪類型雷達圖對比
def plot_crime_radar_comparison():
    from math import pi
    
    # 選擇特殊犯罪類型進行對比
    special_crimes = ['賭博', '一般妨害風化', '違反槍砲彈藥刀械管制條例', '暴力犯罪總數']
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12), subplot_kw=dict(projection='polar'))
    axes = axes.flatten()
    
    angles = [n / float(len(time_periods)) * 2 * pi for n in range(len(time_periods))]
    angles += angles[:1]  # 完成圓形
    
    for i, crime in enumerate(special_crimes):
        values = crime_time_data[crime]
        values += values[:1]  # 完成圓形
        
        ax = axes[i]
        ax.plot(angles, values, 'o-', linewidth=2, label=crime)
        ax.fill(angles, values, alpha=0.25)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(time_periods, fontsize=8)
        ax.set_title(f'{crime}\n24小時分布模式', fontsize=12, fontweight='bold')
        ax.grid(True)
        ax.set_ylim(0, max(values) * 1.1 if max(values) > 0 else 1)
    
    plt.tight_layout()
    plt.show()

# 7. 犯罪密度時間分布圖
def plot_crime_density():
    plt.figure(figsize=(14, 8))
    
    # 計算每個時段的犯罪密度指數（以平均值為基準）
    total_crimes = crime_time_data['總計']
    average = sum(total_crimes) / len(total_crimes)
    density_index = [crime / average for crime in total_crimes]
    
    colors = ['green' if d < 0.8 else 'yellow' if d < 1.2 else 'red' for d in density_index]
    
    bars = plt.bar(time_periods, density_index, color=colors, alpha=0.7)
    plt.axhline(y=1, color='black', linestyle='--', alpha=0.5, label='平均線')
    
    plt.title('犯罪密度指數時間分布 (以日平均為基準)', fontsize=16, fontweight='bold')
    plt.xlabel('時間段')
    plt.ylabel('密度指數 (1.0 = 日平均)')
    plt.xticks(rotation=45)
    plt.grid(axis='y', alpha=0.3)
    
    # 添加數值標籤
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{height:.2f}', ha='center', va='bottom', fontsize=10)
    
    # 圖例
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='green', alpha=0.7, label='低密度(<0.8)'),
                      Patch(facecolor='yellow', alpha=0.7, label='中密度(0.8-1.2)'),
                      Patch(facecolor='red', alpha=0.7, label='高密度(>1.2)')]
    plt.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    plt.show()

# 8. 各時段主要犯罪類型排名
def plot_top_crimes_by_time():
    # 選擇幾個重要時段進行分析
    key_times = ['2-4時', '8-10時', '14-16時', '20-22時']
    key_indices = [1, 4, 7, 10]
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    
    major_crimes = ['竊盜總數', '詐欺背信', '違反毒品危害防制條例', 
                    '一般傷害', '妨害自由', '駕駛過失', '公共危險']
    
    for i, (time_label, time_idx) in enumerate(zip(key_times, key_indices)):
        crime_counts = [(crime, crime_time_data[crime][time_idx]) for crime in major_crimes]
        crime_counts.sort(key=lambda x: x[1], reverse=True)
        
        crimes, counts = zip(*crime_counts)
        
        ax = axes[i]
        bars = ax.barh(crimes, counts, color='skyblue', alpha=0.8)
        ax.set_title(f'{time_label} 犯罪類型排名', fontweight='bold')
        ax.set_xlabel('案件數')
        
        # 在條形右側顯示數值
        for bar in bars:
            width = bar.get_width()
            ax.text(width + width*0.01, bar.get_y() + bar.get_height()/2, 
                   f'{int(width)}', ha='left', va='center', fontsize=9)
    
    plt.tight_layout()
    plt.show()

# 執行所有圖表生成
if __name__ == "__main__":
    print("生成圖表1: 全天24小時犯罪總數分布折線圖")
    plot_total_crime_by_time()
    
    print("生成圖表2: 主要犯罪類型時間分布熱力圖")
    plot_crime_heatmap()
    
    print("生成圖表3: 特定犯罪類型時間分布比較")
    plot_specific_crimes_comparison()
    
    print("生成圖表4: 犯罪高峰時段分析圓餅圖")
    plot_peak_hours_analysis()
    
    print("生成圖表5: 多種犯罪類型疊加面積圖")
    plot_stacked_area_chart()
    
    print("生成圖表6: 特殊犯罪類型雷達圖對比")
    plot_crime_radar_comparison()
    
    print("生成圖表7: 犯罪密度時間分布圖")
    plot_crime_density()
    
    print("生成圖表8: 各時段主要犯罪類型排名")
    plot_top_crimes_by_time()
    
    print("所有時間分布圖表生成完成！")