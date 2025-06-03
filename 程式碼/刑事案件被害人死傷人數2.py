import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import rcParams

# 設定中文字體支持
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 讀取並處理資料
def load_and_process_data():
    # 模擬CSV資料（實際使用時請替換為您的檔案路徑）
    data = {
        '案類別': ['故意殺人', '過失殺人', '強盜', '擄人勒贖', '強制性交', '妨害風化', 
                '違反槍砲彈藥刀械管制條例', '駕駛過失', '傷害', '一般傷害', '重傷害', 
                '毀棄損壞', '妨害自由', '公共危險', '妨害公務', '其他'],
        '總計': [151, 78, 59, 3, 11, 109, 11, 28113, 17834, 17810, 24, 89, 943, 6148, 294, 1761],
        '男': [106, 51, 41, 3, 0, 4, 10, 14613, 10867, 10847, 20, 51, 623, 3147, 264, 1087],
        '女': [45, 27, 18, 0, 11, 105, 1, 13500, 6967, 6963, 4, 38, 320, 3001, 30, 674],
        '死亡_計': [88, 73, 0, 0, 0, 0, 0, 446, 15, 0, 15, 0, 2, 29, 0, 19],
        '死亡_男': [57, 47, 0, 0, 0, 0, 0, 284, 12, 0, 12, 0, 2, 20, 0, 11],
        '死亡_女': [31, 26, 0, 0, 0, 0, 0, 162, 3, 0, 3, 0, 0, 9, 0, 8], 
        '受傷_計': [63, 5, 59, 3, 11, 109, 11, 27667, 17819, 17810, 9, 89, 941, 6119, 294, 1742],
        '受傷_男': [49, 4, 41, 3, 0, 4, 10, 14329, 10855, 10847, 8, 51, 621, 3127, 264, 1076],
        '受傷_女': [14, 1, 18, 0, 11, 105, 1, 13338, 6964, 6963, 1, 38, 320, 2992, 30, 666]
    }
    
    df = pd.DataFrame(data)
    return df

# 數據分析函數
def analyze_crime_data(df):
    print("=" * 60)
    print("         台灣刑事案件被害人統計深度分析報告")
    print("=" * 60)
    
    # 排除重複計算的子類別，創建副本避免警告
    df_filtered = df[~df['案類別'].isin(['一般傷害', '重傷害'])].copy()
    
    # 基本統計
    total_victims = df_filtered['總計'].sum()
    total_deaths = df_filtered['死亡_計'].sum()
    total_injuries = df_filtered['受傷_計'].sum()
    total_male = df_filtered['男'].sum()
    total_female = df_filtered['女'].sum()
    
    print(f"\n📊 基本統計資料：")
    print(f"   • 總受害人數：{total_victims:,} 人")
    print(f"   • 總死亡人數：{total_deaths:,} 人 ({total_deaths/total_victims*100:.2f}%)")
    print(f"   • 總受傷人數：{total_injuries:,} 人 ({total_injuries/total_victims*100:.2f}%)")
    print(f"   • 男性受害者：{total_male:,} 人 ({total_male/total_victims*100:.1f}%)")
    print(f"   • 女性受害者：{total_female:,} 人 ({total_female/total_victims*100:.1f}%)")
    
    # 犯罪類型分析
    print(f"\n🎯 犯罪類型分析：")
    top_5_crimes = df_filtered.nlargest(5, '總計').reset_index(drop=True)
    print(f"   前5大犯罪類型：")
    for i, row in top_5_crimes.iterrows():
        percentage = row['總計'] / total_victims * 100
        print(f"   {i+1}. {row['案類別']}：{row['總計']:,} 人 ({percentage:.1f}%)")
    
    # 駕駛過失分析
    driving_row = df_filtered[df_filtered['案類別'] == '駕駛過失'].iloc[0]
    driving_percentage = driving_row['總計'] / total_victims * 100
    print(f"\n🚗 駕駛過失案件分析：")
    print(f"   • 占總受害人數的 {driving_percentage:.1f}%，是最大宗的刑事案件")
    print(f"   • 死亡人數：{driving_row['死亡_計']} 人，死亡率：{driving_row['死亡_計']/driving_row['總計']*100:.2f}%")
    print(f"   • 男性受害者：{driving_row['男']:,} 人 ({driving_row['男']/driving_row['總計']*100:.1f}%)")
    print(f"   • 女性受害者：{driving_row['女']:,} 人 ({driving_row['女']/driving_row['總計']*100:.1f}%)")
    
    # 死亡率分析
    df_filtered.loc[:, '死亡率'] = (df_filtered['死亡_計'] / df_filtered['總計']) * 100
    high_death_rate = df_filtered[df_filtered['死亡率'] > 0].sort_values('死亡率', ascending=False).reset_index(drop=True)
    
    print(f"\n💀 死亡率分析：")
    print(f"   高死亡率犯罪類型（前5名）：")
    for i, row in high_death_rate.head(5).iterrows():
        print(f"   {i+1}. {row['案類別']}：{row['死亡率']:.1f}% ({row['死亡_計']}/{row['總計']})")
    
    # 性別差異分析
    print(f"\n👥 性別差異分析：")
    
    # 找出男女受害差異最大的犯罪類型
    df_filtered.loc[:, '性別差異'] = abs(df_filtered['男'] - df_filtered['女'])
    df_filtered.loc[:, '男性比例'] = df_filtered['男'] / df_filtered['總計'] * 100
    
    # 篩選有足夠樣本數的犯罪類型進行性別分析（至少10人以上）
    df_gender_analysis = df_filtered[df_filtered['總計'] >= 10].copy()
    
    male_dominated = df_gender_analysis[df_gender_analysis['男性比例'] > 70].sort_values('男性比例', ascending=False)
    female_dominated = df_gender_analysis[df_gender_analysis['男性比例'] < 30].sort_values('男性比例', ascending=True)
    
    if len(male_dominated) > 0:
        print(f"   男性受害者占多數的犯罪類型（樣本數≥10）：")
        for i, row in male_dominated.head(3).iterrows():
            print(f"   • {row['案類別']}：男性 {row['男性比例']:.1f}% ({row['男']}/{row['總計']})")
    
    if len(female_dominated) > 0:
        print(f"   女性受害者占多數的犯罪類型（樣本數≥10）：")
        for i, row in female_dominated.head(3).iterrows():
            print(f"   • {row['案類別']}：女性 {100-row['男性比例']:.1f}% ({row['女']}/{row['總計']})")
    
    # 特殊案例分析（小樣本但有代表性）
    special_cases = df_filtered[df_filtered['總計'] < 10]
    if len(special_cases) > 0:
        print(f"   特殊小樣本案件：")
        for i, row in special_cases.iterrows():
            if row['男性比例'] == 100:
                print(f"   • {row['案類別']}：男性 100.0% ({row['男']}/{row['總計']})")
            elif row['男性比例'] == 0:
                print(f"   • {row['案類別']}：女性 100.0% ({row['女']}/{row['總計']})")
    
    # 暴力犯罪分析
    violent_crimes = ['故意殺人', '強盜', '擄人勒贖', '強制性交', '傷害']
    violent_data = df_filtered[df_filtered['案類別'].isin(violent_crimes)]
    violent_total = violent_data['總計'].sum()
    violent_deaths = violent_data['死亡_計'].sum()
    
    print(f"\n⚔️ 暴力犯罪分析：")
    print(f"   • 暴力犯罪總受害人數：{violent_total:,} 人 ({violent_total/total_victims*100:.1f}%)")
    print(f"   • 暴力犯罪死亡人數：{violent_deaths} 人 ({violent_deaths/violent_total*100:.2f}%)")
    
    # 重要發現和結論
    print(f"\n🔍 重要發現與結論：")
    print(f"   1. 駕駛過失是最大宗的刑事案件，占總受害人數的 {driving_percentage:.1f}%")
    print(f"   2. 整體死亡率為 {total_deaths/total_victims*100:.2f}%，屬於中低水準")
    print(f"   3. 男性受害者比例 ({total_male/total_victims*100:.1f}%) 略高於女性 ({total_female/total_victims*100:.1f}%)")
    
    if len(high_death_rate) > 0:
        highest_death_rate = high_death_rate.iloc[0]
        print(f"   4. {highest_death_rate['案類別']}的死亡率最高 ({highest_death_rate['死亡率']:.1f}%)")
    
    print(f"   5. 交通相關案件（駕駛過失）造成大量傷亡，是公共安全的主要威脅")
    
    # 找出最主要的女性受害犯罪類型
    main_female_crimes = df_filtered[df_filtered['女'] > df_filtered['男']].sort_values('女', ascending=False)
    if len(main_female_crimes) > 0:
        main_female_crime = main_female_crimes.iloc[0]
        print(f"   6. {main_female_crime['案類別']}是女性受害者數量最多的犯罪類型 ({main_female_crime['女']}人)")
    
    # 總結交通安全問題
    traffic_deaths = driving_row['死亡_計']
    traffic_death_rate = traffic_deaths / total_deaths * 100
    print(f"   7. 駕駛過失造成 {traffic_deaths} 人死亡，占總死亡人數的 {traffic_death_rate:.1f}%")
    
    # 建議和對策
    print(f"\n💡 政策建議：")
    print(f"   • 【交通安全】強化駕駛過失防治，包括酒駕防制、安全駕駛教育")
    print(f"   • 【暴力犯罪】針對故意殺人、過失殺人等高死亡率犯罪加強預防")
    print(f"   • 【性別保護】重視性侵害和妨害風化案件的被害人保護")
    print(f"   • 【社會安全】建立完善的犯罪預警和社區安全網絡")
    print(f"   • 【數據監控】持續追蹤各類犯罪趨勢，及時調整防治策略")
    
    print("=" * 60)
    return df_filtered

# 圖表1：各犯罪類型總受害人數橫向條形圖
def plot_total_victims_horizontal(df):
    plt.figure(figsize=(12, 10))
    # 排除子類別，避免重複計算
    df_filtered = df[~df['案類別'].isin(['一般傷害', '重傷害'])]
    
    # 按總計排序
    df_sorted = df_filtered.sort_values('總計', ascending=True)
    
    bars = plt.barh(df_sorted['案類別'], df_sorted['總計'], color='steelblue')
    plt.xlabel('受害人數')
    plt.title('2023年台灣各類刑事案件受害人總數', fontsize=16, fontweight='bold')
    plt.grid(axis='x', alpha=0.3)
    
    # 在條形上顯示數值
    for bar in bars:
        width = bar.get_width()
        plt.text(width + max(df_sorted['總計']) * 0.01, bar.get_y() + bar.get_height()/2, 
                f'{int(width):,}', ha='left', va='center')
    
    plt.tight_layout()
    plt.show()

# 圖表2：男女受害者堆疊條形圖
def plot_gender_stacked_bar(df):
    plt.figure(figsize=(14, 8))
    df_filtered = df[~df['案類別'].isin(['一般傷害', '重傷害'])]
    df_sorted = df_filtered.sort_values('總計', ascending=False)
    
    x = range(len(df_sorted))
    width = 0.8
    
    plt.bar(x, df_sorted['男'], width, label='男性', color='#1f77b4')
    plt.bar(x, df_sorted['女'], width, bottom=df_sorted['男'], label='女性', color='#ff7f0e')
    
    plt.xlabel('犯罪類型')
    plt.ylabel('受害人數')
    plt.title('2023年台灣各類刑事案件受害人性別分布', fontsize=16, fontweight='bold')
    plt.xticks(x, df_sorted['案類別'], rotation=45, ha='right')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

# 圖表3：死傷比例分析
def plot_death_injury_comparison(df):
    plt.figure(figsize=(14, 8))
    df_filtered = df[~df['案類別'].isin(['一般傷害', '重傷害'])]
    # 只顯示有死亡案例的犯罪類型
    df_with_deaths = df_filtered[df_filtered['死亡_計'] > 0]
    
    x = np.arange(len(df_with_deaths))
    width = 0.35
    
    plt.bar(x - width/2, df_with_deaths['死亡_計'], width, label='死亡', color='#d62728')
    plt.bar(x + width/2, df_with_deaths['受傷_計'], width, label='受傷', color='#2ca02c')
    
    plt.xlabel('犯罪類型')
    plt.ylabel('人數')
    plt.title('2023年台灣高致死率犯罪類型死傷比較', fontsize=16, fontweight='bold')
    plt.xticks(x, df_with_deaths['案類別'], rotation=45, ha='right')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

# 圖表4：整體性別分布圓餅圖
def plot_gender_pie_chart(df):
    plt.figure(figsize=(10, 8))
    total_male = df['男'].sum() - df[df['案類別']=='一般傷害']['男'].values[0]  # 避免重複計算
    total_female = df['女'].sum() - df[df['案類別']=='一般傷害']['女'].values[0]
    
    sizes = [total_male, total_female]
    labels = [f'男性\n({total_male:,}人)', f'女性\n({total_female:,}人)']
    colors = ['#1f77b4', '#ff7f0e']
    
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.title('2023年台灣刑事案件受害人性別分布', fontsize=16, fontweight='bold')
    plt.axis('equal')
    plt.show()

# 圖表5：前10大犯罪類型詳細分析
def plot_top_crimes_detailed(df):
    plt.figure(figsize=(16, 10))
    df_filtered = df[~df['案類別'].isin(['一般傷害', '重傷害'])]
    df_top = df_filtered.nlargest(10, '總計')
    
    x = np.arange(len(df_top))
    width = 0.25
    
    plt.bar(x - width, df_top['男'], width, label='男性受害者', color='#1f77b4')
    plt.bar(x, df_top['女'], width, label='女性受害者', color='#ff7f0e')
    plt.bar(x + width, df_top['死亡_計'], width, label='死亡人數', color='#d62728')
    
    plt.xlabel('犯罪類型')
    plt.ylabel('人數')
    plt.title('2023年台灣前10大犯罪類型詳細分析', fontsize=16, fontweight='bold')
    plt.xticks(x, df_top['案類別'], rotation=45, ha='right')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

# 圖表6：死亡率分析
def plot_death_rate_analysis(df):
    plt.figure(figsize=(12, 8))
    df_filtered = df[~df['案類別'].isin(['一般傷害', '重傷害'])]
    df_with_victims = df_filtered[df_filtered['總計'] > 0]
    
    # 計算死亡率
    df_with_victims['死亡率'] = (df_with_victims['死亡_計'] / df_with_victims['總計']) * 100
    df_death_rate = df_with_victims[df_with_victims['死亡率'] > 0].sort_values('死亡率', ascending=True)
    
    bars = plt.barh(df_death_rate['案類別'], df_death_rate['死亡率'], color='darkred')
    plt.xlabel('死亡率 (%)')
    plt.title('2023年台灣各類刑事案件死亡率分析', fontsize=16, fontweight='bold')
    plt.grid(axis='x', alpha=0.3)
    
    # 在條形上顯示數值
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.5, bar.get_y() + bar.get_height()/2, 
                f'{width:.1f}%', ha='left', va='center')
    
    plt.tight_layout()
    plt.show()

# 主函數
def main():
    # 載入數據
    df = load_and_process_data()
    
    # 執行深度分析並輸出結果
    analyzed_df = analyze_crime_data(df)
    
    # 詢問是否要生成圖表
    print("\n是否要生成視覺化圖表？(y/n): ", end="")
    response = input().lower().strip()
    
    if response in ['y', 'yes', '是', 'Y']:
        print("\n正在生成圖表...")
        
        # 生成各種圖表
        plot_total_victims_horizontal(df)
        plot_gender_stacked_bar(df)
        plot_death_injury_comparison(df)
        plot_gender_pie_chart(df)
        plot_top_crimes_detailed(df)
        plot_death_rate_analysis(df)
        
        print("所有圖表已生成完成！")
    else:
        print("分析完成，未生成圖表。")

if __name__ == "__main__":
    main()