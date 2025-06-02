import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import rcParams

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 原始資料
data = {
    '總計': {'總計': 244563, '男': 131720, '女': 112843, '兒童': 2047, '少年': 9222, '青年': 30638, '成年': 85297, '壯年': 94629, '老年': 21870},
    '竊盜總數': {'總計': 43064, '男': 26911, '女': 16153, '兒童': 30, '少年': 1115, '青年': 3875, '成年': 15315, '壯年': 18889, '老年': 3611},
    '暴力犯罪總數': {'總計': 529, '男': 281, '女': 248, '兒童': 19, '少年': 39, '青年': 60, '成年': 172, '壯年': 173, '老年': 64},
    '詐欺背信': {'總計': 61440, '男': 29576, '女': 31864, '兒童': 12, '少年': 1012, '青年': 10466, '成年': 24405, '壯年': 20038, '老年': 5465},
    '妨害風化': {'總計': 204, '男': 42, '女': 162, '兒童': 6, '少年': 22, '青年': 50, '成年': 75, '壯年': 49, '老年': 1},
    '性交猥褻': {'總計': 5145, '男': 473, '女': 4672, '兒童': 496, '少年': 2037, '青年': 819, '成年': 1198, '壯年': 538, '老年': 49},
    '駕駛過失': {'總計': 28155, '男': 14635, '女': 13520, '兒童': 374, '少年': 668, '青年': 4254, '成年': 8216, '壯年': 10590, '老年': 4052},
    '妨害家庭及婚姻': {'總計': 331, '男': 125, '女': 206, '兒童': 11, '少年': 94, '青年': 1, '成年': 92, '壯年': 130, '老年': 3},
    '妨害公務': {'總計': 1043, '男': 914, '女': 129, '兒童': 0, '少年': 2, '青年': 85, '成年': 681, '壯年': 235, '老年': 9},
    '公共危險': {'總計': 8034, '男': 4385, '女': 3649, '兒童': 108, '少年': 227, '青年': 1371, '成年': 2623, '壯年': 2744, '老年': 942},
    '其他': {'總計': 96618, '男': 54378, '女': 42240, '兒童': 991, '少年': 4006, '青年': 9657, '成年': 32520, '壯年': 41243, '老年': 7674}
}

# 1. 各案類總被害人數橫條圖
def plot_total_victims_by_case():
    cases = list(data.keys())[1:]  # 排除總計
    totals = [data[case]['總計'] for case in cases]
    
    plt.figure(figsize=(12, 8))
    bars = plt.barh(cases, totals, color='steelblue', alpha=0.7)
    plt.xlabel('被害人數')
    plt.title('2023年各案類刑事案件被害人數', fontsize=16, fontweight='bold')
    plt.grid(axis='x', alpha=0.3)
    
    # 在條形上顯示數值
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(width + width*0.01, bar.get_y() + bar.get_height()/2, 
                f'{int(width):,}', ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.show()

# 2. 年齡層分布圓餅圖
def plot_age_distribution():
    age_groups = ['兒童(0-11歲)', '少年(12-17歲)', '青年(18-23歲)', 
                  '成年(24-39歲)', '壯年(40-64歲)', '老年(65歲以上)']
    age_values = [data['總計']['兒童'], data['總計']['少年'], data['總計']['青年'],
                  data['總計']['成年'], data['總計']['壯年'], data['總計']['老年']]
    
    plt.figure(figsize=(10, 8))
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc', '#c2c2f0']
    wedges, texts, autotexts = plt.pie(age_values, labels=age_groups, colors=colors, 
                                       autopct='%1.1f%%', startangle=90)
    
    plt.title('2023年刑事案件被害者年齡層分布', fontsize=16, fontweight='bold')
    
    # 添加圖例
    plt.legend(wedges, [f'{label}: {value:,}人' for label, value in zip(age_groups, age_values)],
               title="年齡層統計", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    
    plt.tight_layout()
    plt.show()

# 3. 性別比例分析圖
def plot_gender_analysis():
    cases = list(data.keys())[1:]  # 排除總計
    male_counts = [data[case]['男'] for case in cases]
    female_counts = [data[case]['女'] for case in cases]
    
    x = np.arange(len(cases))
    width = 0.35
    
    plt.figure(figsize=(14, 8))
    bars1 = plt.bar(x - width/2, male_counts, width, label='男性', color='skyblue', alpha=0.8)
    bars2 = plt.bar(x + width/2, female_counts, width, label='女性', color='lightcoral', alpha=0.8)
    
    plt.xlabel('案類')
    plt.ylabel('被害人數')
    plt.title('2023年各案類刑事案件被害者性別分布', fontsize=16, fontweight='bold')
    plt.xticks(x, cases, rotation=45, ha='right')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    # 在條形上顯示數值
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 1000:
                plt.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                        f'{int(height):,}', ha='center', va='bottom', fontsize=8)
            elif height > 0:
                plt.text(bar.get_x() + bar.get_width()/2., height + height*0.05,
                        f'{int(height)}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.show()

# 4. 各案類按年齡層分布堆疊圖
def plot_age_stacked_by_case():
    cases = ['竊盜總數', '詐欺背信', '駕駛過失', '公共危險', '其他']  # 選擇主要案類
    age_groups = ['兒童', '少年', '青年', '成年', '壯年', '老年']
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc', '#c2c2f0']
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    bottom = np.zeros(len(cases))
    
    for i, age in enumerate(age_groups):
        values = [data[case][age] for case in cases]
        ax.bar(cases, values, bottom=bottom, label=age, color=colors[i], alpha=0.8)
        bottom += values
    
    ax.set_ylabel('被害人數')
    ax.set_title('主要案類按年齡層分布堆疊圖', fontsize=16, fontweight='bold')
    ax.legend(title='年齡層')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

# 5. 主要案類比較雷達圖
def plot_radar_chart():
    from math import pi
    
    # 選擇主要案類進行比較
    selected_cases = ['竊盜總數', '詐欺背信', '駕駛過失', '性交猥褻', '公共危險']
    age_groups = ['兒童', '少年', '青年', '成年', '壯年', '老年']
    
    # 計算每個案類在各年齡層的比例
    fig, axes = plt.subplots(2, 3, figsize=(18, 12), subplot_kw=dict(projection='polar'))
    axes = axes.flatten()
    
    angles = [n / float(len(age_groups)) * 2 * pi for n in range(len(age_groups))]
    angles += angles[:1]  # 完成圓形
    
    for i, case in enumerate(selected_cases):
        values = [data[case][age] for age in age_groups]
        total = sum(values)
        proportions = [v/total*100 if total > 0 else 0 for v in values]
        proportions += proportions[:1]  # 完成圓形
        
        ax = axes[i]
        ax.plot(angles, proportions, 'o-', linewidth=2, label=case)
        ax.fill(angles, proportions, alpha=0.25)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(age_groups)
        ax.set_title(f'{case}\n年齡層分布比例', fontsize=12, fontweight='bold')
        ax.grid(True)
        ax.set_ylim(0, max(proportions[:-1]) * 1.1 if proportions[:-1] else 1)
    
    # 隱藏第6個子圖
    axes[5].set_visible(False)
    
    plt.tight_layout()
    plt.show()

# 6. 特殊案類分析 - 性犯罪年齡分布
def plot_sex_crime_analysis():
    sex_crimes = ['妨害風化', '性交猥褻']
    age_groups = ['兒童', '少年', '青年', '成年', '壯年', '老年']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    for i, crime in enumerate(sex_crimes):
        values = [data[crime][age] for age in age_groups]
        ax = ax1 if i == 0 else ax2
        
        bars = ax.bar(age_groups, values, color='darkred', alpha=0.7)
        ax.set_title(f'{crime} - 年齡層分布', fontsize=14, fontweight='bold')
        ax.set_ylabel('被害人數')
        ax.tick_params(axis='x', rotation=45)
        
        # 在條形上顯示數值
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + height*0.05,
                       f'{int(height)}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.show()

# 執行所有圖表生成
if __name__ == "__main__":
    print("生成圖表1: 各案類總被害人數橫條圖")
    plot_total_victims_by_case()
    
    print("生成圖表2: 年齡層分布圓餅圖")
    plot_age_distribution()
    
    print("生成圖表3: 性別比例分析圖")
    plot_gender_analysis()
    
    print("生成圖表4: 各案類按年齡層分布堆疊圖")
    plot_age_stacked_by_case()
    
    print("生成圖表5: 主要案類比較雷達圖")
    plot_radar_chart()
    
    print("生成圖表6: 性犯罪案類特殊分析")
    plot_sex_crime_analysis()
    
    print("所有圖表生成完成！")