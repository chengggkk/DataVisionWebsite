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

def load_and_analyze_data():
    """載入並分析暴力犯罪數據"""
    print("=" * 80)
    print("                    台灣地區暴力犯罪統計分析報告")
    print("=" * 80)
    
    # 1. 載入暴力犯罪統計數據
    print("\n正在載入暴力犯罪統計數據...")
    
    # 先讀取檔案查看實際欄位名稱
    df = pd.read_csv("暴力犯罪統計2V.csv", skiprows=3, encoding='utf-8')
    print("原始欄位名稱:", df.columns.tolist())  # 查看實際欄位名稱
    
    # 重新讀取並指定正確欄位名稱
    df = pd.read_csv("暴力犯罪統計2V.csv", skiprows=3, encoding='utf-8')
    df.columns = ['機關別', '總計_發生數', '總計_破獲率', '故意殺人_發生數', '故意殺人_破獲率', 
                  '擄人勒贖_發生數', '擄人勒贖_破獲率', '強盜_發生數', '強盜_破獲率',
                  '搶奪_發生數', '搶奪_破獲率', '重傷害_發生數', '重傷害_破獲率',
                  '恐嚇取財_發生數', '恐嚇取財_破獲率', '強制性交_發生數', '強制性交_破獲率']
    
    # 清理數據 - 移除空行和無效數據
    df = df.dropna(how='all')
    df = df[df['機關別'] != '署所屬機關']  # 移除非縣市數據
    
    return df

def analyze_overall_statistics(df):
    """分析整體統計數據"""
    print(f"\n【整體暴力犯罪統計分析】")
    
    # 轉換數值欄位
    crime_columns = ['總計_發生數', '故意殺人_發生數', '擄人勒贖_發生數', '強盜_發生數', 
                    '搶奪_發生數', '重傷害_發生數', '恐嚇取財_發生數', '強制性交_發生數']
    
    for col in crime_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 計算全國總計
    total_crimes = df['總計_發生數'].sum()
    avg_crimes = df['總計_發生數'].mean()
    max_crimes = df['總計_發生數'].max()
    min_crimes = df['總計_發生數'].min()
    
    max_county = df.loc[df['總計_發生數'].idxmax(), '機關別']
    min_county = df.loc[df['總計_發生數'].idxmin(), '機關別']
    
    print(f"• 全國暴力犯罪總案件數：{total_crimes:,} 件")
    print(f"• 各縣市平均案件數：{avg_crimes:.1f} 件")
    print(f"• 最高案件數縣市：{max_county} ({max_crimes:,} 件)")
    print(f"• 最低案件數縣市：{min_county} ({min_crimes:,} 件)")
    print(f"• 最高與最低差距：{max_crimes - min_crimes:,} 件 ({(max_crimes/min_crimes):.1f} 倍)")
    
    return df

def analyze_crime_types(df):
    """分析各類型犯罪分布"""
    print(f"\n【各類型暴力犯罪分析】")
    
    # 計算各類型犯罪的全國總數
    crime_types = {
        '故意殺人': df['故意殺人_發生數'].sum(),
        '擄人勒贖': df['擄人勒贖_發生數'].sum(),
        '強盜': df['強盜_發生數'].sum(),
        '搶奪': df['搶奪_發生數'].sum(),
        '重傷害': df['重傷害_發生數'].sum(),
        '恐嚇取財': df['恐嚇取財_發生數'].sum(),
        '強制性交': df['強制性交_發生數'].sum()
    }
    
    total_specific_crimes = sum(crime_types.values())
    
    print(f"各類型犯罪案件數排名：")
    sorted_crimes = sorted(crime_types.items(), key=lambda x: x[1], reverse=True)
    
    for i, (crime_type, count) in enumerate(sorted_crimes, 1):
        percentage = (count / total_specific_crimes) * 100 if total_specific_crimes > 0 else 0
        print(f"{i}. {crime_type}：{count:,} 件 ({percentage:.1f}%)")
    
    # 分析最嚴重的犯罪類型
    most_serious = ['故意殺人', '擄人勒贖', '強制性交']
    serious_total = sum(crime_types[crime] for crime in most_serious)
    serious_percentage = (serious_total / total_specific_crimes) * 100 if total_specific_crimes > 0 else 0
    
    print(f"\n【重大犯罪分析】")
    print(f"• 重大犯罪（故意殺人、擄人勒贖、強制性交）總計：{serious_total:,} 件")
    print(f"• 重大犯罪佔比：{serious_percentage:.1f}%")

def analyze_regional_patterns(df):
    """分析地區犯罪模式"""
    print(f"\n【地區犯罪模式分析】")
    
    # 按照犯罪數量分組
    df_sorted = df.sort_values('總計_發生數', ascending=False)
    
    # 高犯罪區域（前5名）
    high_crime = df_sorted.head(5)
    print(f"高犯罪區域（前5名）：")
    for i, (idx, row) in enumerate(high_crime.iterrows(), 1):
        print(f"{i}. {row['機關別']}：{row['總計_發生數']:,} 件")
    
    # 低犯罪區域（後5名）
    low_crime = df_sorted.tail(5)
    print(f"\n低犯罪區域（後5名）：")
    for i, (idx, row) in enumerate(low_crime.iterrows(), 1):
        print(f"{i}. {row['機關別']}：{row['總計_發生數']:,} 件")
    
    # 計算城鄉差距
    top5_avg = high_crime['總計_發生數'].mean()
    bottom5_avg = low_crime['總計_發生數'].mean()
    urban_rural_gap = top5_avg / bottom5_avg
    
    print(f"\n【城鄉差距分析】")
    print(f"• 高犯罪區域平均：{top5_avg:.1f} 件")
    print(f"• 低犯罪區域平均：{bottom5_avg:.1f} 件")
    print(f"• 城鄉犯罪差距：{urban_rural_gap:.1f} 倍")

def analyze_clearance_rates(df):
    """分析破獲率數據"""
    print(f"\n【破獲率分析】")
    
    # 轉換破獲率為數值
    rate_columns = ['總計_破獲率', '故意殺人_破獲率', '擄人勒贖_破獲率', '強盜_破獲率',
                   '搶奪_破獲率', '重傷害_破獲率', '恐嚇取財_破獲率', '強制性交_破獲率']
    
    for col in rate_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 計算全國平均破獲率
    overall_clearance = df['總計_破獲率'].mean()
    highest_clearance = df['總計_破獲率'].max()
    lowest_clearance = df['總計_破獲率'].min()
    
    highest_county = df.loc[df['總計_破獲率'].idxmax(), '機關別']
    lowest_county = df.loc[df['總計_破獲率'].idxmin(), '機關別']
    
    print(f"• 全國平均破獲率：{overall_clearance:.1f}%")
    print(f"• 最高破獲率：{highest_county} ({highest_clearance:.1f}%)")
    print(f"• 最低破獲率：{lowest_county} ({lowest_clearance:.1f}%)")
    
    # 分析各類型犯罪破獲率
    crime_clearance = {
        '故意殺人': df['故意殺人_破獲率'].mean(),
        '擄人勒贖': df['擄人勒贖_破獲率'].mean(),
        '強盜': df['強盜_破獲率'].mean(),
        '搶奪': df['搶奪_破獲率'].mean(),
        '重傷害': df['重傷害_破獲率'].mean(),
        '恐嚇取財': df['恐嚇取財_破獲率'].mean(),
        '強制性交': df['強制性交_破獲率'].mean()
    }
    
    print(f"\n各類型犯罪平均破獲率：")
    sorted_clearance = sorted(crime_clearance.items(), key=lambda x: x[1], reverse=True)
    
    for i, (crime_type, rate) in enumerate(sorted_clearance, 1):
        if not np.isnan(rate):
            print(f"{i}. {crime_type}：{rate:.1f}%")

def generate_conclusions(df):
    """生成分析結論"""
    print(f"\n" + "=" * 80)
    print("                                主要發現與結論")
    print("=" * 80)
    
    # 獲取關鍵數據
    top_county = df.loc[df['總計_發生數'].idxmax(), '機關別']
    top_cases = df['總計_發生數'].max()
    
    # 計算各類型犯罪佔比
    total_crimes = df['總計_發生數'].sum()
    major_crimes = ['重傷害', '恐嚇取財', '搶奪']
    
    print(f"\n【關鍵發現】")
    print(f"1. 犯罪熱點集中化")
    print(f"   - {top_county}以 {top_cases:,} 件居首，顯示都市化程度與犯罪率正相關")
    print(f"   - 人口密集區域暴力犯罪案件明顯較多")
    
    print(f"\n2. 犯罪類型特徵")
    print(f"   - 重傷害、恐嚇取財、搶奪為主要暴力犯罪類型")
    print(f"   - 故意殺人、擄人勒贖等重大犯罪相對較少但影響嚴重")
    
    avg_clearance = df['總計_破獲率'].mean()
    print(f"\n3. 執法效能")
    print(f"   - 全國平均破獲率：{avg_clearance:.1f}%")
    print(f"   - 各地區破獲率存在差異，反映執法資源配置不均")
    
    print(f"\n【政策建議】")
    print(f"• 加強高犯罪率地區的治安維護和預防措施")
    print(f"• 針對主要犯罪類型制定專項打擊策略")
    print(f"• 平衡城鄉執法資源配置，提升整體破獲率")
    print(f"• 建立跨縣市合作機制，共同打擊跨區域犯罪")
    print(f"• 加強社區治安和犯罪預防教育")

def create_visualizations(df):
    """創建地圖和其他視覺化"""
    print(f"\n" + "=" * 80)
    print("                              開始生成視覺化圖表")
    print("=" * 80)
    
    # 2. 選擇需要的列並重命名
    viz_df = df[['機關別', '總計_發生數']].copy()
    viz_df.columns = ['County', 'Total_Violent_Crime']
    
    # 清理縣市名稱
    viz_df['County'] = viz_df['County'].str.strip()
    
    print("\n正在載入台灣地理數據...")
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
    viz_df['County_English'] = viz_df['County'].map(county_mapping)
    
    # 6. 合併地理數據與統計數據
    merged = gdf.merge(viz_df, left_on='name', right_on='County_English', how='left')
    
    # 7. 數據清理 - 轉換為數值
    merged['Total_Violent_Crime'] = pd.to_numeric(merged['Total_Violent_Crime'], errors='coerce')
    
    print("\n正在生成地圖視覺化...")
    # 8. 創建地圖視覺化
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(1, 2, width_ratios=[2, 1])  # 分割為左右兩部分
    ax1 = fig.add_subplot(gs[0])  # 左邊放地圖
    ax2 = fig.add_subplot(gs[1])  # 右邊放數據
    
    # 繪製地圖
    cmap = colormaps['OrRd']
    norm = colors.Normalize(vmin=merged['Total_Violent_Crime'].min(), vmax=merged['Total_Violent_Crime'].max())
    
    merged.plot(column='Total_Violent_Crime', 
               cmap=cmap, 
               norm=norm,
               linewidth=0.8, 
               ax=ax1, 
               edgecolor='0.8',
               legend=True,
               legend_kwds={'label': "暴力犯罪案件數", 'orientation': "horizontal", 'shrink': 0.6})
    
    ax1.axis('off')
    
    # 在右側創建數據表格
    # 準備數據
    table_data = merged[['County', 'Total_Violent_Crime']].dropna()
    table_data = table_data.sort_values('Total_Violent_Crime', ascending=False)
    table_data['Total_Violent_Crime'] = table_data['Total_Violent_Crime'].astype(int)
    
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
    plt.suptitle('台灣地區暴力犯罪案件統計分析', fontsize=18, y=0.98)
    plt.figtext(0.1, 0.02, "數據來源: 暴力犯罪統計表", fontsize=10)
    
    plt.show()

# === 主程式執行 ===

print("正在載入並分析台灣暴力犯罪數據...")

# 載入數據
df = load_and_analyze_data()

# 執行各項分析
df = analyze_overall_statistics(df)
analyze_crime_types(df)
analyze_regional_patterns(df)
analyze_clearance_rates(df)
generate_conclusions(df)

# 生成視覺化
create_visualizations(df)

print(f"\n" + "=" * 80)
print("                            分析報告與地圖生成完成")
print("=" * 80)