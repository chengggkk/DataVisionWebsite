import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Rectangle
import warnings
import matplotlib.font_manager as fm
import os

warnings.filterwarnings('ignore')

# 解決中文顯示問題的多種方法
def setup_chinese_font():
    """設定中文字體的函數"""
    
    # 方法1: 嘗試系統內建字體
    font_list = [
        'Microsoft JhengHei',  # Windows 繁體中文
        'Microsoft YaHei',     # Windows 簡體中文
        'SimHei',              # Windows 黑體
        'Arial Unicode MS',    # Mac/Windows
        'Heiti TC',            # Mac 繁體中文
        'PingFang TC',         # Mac 繁體中文
        'WenQuanYi Micro Hei', # Linux
        'DejaVu Sans'          # Linux 備用
    ]
    
    # 檢查可用字體
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    
    for font in font_list:
        if font in available_fonts:
            plt.rcParams['font.sans-serif'] = [font]
            plt.rcParams['axes.unicode_minus'] = False
            print(f"使用字體: {font}")
            return True
    
    # 方法2: 如果沒有中文字體，使用英文標籤
    print("警告: 沒有找到合適的中文字體，將使用英文標籤")
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    return False

# 設定字體
has_chinese_font = setup_chinese_font()

# 定義雙語標籤對照表
label_mapping = {
    '竊盜': 'Theft',
    '詐欺背信': 'Fraud',
    '違反毒品危害防制條例': 'Drug Violations',
    '駕駛過失': 'Traffic Violations',
    '傷害': 'Assault',
    '妨害自由': 'Obstruction of Freedom',
    '賭博': 'Gambling',
    '侵占': 'Embezzlement',
    '毀棄損壞': 'Vandalism',
    '妨害性自主罪': 'Sexual Assault',
    '妨害風化': 'Public Morals',
    '重利': 'Usury',
    '妨害公務': 'Obstruction of Justice',
    '殺人': 'Homicide',
    '恐嚇取財': 'Extortion',
    '強盜搶奪': 'Robbery',
    '暴力犯罪': 'Violent Crime'
}

def get_display_label(chinese_label):
    """根據是否有中文字體返回適當的標籤"""
    if has_chinese_font:
        return chinese_label
    else:
        return label_mapping.get(chinese_label, chinese_label)

# 讀取和處理數據的函數
def read_and_process_data():
    """讀取並處理犯罪數據"""
    crime_data = {
        '年份': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
        '竊盜_發生數': [66255, 57606, 52025, 47591, 42272, 37016, 35067, 37670],
        '竊盜_破獲數': [55055, 48898, 46022, 43262, 40406, 36597, 34826, 36603],
        '詐欺背信_發生數': [21825, 23994, 23623, 24585, 24642, 24607, 26068, 30876],
        '詐欺背信_破獲數': [18520, 20565, 21667, 22697, 22883, 24122, 25815, 30026],
        '違反毒品危害防制條例_發生數': [49576, 54873, 58515, 55480, 47035, 45489, 38644, 38088],
        '違反毒品危害防制條例_破獲數': [49576, 54873, 58515, 55480, 47035, 45489, 38644, 38088],
        '駕駛過失_發生數': [13431, 13755, 13820, 15099, 16588, 16578, 18695, 21172],
        '駕駛過失_破獲數': [13389, 13648, 13711, 14969, 16426, 16369, 18723, 20479],
        '傷害_發生數': [11141, 11790, 11709, 12256, 13213, 12666, 12717, 13972],
        '傷害_破獲數': [10476, 11118, 11152, 11674, 12856, 12355, 12620, 13435],
        '妨害自由_發生數': [6361, 7136, 7391, 8206, 8990, 9994, 11950, 14438],
        '妨害自由_破獲數': [5816, 6601, 6904, 7704, 8553, 9459, 11809, 13669],
        '賭博_發生數': [6969, 6798, 6447, 4542, 4858, 3175, 2513, 3135],
        '賭博_破獲數': [6969, 6798, 6447, 4542, 4858, 3175, 2513, 3135],
        '侵占_發生數': [5671, 6147, 6439, 7382, 7801, 8160, 8420, 10067],
        '侵占_破獲數': [4056, 4686, 5090, 6079, 6718, 7268, 8008, 9385],
        '毀棄損壞_發生數': [5304, 5335, 5298, 5439, 5403, 5232, 5879, 6791],
        '毀棄損壞_破獲數': [2955, 3410, 3687, 4099, 4483, 4687, 5520, 6177],
        '妨害性自主罪_發生數': [3648, 3642, 3353, 3263, 3384, 4217, 4081, 4520],
        '妨害性自主罪_破獲數': [3637, 3558, 3244, 3215, 3310, 4129, 3929, 4324],
    }
    return pd.DataFrame(crime_data)

# 讀取數據
df = read_and_process_data()

# 計算主要犯罪類型
major_crimes = {}
for col in df.columns:
    if col.endswith('_發生數'):
        crime_name = col.replace('_發生數', '')
        major_crimes[crime_name] = df[col].mean()

top_10_crimes = sorted(major_crimes.items(), key=lambda x: x[1], reverse=True)[:10]

# 1. 主要犯罪類型發生數趨勢圖
plt.figure(figsize=(16, 10))

colors = plt.cm.tab10(np.linspace(0, 1, 10))
for i, (crime, _) in enumerate(top_10_crimes):
    display_label = get_display_label(crime)
    plt.plot(df['年份'], df[f'{crime}_發生數'], 
             marker='o', linewidth=2.5, label=display_label, color=colors[i])

title = '台灣主要犯罪類型發生數趨勢 (2015-2022)' if has_chinese_font else 'Taiwan Major Crime Trends (2015-2022)'
plt.title(title, fontsize=18, fontweight='bold', pad=20)

xlabel = '年份' if has_chinese_font else 'Year'
ylabel = '發生數 (件)' if has_chinese_font else 'Number of Cases'
plt.xlabel(xlabel, fontsize=14)
plt.ylabel(ylabel, fontsize=14)

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
plt.grid(True, alpha=0.3)
plt.xticks(df['年份'])
plt.tight_layout()
plt.show()

# 2. 犯罪類型變化率分析
plt.figure(figsize=(16, 10))

change_rates = {}
for crime, _ in top_10_crimes:
    start_value = df[df['年份'] == 2015][f'{crime}_發生數'].iloc[0]
    end_value = df[df['年份'] == 2022][f'{crime}_發生數'].iloc[0]
    change_rate = ((end_value - start_value) / start_value) * 100
    change_rates[crime] = change_rate

sorted_changes = sorted(change_rates.items(), key=lambda x: x[1])

crimes = [get_display_label(item[0]) for item in sorted_changes]
changes = [item[1] for item in sorted_changes]

colors = ['red' if x > 0 else 'blue' for x in changes]

plt.barh(range(len(crimes)), changes, color=colors, alpha=0.7)
plt.yticks(range(len(crimes)), crimes)

xlabel = '變化率 (%)' if has_chinese_font else 'Change Rate (%)'
title = '各類犯罪發生數變化率 (2015-2022)' if has_chinese_font else 'Crime Rate Changes (2015-2022)'
plt.xlabel(xlabel, fontsize=14)
plt.title(title, fontsize=18, fontweight='bold', pad=20)

plt.axvline(x=0, color='black', linestyle='-', alpha=0.5)
plt.grid(True, alpha=0.3, axis='x')

for i, v in enumerate(changes):
    plt.text(v + (1 if v > 0 else -1), i, f'{v:.1f}%', 
             va='center', ha='left' if v > 0 else 'right')

plt.tight_layout()
plt.show()

# 3. 破獲率比較圖
plt.figure(figsize=(16, 10))

crime_clearance_rates = {}
for crime, _ in top_10_crimes[:5]:  # 只顯示前5名
    if f'{crime}_破獲數' in df.columns:
        clearance_rate = (df[f'{crime}_破獲數'] / df[f'{crime}_發生數'] * 100)
        crime_clearance_rates[crime] = clearance_rate

colors = plt.cm.tab10(np.linspace(0, 1, len(crime_clearance_rates)))
for i, (crime, rates) in enumerate(crime_clearance_rates.items()):
    display_label = get_display_label(crime)
    plt.plot(df['年份'], rates, marker='s', linewidth=2.5, 
             label=display_label, color=colors[i])

title = '台灣主要犯罪類型破獲率趨勢 (2015-2022)' if has_chinese_font else 'Taiwan Crime Clearance Rate Trends (2015-2022)'
plt.title(title, fontsize=18, fontweight='bold', pad=20)

xlabel = '年份' if has_chinese_font else 'Year'
ylabel = '破獲率 (%)' if has_chinese_font else 'Clearance Rate (%)'
plt.xlabel(xlabel, fontsize=14)
plt.ylabel(ylabel, fontsize=14)

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
plt.grid(True, alpha=0.3)
plt.xticks(df['年份'])
plt.ylim(0, 120)
plt.tight_layout()
plt.show()

# 檢查字體函數
def check_available_fonts():
    """檢查系統可用的中文字體"""
    print("系統可用的字體:")
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    chinese_fonts = [font for font in available_fonts if any(keyword in font for keyword in 
                    ['JhengHei', 'YaHei', 'SimHei', 'Heiti', 'PingFang', 'WenQuanYi'])]
    
    if chinese_fonts:
        print("找到的中文字體:")
        for font in chinese_fonts[:10]:  # 只顯示前10個
            print(f"  - {font}")
    else:
        print("沒有找到中文字體")
    
    return chinese_fonts

# 執行字體檢查
print("="*50)
print("字體檢查結果:")
check_available_fonts()
print("="*50)