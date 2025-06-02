import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import requests

# Load and clean the crime data
df = pd.read_csv("行政區犯罪人口率統計/104年行政區犯罪人口率統計_縣市.csv", skiprows=1, encoding='big5')
# Clean data
df = df.rename(columns={
    '縣市名稱': 'County',
    '犯罪人口率': 'Crime_Rate'
})
# Convert crime rate to numeric
df['Crime_Rate'] = pd.to_numeric(df['Crime_Rate'], errors='coerce')
df = df.dropna()
# Create county name mapping for GeoJSON matching
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

# Map county names to English
df['County_English'] = df['County'].map(county_mapping)

# Load Taiwan GeoJSON data
geojson_url = "https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/taiwan.geojson"

try:
    # Try to load GeoJSON from URL
    response = requests.get(geojson_url)
    taiwan_geojson = response.json()
    
    # Fix Taoyuan County -> Taoyuan City in GeoJSON
    for feature in taiwan_geojson['features']:
        if feature['properties']['name'] == 'Taoyuan County':
            feature['properties']['name'] = 'Taoyuan City'
    # Create the choropleth map
    fig = px.choropleth(
        df,
        geojson=taiwan_geojson,
        locations='County_English',
        color='Crime_Rate',
        hover_name='County',
        hover_data={'County_English': False, 'Crime_Rate': ':,.1f'},
        featureidkey="properties.name",
        color_continuous_scale='Reds',
        range_color=(df['Crime_Rate'].min(), df['Crime_Rate'].max()),
        title='台灣各縣市犯罪人口率分布圖 (民國104年)<br>Taiwan Crime Rate Distribution by County/City',
        labels={'Crime_Rate': '犯罪人口率'}
    )
    # Update layout for better Taiwan map display
    fig.update_geos(
        projection_type="mercator",
        showland=True,
        landcolor="rgb(243, 243, 243)",
        coastlinecolor="rgb(204, 204, 204)",
        showocean=True,
        oceancolor="rgb(230, 245, 255)",
        showlakes=True,
        lakecolor="rgb(230, 245, 255)",
        fitbounds="locations",
        visible=False
    )
    
    # Update layout
    fig.update_layout(
        title_font_size=16,
        title_x=0.5,
        width=1000,
        height=800,
        coloraxis_colorbar=dict(
            title_font_size=14,
            tickfont_size=12
        )
    )
    # Show the interactive map
    fig.show()
    
    # Generate data interpretation
    print("=" * 60)
    print("            台灣犯罪人口率數據分析")
    print("      Taiwan Crime Rate Data Analysis")
    print("=" * 60)
    
    # Basic statistics
    mean_rate = df['Crime_Rate'].mean()
    median_rate = df['Crime_Rate'].median()
    std_rate = df['Crime_Rate'].std()
    min_rate = df['Crime_Rate'].min()
    max_rate = df['Crime_Rate'].max()
    
    print(f"\n📊 基本統計 (Basic Statistics):")
    print(f"   平均犯罪率: {mean_rate:.1f} (每十萬人)")
    print(f"   中位數: {median_rate:.1f}")
    print(f"   標準差: {std_rate:.1f}")
    print(f"   最低: {min_rate:.1f}")
    print(f"   最高: {max_rate:.1f}")
    print(f"   範圍: {max_rate - min_rate:.1f}")
    
    # Top 5 highest and lowest
    top_5 = df.nlargest(5, 'Crime_Rate')
    bottom_5 = df.nsmallest(5, 'Crime_Rate')
    
    print(f"\n🔴 犯罪率最高的5個縣市:")
    for idx, row in top_5.iterrows():
        print(f"   {row['County']}: {row['Crime_Rate']:.1f}")
    
    print(f"\n🟢 犯罪率最低的5個縣市:")
    for idx, row in bottom_5.iterrows():
        print(f"   {row['County']}: {row['Crime_Rate']:.1f}")
    
    # Risk categorization
    q1 = df['Crime_Rate'].quantile(0.25)
    q3 = df['Crime_Rate'].quantile(0.75)
    
    high_risk = df[df['Crime_Rate'] > q3]
    medium_risk = df[(df['Crime_Rate'] >= q1) & (df['Crime_Rate'] <= q3)]
    low_risk = df[df['Crime_Rate'] < q1]
    
    print(f"\n🚨 風險等級分類 (基於四分位數):")
    print(f"   高風險 (>{q3:.1f}): {len(high_risk)} 個縣市")
    print(f"   中風險 ({q1:.1f}-{q3:.1f}): {len(medium_risk)} 個縣市")
    print(f"   低風險 (<{q1:.1f}): {len(low_risk)} 個縣市")
    
    print(f"\n💡 關鍵洞察:")
    print(f"   • 地區差異: 最高與最低相差 {max_rate - min_rate:.1f}")
    if std_rate > mean_rate * 0.3:
        print(f"   • 分布特徵: 標準差較大，縣市間差異顯著")
    else:
        print(f"   • 分布特徵: 相對均勻分布")
    
    cv = (std_rate / mean_rate) * 100
    print(f"   • 變異係數: {cv:.1f}% (衡量相對變異程度)")
    
    if len(high_risk) / len(df) > 0.3:
        print(f"   • 治安警示: {len(high_risk)/len(df)*100:.1f}% 縣市屬高風險，需加強關注")
    
    print("=" * 60)

except requests.RequestException:
    print("無法載入地理資料，改用替代方案...")
    
    # Alternative: Create a horizontal bar chart if GeoJSON fails
    fig = px.bar(
        df.sort_values('Crime_Rate'),
        x='Crime_Rate',
        y='County',
        orientation='h',
        color='Crime_Rate',
        color_continuous_scale='Reds',
        title='台灣各縣市犯罪人口率 (Interactive Bar Chart)<br>Taiwan Crime Rate by County/City',
        labels={'Crime_Rate': '犯罪人口率', 'County': '縣市'}
    )
    
    fig.update_layout(
        height=800,
        width=1000,
        title_x=0.5,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    fig.show()
    
    # Still generate the same data interpretation
    print("=" * 60)
    print("            台灣犯罪人口率數據分析")
    print("      Taiwan Crime Rate Data Analysis")  
    print("=" * 60)
    
    # Same analysis code as above...
    mean_rate = df['Crime_Rate'].mean()
    median_rate = df['Crime_Rate'].median()
    std_rate = df['Crime_Rate'].std()
    min_rate = df['Crime_Rate'].min()
    max_rate = df['Crime_Rate'].max()
    
    print(f"\n📊 基本統計 (Basic Statistics):")
    print(f"   平均犯罪率: {mean_rate:.1f} (每十萬人)")
    print(f"   中位數: {median_rate:.1f}")
    print(f"   標準差: {std_rate:.1f}")
    print(f"   最低: {min_rate:.1f}")
    print(f"   最高: {max_rate:.1f}")
    print(f"   範圍: {max_rate - min_rate:.1f}")
    
    top_5 = df.nlargest(5, 'Crime_Rate')
    bottom_5 = df.nsmallest(5, 'Crime_Rate')
    
    print(f"\n🔴 犯罪率最高的5個縣市:")
    for idx, row in top_5.iterrows():
        print(f"   {row['County']}: {row['Crime_Rate']:.1f}")
    
    print(f"\n🟢 犯罪率最低的5個縣市:")
    for idx, row in bottom_5.iterrows():
        print(f"   {row['County']}: {row['Crime_Rate']:.1f}")
    
    q1 = df['Crime_Rate'].quantile(0.25)
    q3 = df['Crime_Rate'].quantile(0.75)
    
    high_risk = df[df['Crime_Rate'] > q3]
    medium_risk = df[(df['Crime_Rate'] >= q1) & (df['Crime_Rate'] <= q3)]
    low_risk = df[df['Crime_Rate'] < q1]
    
    print(f"\n🚨 風險等級分類:")
    print(f"   高風險: {len(high_risk)} 個縣市")
    print(f"   中風險: {len(medium_risk)} 個縣市") 
    print(f"   低風險: {len(low_risk)} 個縣市")
    print("=" * 60)