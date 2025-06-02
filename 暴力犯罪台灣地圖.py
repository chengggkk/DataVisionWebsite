import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np

# 1. 準備犯罪數據
crime_data = {
    '地區': ['新北市', '臺北市', '桃園市', '臺中市', '臺南市', '高雄市', 
           '基隆市', '新竹縣', '苗栗縣', '彰化縣', '南投縣', '雲林縣',
           '嘉義縣', '屏東縣', '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣',
           '金門縣', '連江縣', '新竹市', '嘉義市'],
    '暴力犯罪總數': [73, 42, 29, 19, 46, 31, 18, 13, 10, 17, 17, 12,
                14, 17, 13, 8, 2, 11, 7, 3, 1, 13],
    '破獲率': [101.37, 104.76, 96.55, 100, 102.17, 103.23, 100, 100, 
            100, 100, 100, 108.33, 100, 94.12, 100, 112.5, 200, 
            109.09, 100, 66.67, 100, 100]
}
df = pd.DataFrame(crime_data)

# 2. 載入台灣地圖 GeoJSON
taiwan_gdf = gpd.read_file("https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/taiwan.geojson")

# 3. 統一縣市名稱格式
taiwan_gdf['name'] = taiwan_gdf['name'].str.replace('台', '臺')
df['地區'] = df['地區'].str.replace('台', '臺')

# 4. 合併數據時處理可能的缺失值
merged = taiwan_gdf.merge(df, left_on='name', right_on='地區', how='left')

# 填充缺失值
merged['暴力犯罪總數'] = merged['暴力犯罪總數'].fillna(0)
merged['破獲率'] = merged['破獲率'].fillna(0)

# 5. 設定中文字體 (macOS專用)
try:
    # 嘗試蘋方-繁
    zh_font = FontProperties(fname='/System/Library/Fonts/PingFang.ttc', size=12)
    plt.rcParams['font.sans-serif'] = ['PingFang TC']
except:
    try:
        # 嘗試華康黑體
        zh_font = FontProperties(fname='/System/Library/Fonts/STHeiti Medium.ttc', size=12)
        plt.rcParams['font.sans-serif'] = ['Heiti TC']
    except:
        # 最後嘗試
        zh_font = FontProperties(size=12)
        print("警告: 使用系統預設字體，中文可能無法正常顯示")

plt.rcParams['axes.unicode_minus'] = False

# 6. 創建犯罪總數地圖
fig, ax = plt.subplots(figsize=(12, 10))

# 使用手動分組避免自動分組錯誤
bins = [0, 5, 10, 20, 30, 50, 100]
merged.plot(column='暴力犯罪總數', cmap='OrRd', legend=True, 
           scheme='User_Defined', classification_kwds={'bins': bins},
           edgecolor='black', linewidth=0.5, ax=ax,
           legend_kwds={'title': '犯罪案件數', 'loc': 'lower right'})

# 添加縣市標籤
for idx, row in merged.iterrows():
    if row['暴力犯罪總數'] > 0:  # 只標記有數據的縣市
        ax.annotate(text=f"{row['地區']}\n{int(row['暴力犯罪總數'])}件", 
                   xy=row['geometry'].centroid.coords[0],
                   ha='center', fontsize=8, fontproperties=zh_font,
                   bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.7))

ax.set_title('台灣各縣市暴力犯罪統計 (2023年)', fontproperties=zh_font, fontsize=16)
ax.axis('off')

# 添加資料來源說明
plt.figtext(0.5, 0.01, "資料來源: 內政部警政署 | 製圖: Python GeoPandas", 
           ha="center", fontsize=10, fontproperties=zh_font)

plt.tight_layout()
plt.show()

# 7. 創建破獲率地圖
fig, ax = plt.subplots(figsize=(12, 10))

# 手動設定破獲率分組
bins = [0, 80, 90, 100, 110, 200]
merged.plot(column='破獲率', cmap='YlGnBu', legend=True, 
           scheme='User_Defined', classification_kwds={'bins': bins},
           edgecolor='black', linewidth=0.5, ax=ax,
           legend_kwds={'title': '破獲率(%)', 'loc': 'lower right'})

# 添加縣市標籤
for idx, row in merged.iterrows():
    if row['破獲率'] > 0:  # 只標記有數據的縣市
        ax.annotate(text=f"{row['地區']}\n{row['破獲率']:.1f}%", 
                   xy=row['geometry'].centroid.coords[0],
                   ha='center', fontsize=8, fontproperties=zh_font,
                   bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.7))

ax.set_title('台灣各縣市暴力犯罪破獲率 (2023年)', fontproperties=zh_font, fontsize=16)
ax.axis('off')

plt.figtext(0.5, 0.01, "資料來源: 內政部警政署 | 製圖: Python GeoPandas", 
           ha="center", fontsize=10, fontproperties=zh_font)

plt.tight_layout()
plt.show()