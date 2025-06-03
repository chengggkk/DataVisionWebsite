import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
import io

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 讀取CSV數據
def read_csv_data():
    # 模擬CSV數據
    data = {
        '年別': ['民國 92年 2003', '民國 93年 2004', '民國 94年 2005', '民國 95年 2006', '民國 96年 2007', 
                '民國 97年 2008', '民國 98年 2009', '民國 99年 2010', '民國100年 2011', '民國101年 2012',
                '民國102年 2013', '民國103年 2014', '民國104年 2015', '民國105年 2016', '民國106年 2017',
                '民國107年 2018', '民國108年 2019', '民國109年 2020', '民國110年 2021', '民國111年 2022'],
        '總計': [158687, 176975, 207425, 229193, 265860, 271186, 261973, 269340, 260356, 262058,
                255310, 261603, 269296, 272817, 287294, 291621, 277664, 281811, 265221, 291891],
        '不識字': [1981, 1747, 2125, 2185, 2139, 2078, 2088, 2449, 1479, 1513,
                  1402, 1633, 1109, 993, 802, 939, 724, 747, 523, 521],
        '自修': [121, 123, 130, 156, 180, 139, 169, 218, 125, 127,
                131, 166, 115, 120, 86, 123, 146, 113, 169, 143],
        '國小': [18857, 19288, 21420, 22151, 24579, 23226, 21850, 23250, 18660, 18357,
                16671, 16956, 16023, 14015, 11619, 11732, 10505, 10602, 8916, 9169],
        '國中': [61011, 68660, 78682, 84009, 91490, 90576, 80706, 82928, 76302, 75509,
                69387, 71036, 70723, 64638, 64891, 59413, 53909, 51152, 46511, 48588],
        '高中職': [60653, 70107, 85417, 96702, 118577, 127244, 128464, 131364, 134985, 136214,
                  138487, 139474, 145608, 156264, 170810, 177042, 166001, 170050, 162751, 183481],
        '大專': [14389, 15776, 18244, 21844, 26450, 25576, 25321, 25425, 24886, 26583,
                25473, 26446, 27352, 27769, 30063, 30828, 33420, 39731, 38261, 40614],
        '研究所': [543, 684, 818, 996, 1354, 1329, 1479, 1563, 1547, 1644,
                  1626, 1742, 1782, 1864, 1907, 1965, 2004, 2086, 1978, 2060],
        '其他': [1132, 590, 589, 1150, 1091, 1018, 1896, 2143, 2372, 2111,
                2133, 4150, 6584, 7154, 7116, 9579, 10955, 7330, 6112, 7315]
    }
    
    df = pd.DataFrame(data)
    # 提取年份
    df['年份'] = df['年別'].str.extract(r'(\d{4})').astype(int)
    return df

# 讀取數據
df = read_csv_data()

# 數據分析和結論輸出
def analyze_data(df):
    print("=" * 60)
    print("台灣刑事案件嫌疑犯教育程度數據分析報告 (2003-2022)")
    print("=" * 60)
    
    # 基本統計
    print("\n【基本統計】")
    print(f"資料期間：{df['年份'].min()}年 - {df['年份'].max()}年")
    print(f"總案件數範圍：{df['總計'].min():,} - {df['總計'].max():,} 人")
    print(f"平均年度案件數：{df['總計'].mean():.0f} 人")
    
    # 趨勢分析
    print("\n【整體趨勢分析】")
    start_total = df['總計'].iloc[0]
    end_total = df['總計'].iloc[-1]
    change_rate = ((end_total - start_total) / start_total) * 100
    print(f"2003年總數：{start_total:,} 人")
    print(f"2022年總數：{end_total:,} 人")
    print(f"20年變化率：{change_rate:+.1f}%")
    
    # 各教育程度變化分析
    print("\n【各教育程度變化分析】")
    categories = ['不識字', '自修', '國小', '國中', '高中職', '大專', '研究所', '其他']
    
    for category in categories:
        start_val = df[category].iloc[0]
        end_val = df[category].iloc[-1]
        if start_val > 0:
            change_rate = ((end_val - start_val) / start_val) * 100
            print(f"{category:>4}：{start_val:>6,} → {end_val:>6,} 人 ({change_rate:+6.1f}%)")
        else:
            print(f"{category:>4}：{start_val:>6,} → {end_val:>6,} 人 (無法計算變化率)")
    
    # 占比分析
    print("\n【2022年教育程度占比】")
    total_2022 = df['總計'].iloc[-1]
    for category in categories:
        val_2022 = df[category].iloc[-1]
        percentage = (val_2022 / total_2022) * 100
        print(f"{category:>4}：{val_2022:>6,} 人 ({percentage:>5.1f}%)")
    
    # 關鍵發現
    print("\n【關鍵發現】")
    
    # 找出增長最多和減少最多的教育程度
    max_increase = 0
    max_increase_cat = ""
    max_decrease = 0
    max_decrease_cat = ""
    
    for category in categories:
        start_val = df[category].iloc[0]
        end_val = df[category].iloc[-1]
        change = end_val - start_val
        
        if change > max_increase:
            max_increase = change
            max_increase_cat = category
        elif change < max_decrease:
            max_decrease = change
            max_decrease_cat = category
    
    print(f"• 增長最多：{max_increase_cat} (+{max_increase:,} 人)")
    print(f"• 減少最多：{max_decrease_cat} ({max_decrease:,} 人)")
    
    # 高等教育趨勢
    higher_ed_2003 = df['大專'].iloc[0] + df['研究所'].iloc[0]
    higher_ed_2022 = df['大專'].iloc[-1] + df['研究所'].iloc[-1]
    higher_ed_change = ((higher_ed_2022 - higher_ed_2003) / higher_ed_2003) * 100
    print(f"• 高等教育(大專+研究所)：{higher_ed_2003:,} → {higher_ed_2022:,} 人 ({higher_ed_change:+.1f}%)")
    
    # 基礎教育趨勢
    basic_ed_2003 = df['國小'].iloc[0] + df['國中'].iloc[0]
    basic_ed_2022 = df['國小'].iloc[-1] + df['國中'].iloc[-1]
    basic_ed_change = ((basic_ed_2022 - basic_ed_2003) / basic_ed_2003) * 100
    print(f"• 基礎教育(國小+國中)：{basic_ed_2003:,} → {basic_ed_2022:,} 人 ({basic_ed_change:+.1f}%)")
    
    print("\n【結論】")
    print("1. 高中職學歷的嫌疑犯人數大幅增加，成為主要群體")
    print("2. 基礎教育(國小+國中)學歷的嫌疑犯人數明顯下降")
    print("3. 高等教育學歷的嫌疑犯人數持續增長，值得關注")
    print("4. 整體犯罪案件數在20年間呈現上升趨勢")
    print("5. 教育程度結構反映了台灣社會教育水平的提升")
    print("=" * 60)

# 執行數據分析
analyze_data(df)

# 圖表1：堆疊面積圖 - 台灣刑事案件嫌疑犯教育程度變化 (2003-2022)
fig1, ax1 = plt.subplots(figsize=(12, 8))

# 準備堆疊數據
categories = ['不識字', '自修', '國小', '國中', '高中職', '大專', '研究所', '其他']
colors = ['#FFB6C1', '#FFA07A', '#98FB98', '#87CEEB', '#DDA0DD', '#F0E68C', '#D3D3D3', '#FFFF99']

# 創建堆疊面積圖
x = df['年份']
y_stack = np.zeros(len(df))

for i, category in enumerate(categories):
    ax1.fill_between(x, y_stack, y_stack + df[category], 
                     alpha=0.7, color=colors[i], label=category)
    y_stack += df[category]

ax1.set_title('台灣刑事案件嫌疑犯教育程度變化 (2003-2022)', fontsize=16, fontweight='bold')
ax1.set_xlabel('年份', fontsize=12)
ax1.set_ylabel('嫌疑犯人數', fontsize=12)
ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax1.grid(True, alpha=0.3)
ax1.set_xlim(2003, 2022)

# 設定y軸格式
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/1000)}萬' if x >= 10000 else f'{int(x)}'))

plt.tight_layout()
plt.show()

# 圖表2：線圖 - 主要學歷類別嫌疑犯人數趨勢變化
fig2, ax2 = plt.subplots(figsize=(12, 8))

# 選擇主要學歷類別
main_categories = ['國中', '高中職', '大專', '國小', '研究所', '其他']
line_colors = ['#87CEEB', '#4169E1', '#32CD32', '#FFB347', '#FF69B4', '#9370DB']
line_styles = ['-', '-', '-', '--', '-.', ':']
markers = ['o', 's', '^', 'v', 'd', '*']

for i, category in enumerate(main_categories):
    ax2.plot(df['年份'], df[category], 
             color=line_colors[i], 
             linestyle=line_styles[i],
             marker=markers[i],
             markersize=6,
             linewidth=2,
             label=category,
             alpha=0.8)

ax2.set_title('主要學歷類別嫌疑犯人數趨勢變化', fontsize=16, fontweight='bold')
ax2.set_xlabel('年份', fontsize=12)
ax2.set_ylabel('人數', fontsize=12)
ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax2.grid(True, alpha=0.3)
ax2.set_xlim(2003, 2022)

# 設定y軸格式
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/1000)}千' if x >= 1000 else f'{int(x)}'))

# 添加數據標註框
textstr = '資料來源：內政部警政署\n2022年：約29.1萬人'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax2.text(0.98, 0.98, textstr, transform=ax2.transAxes, fontsize=10,
         verticalalignment='top', horizontalalignment='right', bbox=props)

plt.tight_layout()
plt.show()

print("\n" + "=" * 40)
print("圖表生成完成")
print("=" * 40)
print("✓ 圖表1：堆疊面積圖 - 顯示各教育程度嫌疑犯人數的整體變化趨勢")
print("✓ 圖表2：線圖 - 顯示主要學歷類別的個別趨勢變化")
print("✓ 數據分析報告已輸出")