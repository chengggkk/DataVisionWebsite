import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import pandas as pd

# 使用 Mac 支援的中文字體（可根據實際安裝情況調整）
# 常見選項："Heiti TC", "PingFang TC", "STHeiti"
font = FontProperties(fname="/System/Library/Fonts/STHeiti Light.ttc", size=12)

# 下載台灣地圖資料
geo_url = "https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/taiwan.geojson"
gdf = gpd.read_file(geo_url)

# 中文對照表
county_mapping = {
    '新北市': 'New Taipei City',
    '臺北市': 'Taipei City',
    '台北市': 'Taipei City',
    '桃園市': 'Taoyuan City',
    '臺中市': 'Taichung City',
    '台中市': 'Taichung City',
    '臺南市': 'Tainan City',
    '台南市': 'Tainan City',
    '高雄市': 'Kaohsiung City',
    '宜蘭縣': 'Yilan County',
    '新竹縣': 'Hsinchu County',
    '苗栗縣': 'Miaoli County',
    '彰化縣': 'Changhua County',
    '南投縣': 'Nantou County',
    '雲林縣': 'Yunlin County',
    '嘉義縣': 'Chiayi County',
    '屏東縣': 'Pingtung County',
    '臺東縣': 'Taitung County',
    '台東縣': 'Taitung County',
    '花蓮縣': 'Hualien County',
    '澎湖縣': 'Penghu County',
    '基隆市': 'Keelung City',
    '新竹市': 'Hsinchu City',
    '嘉義市': 'Chiayi City',
    '金門縣': 'Kinmen County',
    '連江縣': 'Lienchiang County'
}

# 數據
data = {
    '新北市': 7558,
    '臺北市': 7823,
    '桃園市': 4868,
    '臺中市': 6583,
    '臺南市': 4374,
    '高雄市': 7135,
    '宜蘭縣': 1295,
    '新竹縣': 1105,
    '苗栗縣': 1268,
    '彰化縣': 2830,
    '南投縣': 1448,
    '雲林縣': 1561,
    '嘉義縣': 1349,
    '屏東縣': 1963,
    '臺東縣': 1030,
    '花蓮縣': 1259,
    '澎湖縣': 743,
    '基隆市': 1119,
    '新竹市': 991,
    '嘉義市': 819,
    '金門縣': 342,
    '連江縣': 80
}

# 對應英文名與數值
eng_data = {county_mapping[k]: v for k, v in data.items() if k in county_mapping}

# 建立 DataFrame，並取得中心點
gdf["count"] = gdf["name"].map(eng_data)
gdf["centroid"] = gdf["geometry"].centroid
gdf["x"] = gdf["centroid"].x
gdf["y"] = gdf["centroid"].y

# 繪圖
fig, ax = plt.subplots(figsize=(10, 12))
gdf.plot(ax=ax, color="lightgray", edgecolor="black")

# 畫出氣泡（大小根據數值）
for _, row in gdf.dropna(subset=["count"]).iterrows():
    ax.scatter(row["x"], row["y"], s=row["count"] / 2, color="red", alpha=0.6, edgecolors='black', linewidth=0.5)

# 標題與格式
ax.set_title("台灣各縣市警備人數", fontproperties=font, fontsize=16)
ax.axis("off")
plt.show()