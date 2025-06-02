import matplotlib.pyplot as plt
import numpy as np

# 設定中文字體（使用 macOS 內建字體）
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 數據
years = ['92', '93', '94', '95', '96', '97', '98', '99', '100', '101', 
         '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112']
cases = [12966, 12706, 14301, 12226, 9534, 8117, 6764, 5312, 4190, 3461, 
         2525, 2289, 1956, 1627, 1260, 993, 859, 707, 598, 499, 442]
clearance_rates = [71.55, 62.36, 59.28, 64.63, 75.04, 79.99, 84.65, 88.18, 94.11, 96.94, 
                  97.27, 97.60, 102.66, 101.78, 102.62, 100.20, 104.54, 104.24, 99.83, 99.60, 102.04]

# 創建圖表和雙軸
fig, ax1 = plt.subplots(figsize=(14, 8))

# 柱狀圖（發生數）
bars = ax1.bar(years, cases, color='#1f77b4', alpha=0.7, label='發生數（件）')
ax1.set_xlabel('民國年份', fontsize=12)
ax1.set_ylabel('刑案發生數（件）', fontsize=12)
ax1.tick_params(axis='y')
ax1.set_ylim(0, max(cases)*1.2)

# 在柱子上方添加數據標籤
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height):,}',
             ha='center', va='bottom', fontsize=8)

# 第二個y軸（破獲率）
ax2 = ax1.twinx()
line = ax2.plot(years, clearance_rates, color='#ff7f0e', marker='o', linewidth=2, label='破獲率（%）')
ax2.set_ylabel('破獲率（%）', fontsize=12)
ax2.set_ylim(50, 110)
ax2.tick_params(axis='y')

# 在折線圖上添加數據標籤
for i, rate in enumerate(clearance_rates):
    ax2.text(i, rate+1, f'{rate:.1f}%', 
            ha='center', va='bottom', color='#ff7f0e', fontsize=8)

# 添加標題和圖例
plt.title('民國92-112年刑案發生數與破獲率趨勢分析', fontsize=16, pad=20)

# 合併圖例
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper right')

# 添加網格線
ax1.grid(axis='y', linestyle='--', alpha=0.7)

# 突出顯示最高和最低值
max_case_idx = np.argmax(cases)
min_case_idx = np.argmin(cases)
bars[max_case_idx].set_color('#d62728')
bars[min_case_idx].set_color('#2ca02c')

plt.tight_layout()
plt.show()