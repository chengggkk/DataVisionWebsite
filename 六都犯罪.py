import matplotlib.pyplot as plt
import pandas as pd


# 創建 DataFrame
df = pd.DataFrame("行政區犯罪人口率統計_縣市.csv", columns=['縣市代碼', '縣市', '總犯罪率', '少年犯罪率', '青年犯罪率', '成年犯罪率', '年份'])

# 設定圖表大小
fig, axes = plt.subplots(2, 3, figsize=(48, 16))  # 2x3 的子圖，axes 是 2D 陣列

# 1. 繪製六都犯罪率變化趨勢
ax1 = axes[0, 0]  # 左上角子圖
major_cities = ['臺北市', '新北市', '桃園市', '臺中市', '臺南市', '高雄市']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

for i, city in enumerate(major_cities):
    city_data = df[df['縣市'] == city].sort_values('年份')
    ax1.plot(city_data['年份'], city_data['總犯罪率'], marker='o', linewidth=2.5, 
             label=city, color=colors[i], markersize=6)

ax1.set_title('六都總犯罪率變化趨勢 (2015-2023)', fontsize=24, fontweight='bold', pad=20)
ax1.set_xlabel('年份', fontsize=20)
ax1.set_ylabel('犯罪人口率 (每十萬人)', fontsize=20)
ax1.legend(loc='upper left', fontsize=16)
ax1.grid(True, alpha=0.3)
ax1.set_xticks(range(2015, 2024))

# 其他子圖預留空間（可以依需求繪製其他資料）
# axes[0, 1], axes[0, 2], axes[1, 0], axes[1, 1], axes[1, 2]

plt.tight_layout()
plt.show()