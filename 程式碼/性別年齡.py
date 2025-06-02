import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

# 設定中文字體（使用 macOS 內建字體）
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 使用 macOS 內建的中文字體
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# 數據
data = {
    "分類": ["總計", "竊盜總數", "暴力犯罪總數", "強制性交", "詐欺背信", 
            "妨害風化", "性交猥褻", "駕駛過失", "妨害家庭及婚姻", 
            "妨害公務", "公共危險", "其他"],
    "總計": [244563, 43064, 529, 92, 61440, 204, 5145, 28155, 331, 1043, 8034, 96618],
    "男性總計": [131720, 26911, 281, 4, 29576, 42, 473, 14635, 125, 914, 4385, 54378],
    "女性總計": [112843, 16153, 248, 88, 31864, 162, 4672, 13520, 206, 129, 3649, 42240],
    # 年齡組數據 (總計, 男, 女) 順序: 兒童, 少年, 青年, 成年, 壯年, 老年, 不詳
    "兒童": [(2047, 777, 1270), (30, 15, 15), (19, 5, 14), (11, 0, 11), (12, 6, 6), 
            (6, 1, 5), (496, 65, 431), (374, 196, 178), (11, 3, 8), (0, 0, 0), 
            (108, 65, 43), (991, 421, 570)],
    "少年": [(9222, 4086, 5136), (1115, 804, 311), (39, 11, 28), (28, 2, 26), (1012, 571, 441), 
            (22, 5, 17), (2037, 226, 1811), (668, 423, 245), (94, 7, 87), (2, 2, 0), 
            (227, 131, 96), (4006, 1906, 2100)],
    "青年": [(30638, 16457, 14181), (3875, 2478, 1397), (60, 32, 28), (14, 0, 14), (10466, 5224, 5242), 
            (50, 6, 44), (819, 57, 762), (4254, 2488, 1766), (1, 1, 0), (85, 78, 7), 
            (1371, 760, 611), (9657, 5333, 4324)],
    "成年": [(85297, 46628, 38669), (15315, 9629, 5686), (172, 97, 75), (31, 1, 30), (24405, 12011, 12394), 
            (75, 15, 60), (1198, 77, 1121), (8216, 4514, 3702), (92, 38, 54), (681, 591, 90), 
            (2623, 1480, 1143), (32520, 18176, 14344)],
    "壯年": [(94629, 51271, 43358), (18889, 11541, 7348), (173, 97, 76), (7, 1, 6), (20038, 9036, 11002), 
            (49, 13, 36), (538, 37, 501), (10590, 5176, 5414), (130, 73, 57), (235, 204, 31), 
            (2744, 1457, 1287), (41243, 23637, 17606)],
    "老年": [(21870, 11660, 10210), (3611, 2233, 1378), (64, 37, 27), (1, 0, 1), (5465, 2686, 2779), 
            (1, 1, 0), (49, 3, 46), (4052, 1837, 2215), (3, 3, 0), (9, 8, 1), 
            (942, 473, 469), (7674, 4379, 3295)],
    "不詳": [(860, 841, 19), (229, 211, 18), (2, 2, 0), (0, 0, 0), (42, 42, 0), 
            (1, 1, 0), (8, 8, 0), (1, 1, 0), (0, 0, 0), (31, 31, 0), 
            (19, 19, 0), (527, 526, 1)]
}

# 創建DataFrame
df = pd.DataFrame(data)

# 設置顏色
age_colors = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69']
age_groups = ["兒童", "少年", "青年", "成年", "壯年", "老年", "不詳"]

# 繪圖
fig, ax = plt.subplots(figsize=(16, 10), dpi=100)

# 設置條形圖的位置和寬度
bar_width = 0.35
index = np.arange(len(df))

# 繪製男性條形圖 (堆疊)
bottom_m = np.zeros(len(df))
for i, age_group in enumerate(age_groups):
    male_values = [x[1] for x in df[age_group]]
    ax.bar(index - bar_width/2, male_values, bar_width, 
           color=age_colors[i], bottom=bottom_m, edgecolor='white', linewidth=0.5)
    bottom_m += male_values

# 繪製女性條形圖 (堆疊)
bottom_f = np.zeros(len(df))
for i, age_group in enumerate(age_groups):
    female_values = [x[2] for x in df[age_group]]
    ax.bar(index + bar_width/2, female_values, bar_width, 
           color=age_colors[i], bottom=bottom_f, alpha=0.7, edgecolor='white', linewidth=0.5)
    bottom_f += female_values

# 只在「總計」條形圖上標註性別
total_index = np.where(df["分類"] == "總計")[0][0]  # 找到「總計」的索引位置

# 在「總計」男性條形圖上添加標註
ax.text(total_index - bar_width/2, bottom_m[total_index]/2, '男性', 
        ha='center', va='center', color='black', fontsize=12, fontweight='bold')

# 在「總計」女性條形圖上添加標註
ax.text(total_index + bar_width/2, bottom_f[total_index]/2, '女性', 
        ha='center', va='center', color='black', fontsize=12, fontweight='bold')

# 添加標籤和標題
ax.set_xlabel('犯罪分類', fontsize=12)
ax.set_ylabel('人數', fontsize=12)
ax.set_title('刑事案件被害者統計分析（按性別與年齡層）', fontsize=16, pad=20)
ax.set_xticks(index)
ax.set_xticklabels(df["分類"], rotation=45, ha="right", fontsize=10)
ax.grid(axis='y', linestyle='--', alpha=0.7)

# 創建自定義圖例（顯示所有年齡層）
legend_patches = [plt.Rectangle((0,0),1,1, fc=color) for color in age_colors]
ax.legend(legend_patches, age_groups, 
          bbox_to_anchor=(1.05, 1), loc='upper left', 
          title='年齡層', borderaxespad=0., fontsize=10)

plt.tight_layout()

# 顯示圖表
plt.show()