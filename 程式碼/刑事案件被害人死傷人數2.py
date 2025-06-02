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
    df = load_and_process_data()
    
    print("=== 台灣刑事案件被害人統計分析 ===")
    print(f"資料概況：")
    print(f"- 犯罪類型數：{len(df)}種")
    print(f"- 總受害人數：{df['總計'].sum() - df[df['案類別']=='一般傷害']['總計'].values[0]:,}人")
    print(f"- 總死亡人數：{df['死亡_計'].sum():,}人")
    print()
    
    print("正在生成圖表...")
    
    # 生成各種圖表
    plot_total_victims_horizontal(df)
    plot_gender_stacked_bar(df)
    plot_death_injury_comparison(df)
    plot_gender_pie_chart(df)
    plot_top_crimes_detailed(df)
    plot_death_rate_analysis(df)
    
    print("所有圖表已生成完成！")

if __name__ == "__main__":
    main()