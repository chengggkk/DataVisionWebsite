import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

# 中文字體（macOS 使用 PingFang）
chinese_font = FontProperties(fname="/System/Library/Fonts/PingFang.ttc", size=12)

# 年度與資料
years = np.array([92 + i for i in range(20)])
male = np.array([
    11416, 10852, 12924, 16845, 18437, 18051, 18691, 21352, 23258, 22770,
    22578, 21306, 20872, 22246, 22649, 23785, 25874, 26337, 27562, 29981
])
female = np.array([
    8456, 8120, 9530, 11778, 13747, 13368, 13872, 16160, 17051, 16877,
    17217, 16071, 16486, 16919, 16976, 17946, 19322, 19158, 20591, 22790
])
total = male + female

# 偏移設定，讓男女條形圖並排
bar_width = 0.35
x = np.arange(len(years))

# 畫圖
fig, ax = plt.subplots(figsize=(13, 6))

# 條形圖：男性與女性分開顯示
ax.bar(x - bar_width/2, male, width=bar_width, label='男性', color='skyblue')
ax.bar(x + bar_width/2, female, width=bar_width, label='女性', color='lightcoral')

# 折線圖：總計
ax.plot(x, total, label='總計（死傷人數）', color='black', marker='o', linewidth=2)

# 設定標籤與標題
ax.set_title('歷年刑事案件死傷人數（按性別與總計）', fontproperties=chinese_font)
ax.set_xlabel('年份', fontproperties=chinese_font)
ax.set_ylabel('人數', fontproperties=chinese_font)
ax.set_xticks(x)
ax.set_xticklabels([f'{y}年' for y in years], rotation=45, fontproperties=chinese_font)

# 顯示圖例
ax.legend(prop=chinese_font)

# 顯示圖表
plt.tight_layout()
plt.show()