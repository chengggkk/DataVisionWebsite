import matplotlib.pyplot as plt
import numpy as np

# 設定中文字體（使用 macOS 內建字體）
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 數據準備
years = ['92', '93', '94', '95', '96', '97', '98', '99', '100', '101', 
         '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112']

# 各類竊盜案件發生數（重大竊盜、普通竊盜、汽車竊盜、機車竊盜）
categories = ['重大竊盜', '普通竊盜', '汽車竊盜', '機車竊盜']
data = {
    '重大竊盜': [352, 326, 396, 390, 321, 295, 203, 171, 144, 121, 96, 70, 71, 37, 32, 18, 33, 30, 16, 28, 19],
    '普通竊盜': [99697, 112818, 148105, 144513, 118393, 101335, 77659, 75820, 67436, 61220, 52579, 49476, 43478, 38666, 36825, 35652, 34725, 31469, 30040, 33013, 33465],
    '汽車竊盜': [48373, 50719, 48992, 33739, 31966, 28508, 19697, 17106, 11385, 8577, 6535, 6363, 5638, 4500, 3086, 2235, 1456, 1006, 821, 676, 803],
    '機車竊盜': [182233, 166457, 130661, 102919, 90411, 79213, 57592, 49677, 37866, 30346, 23286, 20421, 17068, 14403, 12082, 9686, 6058, 4511, 4190, 3953, 4052]
}

# 顏色設定
colors = ['#d62728', '#ff7f0e', '#1f77b4', '#2ca02c']

# 創建圖表
fig, ax = plt.subplots(figsize=(16, 8))

# 繪製堆疊長條圖
bottom = np.zeros(len(years))
for i, category in enumerate(categories):
    ax.bar(years, data[category], bottom=bottom, label=category, color=colors[i], alpha=0.8)
    bottom += data[category]

# 添加總案件數標籤（只顯示部分年份避免擁擠）
total_cases = [sum([data[cat][i] for cat in categories]) for i in range(len(years))]
for i in range(0, len(years), 2):  # 每隔一年顯示一個標籤
    ax.text(years[i], total_cases[i] + 5000, f'{total_cases[i]:,}', 
            ha='center', va='bottom', fontsize=8)

# 添加破獲率折線圖（使用右軸）
ax2 = ax.twinx()
clearance_rates = [53.92, 54.27, 57.27, 58.44, 62.26, 63.92, 65.89, 64.49, 66.44, 
                   70.18, 73.26, 77.59, 83.10, 84.88, 88.46, 90.90, 95.59, 98.87, 
                   99.31, 97.17, 98.34]
ax2.plot(years, clearance_rates, color='#9467bd', marker='o', linewidth=2, label='總破獲率(%)')
ax2.set_ylim(50, 110)
ax2.set_ylabel('破獲率 (%)', fontsize=12)

# 在折線圖上標註破獲率
for i, rate in enumerate(clearance_rates):
    if i % 2 == 0:  # 每隔一年顯示一個標籤
        ax2.text(years[i], rate+1, f'{rate:.1f}%', 
                ha='center', va='bottom', color='#9467bd', fontsize=8)

# 圖表裝飾
ax.set_title('民國92-112年竊盜案件類型分布與破獲率趨勢', fontsize=16, pad=20)
ax.set_xlabel('民國年份', fontsize=12)
ax.set_ylabel('案件發生數（件）', fontsize=12)
ax.grid(axis='y', linestyle='--', alpha=0.3)

# 合併圖例
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines + lines2, labels + labels2, loc='upper right', bbox_to_anchor=(1.15, 1))

plt.tight_layout()
plt.show()