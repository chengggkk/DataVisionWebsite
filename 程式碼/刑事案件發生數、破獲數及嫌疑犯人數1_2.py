import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import rcParams

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 手動輸入數據（基於CSV檔案內容）
years = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']
crime_types = ['總計', '竊盜', '贓物', '賭博', '傷害', '詐欺背信', '重利', '妨害自由', '殺人', 
               '駕駛過失', '妨害婚姻及家庭', '妨害風化', '妨害性自主罪', '恐嚇取財', '擄人勒贖',
               '侵占', '偽造文書印文', '違反毒品危害防制條例', '毀棄損壞', '妨害公務', '強盜搶奪',
               '竊佔', '偽造有價證券', '妨害秩序', '違反藥事法', '公共危險', '妨害名譽', '其他', '暴力犯罪']

# 發生數數據
cases_data = {
    '2015': [297800, 66255, 666, 6969, 11141, 21825, 1909, 6361, 522, 13431, 647, 2220, 3648, 1126, 7, 5671, 3406, 49576, 5304, 1287, 740, 741, 78, 117, 301, 71075, 4771, 6748, 1956],
    '2016': [294831, 57606, 295, 6798, 11790, 23994, 1347, 7136, 465, 13755, 622, 1622, 3642, 885, 4, 6147, 3424, 54873, 5335, 1474, 643, 684, 74, 92, 631, 68776, 5333, 6452, 1627],
    '2017': [293453, 52025, 246, 6447, 11709, 23623, 857, 7391, 451, 13820, 591, 1537, 3353, 806, 3, 6439, 3438, 58515, 5298, 1573, 523, 634, 71, 201, 734, 67148, 6797, 8758, 1260],
    '2018': [284538, 47591, 173, 4542, 12256, 24585, 473, 8206, 379, 15099, 616, 1540, 3263, 685, 5, 7382, 3091, 55480, 5439, 1622, 399, 595, 70, 249, 385, 64153, 7611, 7324, 993],
    '2019': [268349, 42272, 115, 4858, 13213, 24642, 669, 8990, 378, 16588, 649, 1218, 3384, 575, 6, 7801, 2964, 47035, 5403, 1572, 329, 559, 81, 228, 326, 59876, 8083, 7168, 859],
    '2020': [259713, 37016, 112, 3175, 12666, 24607, 1200, 9994, 332, 16578, 451, 999, 4217, 620, 1, 8160, 2980, 45489, 5232, 1536, 281, 690, 77, 1231, 828, 53835, 8949, 8822, 707],
    '2021': [243082, 35067, 73, 2513, 12717, 26068, 614, 11950, 292, 18695, 319, 991, 4081, 562, 7, 8420, 3065, 38644, 5879, 1252, 267, 737, 65, 1390, 460, 42001, 8960, 9497, 598],
    '2022': [265518, 37670, 67, 3135, 13972, 30876, 856, 14438, 254, 21172, 349, 849, 4520, 544, 1, 10067, 3422, 38088, 6791, 1224, 233, 743, 70, 1229, 332, 41331, 9833, 12089, 499]
}

# 破獲數數據
cleared_data = {
    '2015': [273567, 55055, 666, 6969, 10476, 18520, 1902, 5816, 518, 13389, 610, 2205, 3637, 1020, 7, 4056, 2630, 49576, 2955, 1282, 756, 706, 63, 112, 301, 70984, 4009, 6588, 2008],
    '2016': [274091, 48898, 295, 6798, 11118, 20565, 1340, 6601, 459, 13648, 603, 1608, 3558, 845, 4, 4686, 2734, 54873, 3410, 1471, 668, 673, 62, 89, 631, 68803, 4491, 6338, 1656],
    '2017': [277506, 46022, 246, 6447, 11152, 21667, 844, 6904, 446, 13711, 560, 1521, 3244, 765, 3, 5090, 2832, 58515, 3687, 1568, 554, 613, 67, 199, 734, 67119, 5735, 8644, 1293],
    '2018': [270882, 43262, 173, 4542, 11674, 22697, 462, 7704, 374, 14969, 590, 1521, 3215, 656, 5, 6079, 2615, 55480, 4099, 1618, 412, 593, 64, 245, 385, 64138, 6565, 7173, 995],
    '2019': [258706, 40406, 115, 4858, 12856, 22883, 658, 8553, 388, 16426, 632, 1213, 3310, 568, 6, 6718, 2610, 47035, 4483, 1572, 338, 546, 76, 227, 326, 59841, 7034, 7037, 898],
    '2020': [253741, 36597, 112, 3175, 12355, 24122, 1185, 9459, 335, 16369, 449, 985, 4129, 578, 1, 7268, 2744, 45489, 4687, 1532, 296, 671, 73, 1215, 828, 53787, 8301, 8592, 737],
    '2021': [240177, 34826, 73, 2513, 12620, 25815, 613, 11809, 289, 18723, 312, 977, 3929, 543, 7, 8008, 2896, 38644, 5520, 1253, 269, 733, 66, 1382, 460, 41987, 8719, 9384, 597],
    '2022': [256733, 36603, 67, 3135, 13435, 30026, 845, 13669, 253, 20479, 338, 834, 4324, 480, 1, 9385, 3233, 38088, 6177, 1212, 229, 726, 68, 1221, 332, 41257, 9172, 11195, 497]
}

# 嫌疑犯數據
offenders_data = {
    '2015': [269296, 33913, 685, 13366, 13324, 17888, 1967, 6420, 897, 13295, 728, 2483, 3537, 1150, 33, 3283, 2531, 53622, 2845, 1277, 856, 961, 69, 134, 374, 70305, 4030, 9979, 2522],
    '2016': [272817, 31543, 251, 11251, 15086, 21005, 1587, 7442, 844, 13723, 773, 1801, 3415, 1153, 10, 3716, 2653, 58707, 3396, 1432, 806, 879, 84, 144, 614, 67654, 4617, 8652, 2208],
    '2017': [287294, 32204, 261, 11038, 15505, 25104, 1230, 8535, 842, 14183, 743, 1682, 3193, 1217, 23, 4237, 2820, 62644, 3872, 1534, 707, 787, 85, 559, 606, 67874, 5957, 11022, 1910],
    '2018': [291621, 32028, 175, 9988, 16180, 28169, 621, 9731, 849, 15535, 795, 1743, 3123, 1150, 35, 5154, 2668, 59106, 4367, 1585, 560, 838, 76, 725, 334, 65176, 6849, 10053, 1666],
    '2019': [277664, 31398, 121, 9792, 18381, 30469, 962, 10921, 806, 16888, 849, 1372, 3194, 992, 18, 5639, 2671, 49131, 4838, 1565, 476, 704, 74, 680, 335, 59918, 7302, 9708, 1464],
    '2020': [281811, 29128, 120, 8555, 16330, 35091, 1642, 11633, 632, 17519, 537, 1155, 4002, 945, 5, 6077, 2892, 47779, 4755, 1517, 480, 947, 84, 5995, 769, 54251, 8311, 11778, 1195],
    '2021': [265221, 27929, 86, 6339, 16185, 37335, 903, 14217, 561, 19763, 279, 1105, 3718, 850, 49, 6504, 2811, 40987, 5342, 1244, 407, 902, 61, 6578, 490, 41844, 8687, 11919, 1073],
    '2022': [291891, 31139, 80, 6853, 17303, 46690, 1239, 16358, 424, 21514, 300, 955, 4199, 756, 4, 7876, 3046, 39964, 6175, 1263, 341, 917, 67, 6187, 324, 41285, 9263, 14825, 761]
}

# 1. 總體犯罪趨勢圖（發生數、破獲數、嫌疑犯數）
def plot_overall_trend():
    plt.figure(figsize=(12, 8))
    
    total_cases = [cases_data[year][0] for year in years]
    total_cleared = [cleared_data[year][0] for year in years]
    total_offenders = [offenders_data[year][0] for year in years]
    
    plt.plot(years, total_cases, marker='o', linewidth=2, label='發生數', color='red')
    plt.plot(years, total_cleared, marker='s', linewidth=2, label='破獲數', color='blue')
    plt.plot(years, total_offenders, marker='^', linewidth=2, label='嫌疑犯數', color='green')
    
    plt.title('台灣刑事案件總體趨勢 (2015-2022)', fontsize=16, fontweight='bold')
    plt.xlabel('年份', fontsize=12)
    plt.ylabel('案件數/人數', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# 2. 2022年各犯罪類型發生數圓餅圖
def plot_crime_types_pie_2022():
    plt.figure(figsize=(14, 10))
    
    # 選取2022年的主要犯罪類型（排除總計）
    crime_names = ['竊盜', '詐欺背信', '駕駛過失', '妨害自由', '傷害', '侵占', '妨害公務', '其他']
    crime_values_2022 = [37670, 30876, 21172, 14438, 13972, 10067, 6791, 12089]
    
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc', '#c2c2f0', '#ffb3e6', '#c4e17f']
    
    plt.pie(crime_values_2022, labels=crime_names, autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title('2022年主要犯罪類型分布', fontsize=16, fontweight='bold')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

# 3. 主要犯罪類型趨勢比較
def plot_major_crimes_trend():
    plt.figure(figsize=(14, 10))
    
    major_crimes = ['竊盜', '詐欺背信', '駕駛過失', '妨害自由', '傷害']
    major_indices = [1, 5, 9, 7, 4]  # 對應在crime_types中的索引
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    for i, (crime, idx) in enumerate(zip(major_crimes, major_indices)):
        values = [cases_data[year][idx] for year in years]
        plt.plot(years, values, marker='o', linewidth=2, label=crime, color=colors[i])
    
    plt.title('主要犯罪類型發生數趨勢 (2015-2022)', fontsize=16, fontweight='bold')
    plt.xlabel('年份', fontsize=12)
    plt.ylabel('發生數', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# 4. 破獲率分析
def plot_clearance_rate():
    plt.figure(figsize=(14, 8))
    
    # 計算總體破獲率
    clearance_rates = []
    for year in years:
        rate = (cleared_data[year][0] / cases_data[year][0]) * 100
        clearance_rates.append(rate)
    
    bars = plt.bar(years, clearance_rates, color='skyblue', alpha=0.7, edgecolor='navy')
    
    # 在每個柱子上添加數值標籤
    for bar, rate in zip(bars, clearance_rates):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{rate:.1f}%', ha='center', va='bottom', fontsize=10)
    
    plt.title('台灣刑事案件破獲率趨勢 (2015-2022)', fontsize=16, fontweight='bold')
    plt.xlabel('年份', fontsize=12)
    plt.ylabel('破獲率 (%)', fontsize=12)
    plt.ylim(85, 100)
    plt.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# 5. 各犯罪類型發生數橫條圖（2022年）
def plot_all_crimes_bar_2022():
    plt.figure(figsize=(12, 14))
    
    # 排除總計，取其他所有犯罪類型
    selected_crimes = crime_types[1:]  # 去掉總計
    selected_values = cases_data['2022'][1:]  # 去掉總計的數值
    
    # 按數值排序
    sorted_data = sorted(zip(selected_crimes, selected_values), key=lambda x: x[1], reverse=True)
    sorted_crimes, sorted_values = zip(*sorted_data)
    
    # 只顯示前20種犯罪類型以避免圖表過於擁擠
    top_crimes = sorted_crimes[:20]
    top_values = sorted_values[:20]
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(top_crimes)))
    
    bars = plt.barh(range(len(top_crimes)), top_values, color=colors)
    plt.yticks(range(len(top_crimes)), top_crimes)
    
    # 在每個柱子上添加數值標籤
    for i, (bar, value) in enumerate(zip(bars, top_values)):
        plt.text(value + max(top_values)*0.01, bar.get_y() + bar.get_height()/2,
                f'{value:,}', ha='left', va='center', fontsize=9)
    
    plt.title('2022年各犯罪類型發生數排名（前20名）', fontsize=16, fontweight='bold')
    plt.xlabel('發生數', fontsize=12)
    plt.ylabel('犯罪類型', fontsize=12)
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.show()

# 6. 2022年所有犯罪類型發生數與嫌疑犯人數比較圖
def plot_all_crimes_comparison_2022():
    plt.figure(figsize=(16, 12))
    
    # 排除總計，取其他所有犯罪類型
    selected_crimes = crime_types[1:]  # 去掉總計
    cases_values = cases_data['2022'][1:]  # 發生數
    offenders_values = offenders_data['2022'][1:]  # 嫌疑犯人數
    
    # 按發生數排序
    sorted_data = sorted(zip(selected_crimes, cases_values, offenders_values), 
                        key=lambda x: x[1], reverse=True)
    sorted_crimes, sorted_cases, sorted_offenders = zip(*sorted_data)
    
    # 設定x軸位置
    x = np.arange(len(sorted_crimes))
    width = 0.35
    
    # 創建雙柱狀圖
    fig, ax = plt.subplots(figsize=(16, 12))
    bars1 = ax.bar(x - width/2, sorted_cases, width, label='發生數', 
                   color='steelblue', alpha=0.8)
    bars2 = ax.bar(x + width/2, sorted_offenders, width, label='嫌疑犯人數', 
                   color='coral', alpha=0.8)
    
    # 設定圖表標籤和標題
    ax.set_xlabel('犯罪類型', fontsize=12)
    ax.set_ylabel('案件數/人數', fontsize=12)
    ax.set_title('2022年各犯罪類型發生數與嫌疑犯人數比較', fontsize=16, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(sorted_crimes, rotation=45, ha='right')
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')
    
    # 在重要的柱子上添加數值標籤（只顯示前10名）
    for i in range(min(10, len(bars1))):
        # 發生數標籤
        height1 = bars1[i].get_height()
        ax.text(bars1[i].get_x() + bars1[i].get_width()/2., height1 + max(sorted_cases)*0.01,
                f'{int(height1):,}', ha='center', va='bottom', fontsize=8, rotation=0)
        
        # 嫌疑犯人數標籤
        height2 = bars2[i].get_height()
        ax.text(bars2[i].get_x() + bars2[i].get_width()/2., height2 + max(sorted_offenders)*0.01,
                f'{int(height2):,}', ha='center', va='bottom', fontsize=8, rotation=0)
    
    plt.tight_layout()
    plt.show()

# 7. 2022年所有犯罪類型發生數詳細橫條圖（完整版）
def plot_complete_crimes_horizontal_2022():
    plt.figure(figsize=(14, 20))
    
    # 排除總計，取其他所有犯罪類型
    selected_crimes = crime_types[1:]  # 去掉總計
    selected_values = cases_data['2022'][1:]  # 去掉總計的數值
    
    # 按數值排序
    sorted_data = sorted(zip(selected_crimes, selected_values), key=lambda x: x[1], reverse=True)
    sorted_crimes, sorted_values = zip(*sorted_data)
    
    # 為不同範圍的犯罪類型設定不同顏色
    colors = []
    for value in sorted_values:
        if value >= 30000:
            colors.append('#d62728')  # 紅色 - 高發犯罪
        elif value >= 10000:
            colors.append('#ff7f0e')  # 橙色 - 中高發犯罪
        elif value >= 5000:
            colors.append('#2ca02c')  # 綠色 - 中等犯罪
        elif value >= 1000:
            colors.append('#1f77b4')  # 藍色 - 一般犯罪
        else:
            colors.append('#9467bd')  # 紫色 - 低發犯罪
    
    bars = plt.barh(range(len(sorted_crimes)), sorted_values, color=colors, alpha=0.8)
    plt.yticks(range(len(sorted_crimes)), sorted_crimes, fontsize=10)
    
    # 在每個柱子上添加數值標籤
    for i, (bar, value) in enumerate(zip(bars, sorted_values)):
        plt.text(value + max(sorted_values)*0.01, bar.get_y() + bar.get_height()/2,
                f'{value:,}', ha='left', va='center', fontsize=9)
    
    plt.title('2022年所有犯罪類型發生數完整排名', fontsize=16, fontweight='bold')
    plt.xlabel('發生數', fontsize=12)
    plt.ylabel('犯罪類型', fontsize=12)
    plt.grid(True, alpha=0.3, axis='x')
    
    # 添加顏色說明
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='#d62728', alpha=0.8, label='高發犯罪 (≥30,000)'),
                      Patch(facecolor='#ff7f0e', alpha=0.8, label='中高發犯罪 (10,000-29,999)'),
                      Patch(facecolor='#2ca02c', alpha=0.8, label='中等犯罪 (5,000-9,999)'),
                      Patch(facecolor='#1f77b4', alpha=0.8, label='一般犯罪 (1,000-4,999)'),
                      Patch(facecolor='#9467bd', alpha=0.8, label='低發犯罪 (<1,000)')]
    plt.legend(handles=legend_elements, loc='lower right', fontsize=10)
    
    plt.tight_layout()
    plt.show()



# 執行所有圖表生成
if __name__ == "__main__":
    print("正在生成台灣刑事案件統計圖表...")
    
    # 生成圖表
    plot_all_crimes_bar_2022()  # 保留的原始圖表
    plot_all_crimes_comparison_2022()  # 發生數與嫌疑犯人數比較
    plot_complete_crimes_horizontal_2022()  # 完整的所有犯罪類型橫條圖
    
    print("所有圖表生成完成！")