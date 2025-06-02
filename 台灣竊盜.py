import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib import colormaps
from matplotlib.font_manager import FontProperties
import numpy as np

# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # Mac系統使用
# plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # Windows系統使用
plt.rcParams['axes.unicode_minus'] = False

# 1. 載入竊盜統計數據
df = pd.read_csv("竊盜統計2.csv", skiprows=3, encoding='utf-8')

# 清理數據 - 移除空行和無效數據
df = df.dropna(how='all')
df = df[df['機關別'] != '署所屬機關']  # 移除非縣市數據

# 2. 選擇需要的列並重命名
df = df[['機關別', '總          計']]
df.columns = ['County', 'Total_Larceny']

# 清理縣市名稱
df['County'] = df['County'].str.strip()

# 3. 載入台灣地理數據
geo_url = "https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/taiwan.geojson"
gdf = gpd.read_file(geo_url)

# 修正GeoJSON中的縣市名稱 (Taitung County有換行符)
gdf['name'] = gdf['name'].str.strip()

# 4. 創建縣市名稱映射表 (中文到英文)
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

# 特殊處理桃園市
gdf.loc[gdf['name'] == 'Taoyuan County', 'name'] = 'Taoyuan City'

# 5. 將中文縣市名轉換為英文
df['County_English'] = df['County'].map(county_mapping)

# 6. 合併地理數據與統計數據
merged = gdf.merge(df, left_on='name', right_on='County_English', how='left')

# 7. 數據清理 - 移除千位分隔符並轉換為數值
merged['Total_Larceny'] = merged['Total_Larceny'].str.replace(',', '').astype(float)

# 8. 創建地圖視覺化
fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(1, 2, width_ratios=[2, 1])  # 分割為左右兩部分
ax1 = fig.add_subplot(gs[0])  # 左邊放地圖
ax2 = fig.add_subplot(gs[1])  # 右邊放數據

# 繪製地圖
cmap = colormaps['OrRd']
norm = colors.Normalize(vmin=merged['Total_Larceny'].min(), vmax=merged['Total_Larceny'].max())

merged.plot(column='Total_Larceny', 
           cmap=cmap, 
           norm=norm,
           linewidth=0.8, 
           ax=ax1, 
           edgecolor='0.8',
           legend=True,
           legend_kwds={'label': "竊盜案件數", 'orientation': "horizontal", 'shrink': 0.6})


ax1.axis('off')

# 在右側創建數據表格
# 準備數據
table_data = merged[['County', 'Total_Larceny']].dropna()
table_data = table_data.sort_values('Total_Larceny', ascending=False)
table_data['Total_Larceny'] = table_data['Total_Larceny'].astype(int)

# 隱藏右側坐標軸
ax2.axis('off')

# 創建表格
table = ax2.table(cellText=table_data.values,
                 colLabels=['縣市', '案件數'],
                 loc='center',
                 cellLoc='center',
                 colColours=['#f7f7f7', '#f7f7f7'])

# 調整表格樣式
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1, 1.5)  # 調整表格大小


# 調整佈局
plt.tight_layout()

# 添加整體標題和數據來源說明
plt.suptitle('台灣地區竊盜案件統計分析', fontsize=18, y=0.98)
plt.figtext(0.1, 0.02, "數據來源: 各級警察機關偵辦刑案紀錄表", fontsize=10)

plt.show()