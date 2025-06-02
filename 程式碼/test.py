import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# 設置中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 直接在程式碼中定義數據
suspect_data = [
    # 年份, 男總計, 女總計, 男不識字, 女不識字, 男自修, 女自修, 男國小, 女國小, 男國中, 女國中, 男高中職, 女高中職, 男大專, 女大專, 男研究所, 女研究所, 男其他, 女其他
    [2003, 134394, 24293, 1155, 826, 89, 32, 15717, 3140, 53539, 7472, 50638, 10015, 11892, 2497, 474, 69, 890, 242],
    [2004, 150376, 26599, 978, 769, 91, 32, 15878, 3410, 60168, 8492, 59023, 11084, 13191, 2585, 583, 101, 464, 126],
    [2005, 173286, 34139, 1182, 943, 89, 41, 17379, 4041, 67919, 10763, 70760, 14657, 14752, 3492, 703, 115, 502, 87],
    [2006, 189495, 39698, 1199, 986, 103, 53, 17758, 4393, 72331, 11678, 79123, 17579, 17261, 4583, 836, 160, 884, 266],
    [2007, 221006, 44854, 1188, 951, 116, 64, 19900, 4679, 79318, 12172, 97604, 20973, 20898, 5552, 1121, 233, 861, 230],
    [2008, 225335, 45851, 1151, 927, 101, 38, 18618, 4608, 78708, 11868, 104899, 22345, 19958, 5618, 1087, 242, 813, 205],
    [2009, 214583, 47390, 1126, 962, 116, 53, 17093, 4757, 69237, 11469, 105146, 23318, 19156, 6165, 1180, 299, 1529, 367],
    [2010, 219709, 49631, 1191, 1258, 139, 79, 17715, 5535, 70957, 11971, 107477, 23887, 19218, 6207, 1228, 335, 1784, 359],
    [2011, 212981, 47375, 791, 688, 80, 45, 14364, 4296, 65469, 10833, 110574, 24411, 18547, 6339, 1205, 342, 1951, 421],
    [2012, 213949, 48109, 782, 731, 81, 46, 14026, 4331, 64721, 10788, 111398, 24816, 19908, 6675, 1287, 357, 1746, 365],
    [2013, 209222, 46088, 730, 672, 82, 49, 12857, 3814, 59602, 9785, 113987, 24500, 18974, 6499, 1275, 351, 1715, 418],
    [2014, 214701, 46902, 836, 797, 100, 66, 12925, 4031, 61155, 9881, 115230, 24244, 19829, 6617, 1399, 343, 3227, 923],
    [2015, 221904, 47392, 612, 497, 76, 39, 12477, 3546, 60955, 9768, 120836, 24772, 20319, 7033, 1396, 386, 5233, 1351],
    [2016, 224383, 48434, 513, 480, 71, 49, 10721, 3294, 55487, 9151, 129596, 26668, 20691, 7078, 1448, 416, 5856, 1298],
    [2017, 235388, 51906, 401, 401, 52, 34, 8740, 2879, 55761, 9130, 140427, 30383, 22737, 7326, 1488, 419, 5782, 1334],
    [2018, 236308, 55313, 454, 485, 64, 59, 8579, 3153, 50419, 8994, 144364, 32678, 23107, 7721, 1516, 449, 7805, 1774],
    [2019, 224434, 53230, 409, 315, 85, 61, 7782, 2723, 45544, 8365, 135569, 30432, 24674, 8746, 1533, 471, 8838, 2117],
    [2020, 226302, 55509, 424, 323, 57, 56, 7805, 2797, 43005, 8147, 138587, 31463, 28929, 10802, 1597, 489, 5898, 1432],
    [2021, 210289, 54932, 280, 243, 87, 82, 6388, 2528, 38560, 7951, 131251, 31500, 27249, 11012, 1515, 463, 4959, 1153],
    [2022, 227306, 64585, 232, 289, 69, 74, 6279, 2890, 39887, 8701, 145280, 38201, 28302, 12312, 1530, 530, 5727, 1588]
]

# 創建DataFrame
columns = ['年份', '男總計', '女總計', '男不識字', '女不識字', '男自修', '女自修', 
           '男國小', '女國小', '男國中', '女國中', '男高中職', '女高中職', 
           '男大專', '女大專', '男研究所', '女研究所', '男其他', '女其他']

df = pd.DataFrame(suspect_data, columns=columns)

# 設定學歷類別
education_categories = ['不識字', '自修', '國小', '國中', '高中職', '大專', '研究所', '其他']
colors = ['#8B4513', '#CD853F', '#F4A460', '#87CEEB', '#4682B4', '#32CD32', '#FFD700', '#FF6347']

# 創建輸出目錄
import os
output_dir = 'suspect_education_charts'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 圖表1: 堆疊長條圖 - 男女分開顯示
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

# 準備男性數據
male_data = []
for category in education_categories:
    male_data.append(df[f'男{category}'].values)

# 準備女性數據
female_data = []
for category in education_categories:
    female_data.append(df[f'女{category}'].values)

# 繪製男性堆疊長條圖
x = np.arange(len(df['年份']))
width = 0.8
bottom_male = np.zeros(len(df))

for i, (category, color) in enumerate(zip(education_categories, colors)):
    ax1.bar(x, male_data[i], width, bottom=bottom_male, label=category, color=color, alpha=0.8)
    bottom_male += male_data[i]

ax1.set_title('男性嫌疑人學歷分布 (2003-2022)', fontsize=16, fontweight='bold', pad=20)
ax1.set_xlabel('年份', fontsize=14)
ax1.set_ylabel('人數', fontsize=14)
ax1.set_xticks(x[::2])  # 每隔一年顯示
ax1.set_xticklabels(df['年份'][::2], rotation=45)
ax1.legend(loc='upper left', bbox_to_anchor=(1.02, 1))
ax1.grid(True, alpha=0.3, axis='y')

# 繪製女性堆疊長條圖
bottom_female = np.zeros(len(df))

for i, (category, color) in enumerate(zip(education_categories, colors)):
    ax2.bar(x, female_data[i], width, bottom=bottom_female, label=category, color=color, alpha=0.8)
    bottom_female += female_data[i]

ax2.set_title('女性嫌疑人學歷分布 (2003-2022)', fontsize=16, fontweight='bold', pad=20)
ax2.set_xlabel('年份', fontsize=14)
ax2.set_ylabel('人數', fontsize=14)
ax2.set_xticks(x[::2])
ax2.set_xticklabels(df['年份'][::2], rotation=45)
ax2.legend(loc='upper left', bbox_to_anchor=(1.02, 1))
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{output_dir}/01_男女分開學歷堆疊圖.png', dpi=300, bbox_inches='tight')
plt.close()

# 圖表2: 比例堆疊長條圖 - 男女分開顯示（百分比）
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

# 計算男性比例
male_totals = df['男總計'].values
male_proportions = []
for category in education_categories:
    male_proportions.append(df[f'男{category}'].values / male_totals * 100)

# 計算女性比例
female_totals = df['女總計'].values
female_proportions = []
for category in education_categories:
    female_proportions.append(df[f'女{category}'].values / female_totals * 100)

# 繪製男性比例堆疊圖
bottom_male_prop = np.zeros(len(df))
for i, (category, color) in enumerate(zip(education_categories, colors)):
    ax1.bar(x, male_proportions[i], width, bottom=bottom_male_prop, label=category, color=color, alpha=0.8)
    bottom_male_prop += male_proportions[i]

ax1.set_title('男性嫌疑人學歷比例分布 (2003-2022)', fontsize=16, fontweight='bold', pad=20)
ax1.set_xlabel('年份', fontsize=14)
ax1.set_ylabel('比例 (%)', fontsize=14)
ax1.set_xticks(x[::2])
ax1.set_xticklabels(df['年份'][::2], rotation=45)
ax1.legend(loc='upper left', bbox_to_anchor=(1.02, 1))
ax1.grid(True, alpha=0.3, axis='y')
ax1.set_ylim(0, 100)

# 繪製女性比例堆疊圖
bottom_female_prop = np.zeros(len(df))
for i, (category, color) in enumerate(zip(education_categories, colors)):
    ax2.bar(x, female_proportions[i], width, bottom=bottom_female_prop, label=category, color=color, alpha=0.8)
    bottom_female_prop += female_proportions[i]

ax2.set_title('女性嫌疑人學歷比例分布 (2003-2022)', fontsize=16, fontweight='bold', pad=20)
ax2.set_xlabel('年份', fontsize=14)
ax2.set_ylabel('比例 (%)', fontsize=14)
ax2.set_xticks(x[::2])
ax2.set_xticklabels(df['年份'][::2], rotation=45)
ax2.legend(loc='upper left', bbox_to_anchor=(1.02, 1))
ax2.grid(True, alpha=0.3, axis='y')
ax2.set_ylim(0, 100)

plt.tight_layout()
plt.savefig(f'{output_dir}/02_男女分開學歷比例堆疊圖.png', dpi=300, bbox_inches='tight')
plt.close()

# 圖表3: 男女並排比較圖
fig, ax = plt.subplots(figsize=(24, 12))

# 準備並排數據
x_male = np.arange(len(df['年份'])) - 0.2
x_female = np.arange(len(df['年份'])) + 0.2
width = 0.35

# 男性堆疊
bottom_male = np.zeros(len(df))
for i, (category, color) in enumerate(zip(education_categories, colors)):
    bars_male = ax.bar(x_male, male_data[i], width, bottom=bottom_male, 
                       label=f'男_{category}' if i == 0 else '', color=color, alpha=0.8, edgecolor='white', linewidth=0.5)
    bottom_male += male_data[i]

# 女性堆疊
bottom_female = np.zeros(len(df))
for i, (category, color) in enumerate(zip(education_categories, colors)):
    bars_female = ax.bar(x_female, female_data[i], width, bottom=bottom_female, 
                         label=f'女_{category}' if i == 0 else '', color=color, alpha=0.6, edgecolor='white', linewidth=0.5)
    bottom_female += female_data[i]

# 創建自定義圖例
import matplotlib.patches as mpatches
legend_elements = []
for category, color in zip(education_categories, colors):
    legend_elements.append(mpatches.Patch(color=color, alpha=0.8, label=category))

# 添加性別區分
legend_elements.append(mpatches.Patch(color='gray', alpha=0.8, label='男性'))
legend_elements.append(mpatches.Patch(color='gray', alpha=0.6, label='女性'))

ax.set_title('嫌疑人性別與學歷分布比較 (2003-2022)', fontsize=18, fontweight='bold', pad=30)
ax.set_xlabel('年份', fontsize=14)
ax.set_ylabel('人數', fontsize=14)
ax.set_xticks(np.arange(len(df['年份'])))
ax.set_xticklabels(df['年份'], rotation=45)
ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=12)
ax.grid(True, alpha=0.3, axis='y')

# 添加註解
ax.text(0.02, 0.98, '深色=男性, 淺色=女性', transform=ax.transAxes, 
        fontsize=12, verticalalignment='top',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig(f'{output_dir}/03_男女並排學歷比較圖.png', dpi=300, bbox_inches='tight')
plt.close()

# 圖表4: 趨勢線圖 - 主要學歷類別
fig, ax = plt.subplots(figsize=(16, 10))

# 選擇主要學歷類別進行趨勢分析
main_categories = ['國中', '高中職', '大專']
line_styles = ['-', '--', '-.']
markers = ['o', 's', '^']

for i, category in enumerate(main_categories):
    # 男性趨勢線
    ax.plot(df['年份'], df[f'男{category}'], 
           color=colors[education_categories.index(category)], 
           linestyle=line_styles[i], marker=markers[i], markersize=8, linewidth=3,
           label=f'男_{category}', alpha=0.8)
    
    # 女性趨勢線
    ax.plot(df['年份'], df[f'女{category}'], 
           color=colors[education_categories.index(category)], 
           linestyle=line_styles[i], marker=markers[i], markersize=8, linewidth=3,
           label=f'女_{category}', alpha=0.6)

ax.set_title('主要學歷類別嫌疑人數趨勢變化', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('年份', fontsize=14)
ax.set_ylabel('人數', fontsize=14)
ax.legend(fontsize=12, loc='upper right')
ax.grid(True, alpha=0.3)
ax.tick_params(axis='x', rotation=45)

# 添加標註
max_year = df.loc[df['男高中職'].idxmax(), '年份']
max_value = df['男高中職'].max()
ax.annotate(f'男性高中職最高點\n{max_year}年: {max_value:,}人', 
            xy=(max_year, max_value), xytext=(max_year+2, max_value+10000),
            arrowprops=dict(arrowstyle='->', color='red', alpha=0.7),
            fontsize=11, ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

plt.tight_layout()
plt.savefig(f'{output_dir}/04_主要學歷趨勢線圖.png', dpi=300, bbox_inches='tight')
plt.close()

# 圖表5: 性別比例變化圖
fig, ax = plt.subplots(figsize=(14, 8))

# 計算每年女性比例
total_suspects = df['男總計'] + df['女總計']
female_ratio = df['女總計'] / total_suspects * 100

# 繪製面積圖
ax.fill_between(df['年份'], 0, female_ratio, alpha=0.6, color='pink', label='女性比例')
ax.fill_between(df['年份'], female_ratio, 100, alpha=0.6, color='lightblue', label='男性比例')

# 添加趨勢線
z = np.polyfit(df['年份'], female_ratio, 1)
p = np.poly1d(z)
ax.plot(df['年份'], p(df['年份']), "r--", alpha=0.8, linewidth=2, label='女性比例趨勢線')

ax.set_title('嫌疑人性別比例變化趨勢 (2003-2022)', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('年份', fontsize=14)
ax.set_ylabel('比例 (%)', fontsize=14)
ax.set_ylim(0, 100)
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)
ax.tick_params(axis='x', rotation=45)

# 添加數值標籤
for i in range(0, len(df), 3):  # 每3年標註一次
    ax.text(df.iloc[i]['年份'], female_ratio.iloc[i] + 1, f'{female_ratio.iloc[i]:.1f}%', 
            ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{output_dir}/05_性別比例變化圖.png', dpi=300, bbox_inches='tight')
plt.close()

print("=== 嫌疑人學歷分析圖表輸出完成 ===")
print(f"所有圖表已保存至 '{output_dir}' 資料夾")
print("輸出的圖表包括：")
print("01_男女分開學歷堆疊圖.png - 男女分開的學歷分布堆疊圖")
print("02_男女分開學歷比例堆疊圖.png - 男女分開的學歷比例分布圖")
print("03_男女並排學歷比較圖.png - 男女並排比較的學歷分布圖")
print("04_主要學歷趨勢線圖.png - 主要學歷類別的趨勢變化")
print("05_性別比例變化圖.png - 嫌疑人性別比例的時間變化")

# 輸出統計摘要
print("\n=== 數據統計摘要 ===")
print(f"資料範圍: {df['年份'].min()}年-{df['年份'].max()}年")
print(f"總年份數: {len(df)}年")

# 計算平均性別比例
avg_female_ratio = (df['女總計'].sum() / (df['男總計'].sum() + df['女總計'].sum())) * 100
print(f"20年平均女性嫌疑人比例: {avg_female_ratio:.2f}%")

# 學歷分布統計（最近5年平均）
recent_years = df.tail(5)
print(f"\n近5年({recent_years['年份'].min()}-{recent_years['年份'].max()})平均學歷分布：")

for category in education_categories:
    male_avg = recent_years[f'男{category}'].mean()
    female_avg = recent_years[f'女{category}'].mean()
    total_avg = male_avg + female_avg
    print(f"{category}: {total_avg:.0f}人 (男:{male_avg:.0f}, 女:{female_avg:.0f})")

# 趨勢分析
print(f"\n=== 趨勢分析 ===")
early_female_ratio = df.head(5)['女總計'].sum() / (df.head(5)['男總計'].sum() + df.head(5)['女總計'].sum()) * 100
recent_female_ratio = df.tail(5)['女總計'].sum() / (df.tail(5)['男總計'].sum() + df.tail(5)['女總計'].sum()) * 100
print(f"女性比例變化: 前5年 {early_female_ratio:.2f}% → 後5年 {recent_female_ratio:.2f}% (變化: {recent_female_ratio-early_female_ratio:+.2f}%)")

# 教育程度變化
early_college = (df.head(5)['男大專'].sum() + df.head(5)['女大專'].sum()) / (df.head(5)['男總計'].sum() + df.head(5)['女總計'].sum()) * 100
recent_college = (df.tail(5)['男大專'].sum() + df.tail(5)['女大專'].sum()) / (df.tail(5)['男總計'].sum() + df.tail(5)['女總計'].sum()) * 100
print(f"大專學歷比例變化: 前5年 {early_college:.2f}% → 後5年 {recent_college:.2f}% (變化: {recent_college-early_college:+.2f}%)")