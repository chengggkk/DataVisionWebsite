import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np

# 中文字體（macOS 使用 PingFang）
chinese_font = FontProperties(fname="/System/Library/Fonts/PingFang.ttc", size=11)

# 資料定義
categories = [
    "故意殺人", "過失殺人", "強盜", "擄人勒贖", "強制性交", "妨害風化",
    "違反槍砲刀械條例", "駕駛過失", "傷害", "一般傷害", "重傷害",
    "毀棄損壞", "妨害自由", "公共危險", "妨害公務", "其他"
]
male_counts = [106, 51, 41, 3, 0, 4, 10, 14613, 10867, 10847, 20, 51, 623, 3147, 264, 1087]
female_counts = [45, 27, 18, 0, 11, 105, 1, 13500, 6967, 6963, 4, 38, 320, 3001, 30, 674]

# 合計
totals = [m + f for m, f in zip(male_counts, female_counts)]

# 繪圖
y = np.arange(len(categories))

plt.figure(figsize=(10, 8))
plt.barh(y, male_counts, color='steelblue', label='男性')
plt.barh(y, female_counts, left=male_counts, color='lightcoral', label='女性')

# 標籤與標題
plt.yticks(y, categories, fontproperties=chinese_font)
plt.xlabel('人數', fontproperties=chinese_font)
plt.title('民國112年台灣各類犯罪案件受害者性別分佈', fontproperties=chinese_font)
plt.legend(prop=chinese_font)
plt.tight_layout()

# 顯示圖表
plt.show()