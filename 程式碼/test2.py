import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import font_manager
import warnings
warnings.filterwarnings('ignore')

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 建立資料
data = {
    '縣市': ['宜蘭縣', '新竹縣', '苗栗縣', '彰化縣', '南投縣', '雲林縣', '嘉義縣', '屏東縣', 
             '臺東縣', '花蓮縣', '澎湖縣', '基隆市', '新竹市', '嘉義市', '金門縣', '連江縣',
             '高雄市', '臺南市', '臺中市', '桃園市', '臺北市', '新北市'],
    '總計_發生數': [7055, 6536, 7707, 15108, 6736, 8335, 6247, 9532, 3404, 5037, 1713, 6099, 5360, 4041, 1088, 166, 21457, 27520, 22081, 21024, 38433, 40967],
    '總計_破獲數': [6777, 5877, 6924, 15145, 6550, 7811, 6318, 8813, 3277, 4691, 1405, 5311, 5233, 3836, 881, 115, 21670, 25943, 21941, 21083, 39335, 39296],
    '總計_嫌疑犯': [8181, 6139, 7316, 18323, 8457, 8821, 8085, 9648, 3387, 4123, 1612, 6322, 5924, 4911, 1391, 175, 24131, 29484, 28099, 20958, 44648, 35707],
    '竊盜_發生數': [935, 857, 1302, 2340, 918, 1243, 875, 904, 503, 790, 150, 918, 879, 699, 104, 16, 3393, 3819, 3493, 2831, 4617, 6031],
    '傷害_發生數': [347, 250, 330, 818, 392, 334, 317, 555, 201, 345, 101, 438, 351, 215, 55, 8, 969, 1191, 1157, 960, 2513, 2291],
    '詐欺背信_發生數': [1166, 1227, 1291, 1929, 1240, 1671, 798, 638, 529, 723, 474, 818, 584, 893, 363, 87, 2569, 5494, 2439, 1983, 4498, 7366],
    '妨害自由_發生數': [357, 329, 324, 822, 395, 408, 331, 614, 152, 335, 80, 460, 343, 156, 40, 6, 911, 1475, 1401, 994, 2323, 2657],
    '駕駛過失_發生數': [867, 545, 580, 1548, 463, 664, 552, 934, 275, 172, 101, 280, 586, 2, 109, 6, 2132, 3102, 782, 1599, 3890, 3331],
    '妨害性自主罪_發生數': [91, 129, 149, 252, 124, 134, 85, 229, 114, 175, 22, 118, 140, 60, 22, 6, 398, 383, 707, 604, 621, 765],
    '違反毒品危害防制條例_發生數': [665, 1112, 1220, 1509, 753, 1077, 830, 1729, 350, 681, 108, 898, 458, 690, 49, 3, 3054, 2646, 3378, 5343, 3316, 6087],
    '公共危險_發生數': [1456, 972, 1318, 2249, 1047, 1405, 1101, 1892, 742, 735, 275, 457, 897, 585, 91, 7, 4452, 4726, 3923, 3274, 4263, 3174]
}

df = pd.DataFrame(data)

# 1. 各縣市總案件發生數比較圖
plt.figure(figsize=(15, 8))
bars = plt.bar(df['縣市'], df['總計_發生數'], color='steelblue', alpha=0.8)
plt.title('各縣市刑事案件總發生數比較', fontsize=16, fontweight='bold')
plt.xlabel('縣市', fontsize=12)
plt.ylabel('案件發生數', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)

# 在柱狀圖上顯示數值
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 100,
             f'{int(height):,}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# 2. 發生數 vs 破獲數 vs 嫌疑犯人數比較圖
fig, ax = plt.subplots(figsize=(16, 10))
x = np.arange(len(df['縣市']))
width = 0.25

bars1 = ax.bar(x - width, df['總計_發生數'], width, label='發生數', color='lightcoral', alpha=0.8)
bars2 = ax.bar(x, df['總計_破獲數'], width, label='破獲數', color='lightgreen', alpha=0.8)
bars3 = ax.bar(x + width, df['總計_嫌疑犯'], width, label='嫌疑犯人數', color='lightskyblue', alpha=0.8)

ax.set_xlabel('縣市', fontsize=12)
ax.set_ylabel('案件數/人數', fontsize=12)
ax.set_title('各縣市刑事案件發生數、破獲數與嫌疑犯人數比較', fontsize=16, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(df['縣市'], rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

# 3. 破獲率分析圖
df['破獲率'] = (df['總計_破獲數'] / df['總計_發生數'] * 100).round(2)

plt.figure(figsize=(15, 8))
colors = ['green' if x >= 95 else 'orange' if x >= 90 else 'red' for x in df['破獲率']]
bars = plt.bar(df['縣市'], df['破獲率'], color=colors, alpha=0.8)
plt.title('各縣市刑事案件破獲率', fontsize=16, fontweight='bold')
plt.xlabel('縣市', fontsize=12)
plt.ylabel('破獲率 (%)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.axhline(y=95, color='green', linestyle='--', alpha=0.7, label='95%基準線')
plt.axhline(y=90, color='orange', linestyle='--', alpha=0.7, label='90%基準線')
plt.grid(axis='y', alpha=0.3)
plt.legend()

# 在柱狀圖上顯示數值
for bar, rate in zip(bars, df['破獲率']):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'{rate}%', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()

# 4. 主要犯罪類型分析 - 竊盜案件
plt.figure(figsize=(15, 8))
bars = plt.bar(df['縣市'], df['竊盜_發生數'], color='crimson', alpha=0.8)
plt.title('各縣市竊盜案件發生數', fontsize=16, fontweight='bold')
plt.xlabel('縣市', fontsize=12)
plt.ylabel('竊盜案件發生數', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)

for bar in bars:
    height = bar.get_height()
    if height > 0:
        plt.text(bar.get_x() + bar.get_width()/2., height + 20,
                 f'{int(height)}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# 5. 詐欺背信案件分析
plt.figure(figsize=(15, 8))
bars = plt.bar(df['縣市'], df['詐欺背信_發生數'], color='darkorange', alpha=0.8)
plt.title('各縣市詐欺背信案件發生數', fontsize=16, fontweight='bold')
plt.xlabel('縣市', fontsize=12)
plt.ylabel('詐欺背信案件發生數', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)

for bar in bars:
    height = bar.get_height()
    if height > 0:
        plt.text(bar.get_x() + bar.get_width()/2., height + 50,
                 f'{int(height)}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# 6. 毒品案件分析
plt.figure(figsize=(15, 8))
bars = plt.bar(df['縣市'], df['違反毒品危害防制條例_發生數'], color='purple', alpha=0.8)
plt.title('各縣市毒品案件發生數', fontsize=16, fontweight='bold')
plt.xlabel('縣市', fontsize=12)
plt.ylabel('毒品案件發生數', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)

for bar in bars:
    height = bar.get_height()
    if height > 0:
        plt.text(bar.get_x() + bar.get_width()/2., height + 30,
                 f'{int(height)}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# 7. 駕駛過失案件分析
plt.figure(figsize=(15, 8))
bars = plt.bar(df['縣市'], df['駕駛過失_發生數'], color='teal', alpha=0.8)
plt.title('各縣市駕駛過失案件發生數', fontsize=16, fontweight='bold')
plt.xlabel('縣市', fontsize=12)
plt.ylabel('駕駛過失案件發生數', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)

for bar in bars:
    height = bar.get_height()
    if height > 0:
        plt.text(bar.get_x() + bar.get_width()/2., height + 20,
                 f'{int(height)}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# 8. 傷害案件分析
plt.figure(figsize=(15, 8))
bars = plt.bar(df['縣市'], df['傷害_發生數'], color='indianred', alpha=0.8)
plt.title('各縣市傷害案件發生數', fontsize=16, fontweight='bold')
plt.xlabel('縣市', fontsize=12)
plt.ylabel('傷害案件發生數', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)

for bar in bars:
    height = bar.get_height()
    if height > 0:
        plt.text(bar.get_x() + bar.get_width()/2., height + 10,
                 f'{int(height)}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# 9. 妨害性自主罪案件分析
plt.figure(figsize=(15, 8))
bars = plt.bar(df['縣市'], df['妨害性自主罪_發生數'], color='darkred', alpha=0.8)
plt.title('各縣市妨害性自主罪案件發生數', fontsize=16, fontweight='bold')
plt.xlabel('縣市', fontsize=12)
plt.ylabel('妨害性自主罪案件發生數', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)

for bar in bars:
    height = bar.get_height()
    if height > 0:
        plt.text(bar.get_x() + bar.get_width()/2., height + 5,
                 f'{int(height)}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# 10. 公共危險案件分析
plt.figure(figsize=(15, 8))
bars = plt.bar(df['縣市'], df['公共危險_發生數'], color='olive', alpha=0.8)
plt.title('各縣市公共危險案件發生數', fontsize=16, fontweight='bold')
plt.xlabel('縣市', fontsize=12)
plt.ylabel('公共危險案件發生數', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)

for bar in bars:
    height = bar.get_height()
    if height > 0:
        plt.text(bar.get_x() + bar.get_width()/2., height + 30,
                 f'{int(height)}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# 11. 主要犯罪類型比較雷達圖 (以台北市為例)
categories = ['竊盜', '傷害', '詐欺背信', '妨害自由', '駕駛過失', '妨害性自主罪', '毒品', '公共危險']
taipei_data = [4617, 2513, 4498, 2323, 3890, 621, 3316, 4263]

# 正規化數據 (0-1之間)
max_val = max(taipei_data)
normalized_data = [x/max_val for x in taipei_data]

angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
normalized_data += normalized_data[:1]  # 閉合圖形
angles += angles[:1]

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
ax.plot(angles, normalized_data, 'o-', linewidth=2, color='blue', alpha=0.8)
ax.fill(angles, normalized_data, alpha=0.25, color='blue')
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories)
ax.set_ylim(0, 1)
ax.set_title('台北市各類犯罪案件分布雷達圖', size=16, fontweight='bold', pad=20)
ax.grid(True)

plt.tight_layout()
plt.show()

# 12. 六都犯罪案件比較圖
six_cities = ['台北市', '新北市', '桃園市', '台中市', '台南市', '高雄市']
six_cities_data = df[df['縣市'].isin(['臺北市', '新北市', '桃園市', '臺中市', '臺南市', '高雄市'])]

crime_types = ['竊盜_發生數', '傷害_發生數', '詐欺背信_發生數', '妨害自由_發生數', '駕駛過失_發生數']
crime_labels = ['竊盜', '傷害', '詐欺背信', '妨害自由', '駕駛過失']

fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

for i, (crime_type, crime_label) in enumerate(zip(crime_types, crime_labels)):
    ax = axes[i]
    bars = ax.bar(six_cities_data['縣市'].str.replace('臺', '台'), six_cities_data[crime_type], 
                  color=plt.cm.Set3(i), alpha=0.8)
    ax.set_title(f'六都{crime_label}案件發生數比較', fontsize=14, fontweight='bold')
    ax.set_ylabel('案件發生數', fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', alpha=0.3)
    
    # 在柱狀圖上顯示數值
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                   f'{int(height)}', ha='center', va='bottom', fontsize=10)

# 移除多餘的子圖
axes[5].axis('off')

plt.tight_layout()
plt.show()

print("所有圖表已生成完成！")
print("\n生成的圖表包括：")
print("1. 各縣市總案件發生數比較圖")
print("2. 發生數 vs 破獲數 vs 嫌疑犯人數比較圖")
print("3. 各縣市破獲率分析圖")
print("4. 竊盜案件分析圖")
print("5. 詐欺背信案件分析圖")
print("6. 毒品案件分析圖")
print("7. 駕駛過失案件分析圖")
print("8. 傷害案件分析圖")
print("9. 妨害性自主罪案件分析圖")
print("10. 公共危險案件分析圖")
print("11. 台北市各類犯罪案件分布雷達圖")
print("12. 六都主要犯罪類型比較圖")