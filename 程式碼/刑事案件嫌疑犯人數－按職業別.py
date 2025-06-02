import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import font_manager
import warnings
warnings.filterwarnings('ignore')

# 設置中文字體
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft JhengHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 讀取並處理數據
def load_and_process_data():
    # 根據CSV結構創建完整的年度數據 (2003-2022)
    years = list(range(2003, 2023))
    
    # 定義職業類別（根據CSV標題）
    occupations = [
        '民意代表、主管及經理人員',
        '專業人員', 
        '技術員及助理專業人員',
        '事務支援人員',
        '服務(不含保安工作人員)',
        '銷售及展示工作人員',
        '農林漁牧業生產人員',
        '保安服務工作人員(含軍人)',
        '技藝(技術)有關工作人員',
        '駕駛及移運設備操作人員',
        '駕駛及移運操作除外之機械設備操作及組裝人員',
        '基層技術工及勞力工',
        '學生',
        '無職',
        '其他(含不詳)'
    ]
    
    # 從CSV提取的實際數據
    data_dict = {
        2003: [6670, 1392, 4211, 1644, 8652, 8967, 5291, 2203, 16004, 5387, 5661, 14870, 10263, 65144, 2328],
        2004: [6465, 1551, 4674, 1564, 11310, 8574, 5409, 2171, 18682, 5312, 5807, 19238, 9180, 74455, 2583],
        2005: [7190, 1707, 4674, 1574, 16077, 8988, 6772, 1963, 22184, 5368, 5629, 24155, 8936, 88523, 3685],
        2006: [6524, 2116, 5251, 1783, 22855, 9561, 6385, 2150, 26157, 6405, 6780, 29406, 9977, 88774, 5069],
        2007: [6792, 2742, 5712, 1657, 30013, 10255, 6707, 2443, 34416, 7110, 9344, 39807, 12165, 90127, 6570],
        2008: [6694, 2972, 5517, 1262, 32577, 8817, 7169, 2254, 36601, 7133, 7082, 44428, 12924, 86840, 8916],
        2009: [5656, 2990, 5576, 1100, 34591, 7888, 7433, 2146, 30113, 6948, 6196, 43310, 12186, 87570, 8270],
        2010: [5550, 3109, 5234, 1038, 36388, 7779, 7697, 2010, 27277, 7130, 7081, 47117, 12035, 90236, 9659],
        2011: [4954, 3442, 4907, 809, 43318, 6745, 6520, 1879, 25321, 7091, 5053, 49166, 14533, 78504, 8114],
        2012: [4785, 3451, 5139, 783, 44720, 6798, 7285, 2421, 23750, 7179, 5033, 52530, 16458, 73821, 7905],
        2013: [4661, 3922, 5395, 738, 43818, 5747, 8467, 2706, 25073, 7566, 4942, 57103, 13455, 65216, 6501],
        2014: [5060, 3804, 5315, 813, 46704, 5477, 8716, 2644, 29616, 7183, 6226, 55244, 12502, 65723, 6576],
        2015: [4743, 4148, 5310, 774, 48687, 5304, 8421, 2995, 30137, 7704, 6488, 59551, 13351, 65533, 6150],
        2016: [4483, 4434, 5849, 862, 52217, 4058, 8542, 3329, 31369, 7836, 6989, 59335, 11482, 64794, 7238],
        2017: [3641, 6251, 6558, 1070, 56334, 3772, 9327, 3525, 33192, 8026, 6472, 62714, 12028, 66844, 7540],
        2018: [4215, 7394, 6938, 1006, 59220, 3926, 10077, 3665, 31604, 8372, 4646, 61410, 10917, 68453, 9778],
        2019: [4047, 6957, 5937, 1052, 55681, 5742, 9074, 3707, 21797, 7490, 5044, 65798, 11672, 64776, 8890],
        2020: [4656, 5467, 3180, 1215, 66454, 7065, 8817, 3689, 16013, 6364, 5760, 70094, 12233, 61966, 8838],
        2021: [4421, 5740, 3227, 1026, 66169, 6340, 8031, 3608, 14515, 6553, 4254, 64134, 11871, 55937, 9395],
        2022: [4569, 6817, 4621, 1149, 73627, 8088, 8638, 4160, 14044, 8303, 3469, 69167, 12570, 59803, 12866]
    }
    
    # 創建DataFrame
    df = pd.DataFrame(data_dict, index=occupations).T
    return df

# 載入數據
df = load_and_process_data()

# 1. 圓餅圖 - 2022年各職業類別分布
def plot_pie_chart():
    plt.figure(figsize=(12, 10))
    
    # 使用2022年數據
    data_2022 = df.loc[2022]
    
    # 只顯示前10大職業類別，其餘合併為"其他"
    sorted_data = data_2022.sort_values(ascending=False)
    top_10 = sorted_data.head(10)
    others_sum = sorted_data.tail(len(sorted_data)-10).sum()
    
    if others_sum > 0:
        pie_data = pd.concat([top_10, pd.Series([others_sum], index=['其他職業'])])
    else:
        pie_data = top_10
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(pie_data)))
    
    plt.pie(pie_data.values, labels=pie_data.index, autopct='%1.1f%%', 
            colors=colors, startangle=90)
    plt.title('2022年刑事案件嫌疑犯職業分布', fontsize=16, fontweight='bold')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

# 2. 堆疊面積圖 - 類似您提供的圖片
def plot_stacked_area():
    plt.figure(figsize=(16, 10))
    
    # 選擇主要職業類別來製作堆疊面積圖
    main_categories = [
        '服務(不含保安工作人員)',
        '無職', 
        '基層技術工及勞力工',
        '技藝(技術)有關工作人員',
        '專業人員',
        '學生',
        '農林漁牧業生產人員',
        '其他(含不詳)'
    ]
    
    # 為了更好的視覺效果，將其他小類別合併
    plot_data = pd.DataFrame(index=df.index)
    
    for category in main_categories:
        if category in df.columns:
            plot_data[category] = df[category]
        else:
            # 如果沒有該類別，設為0
            plot_data[category] = 0
    
    # 將其餘小類別合併到"其他"
    other_categories = [col for col in df.columns if col not in main_categories]
    if other_categories:
        plot_data['其他職業'] = df[other_categories].sum(axis=1)
    
    # 定義顏色 - 使用柔和的顏色搭配
    colors = [
        "#B9B5FF",  # 淺橙色 - 服務業
        '#C0C0C0',  # 銀色 - 無職
        '#98FB98',  # 淺綠色 - 基層技術工
        '#DDA0DD',  # 淺紫色 - 技藝相關
        "#F08CB2",  # 卡其色 - 專業人員
        '#87CEEB',  # 天藍色 - 學生
        '#F5DEB3',  # 小麥色 - 農林漁牧
        "#A01212"   # 淺灰色 - 其他
    ]
    
    # 創建堆疊面積圖
    plt.stackplot(plot_data.index, 
                  *[plot_data[col] for col in plot_data.columns],
                  labels=plot_data.columns,
                  colors=colors[:len(plot_data.columns)],
                  alpha=0.8)
    
    plt.title('台灣刑事案件嫌疑犯職業類別趨勢圖 (2003-2022)', fontsize=16, fontweight='bold')
    plt.xlabel('年份', fontsize=12)
    plt.ylabel('人數', fontsize=12)
    
    # 設置圖例
    plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=10)
    
    # 設置Y軸格式
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/1000)}k' if x >= 1000 else str(int(x))))
    
    # 設置網格
    plt.grid(True, alpha=0.3, axis='y')
    
    # 設置X軸刻度
    plt.xticks(range(2003, 2023, 2), rotation=45)
    
    plt.tight_layout()
    plt.show()

# 3. 額外的趨勢對比圖 - 主要職業類別變化
def plot_trend_comparison():
    plt.figure(figsize=(16, 10))
    
    # 選擇幾個重要的職業類別
    key_occupations = [
        '服務(不含保安工作人員)',
        '無職',
        '基層技術工及勞力工',
        '專業人員',
        '學生'
    ]
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    for i, occupation in enumerate(key_occupations):
        if occupation in df.columns:
            plt.plot(df.index, df[occupation], 
                    marker='o', linewidth=3, markersize=6,
                    label=occupation, color=colors[i])
    
    plt.title('主要職業類別刑事案件嫌疑犯人數變化趨勢', fontsize=16, fontweight='bold')
    plt.xlabel('年份', fontsize=12)
    plt.ylabel('人數', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.xticks(range(2003, 2023, 2), rotation=45)
    plt.tight_layout()
    plt.show()

# 執行圖表繪製
print("正在生成圖表...")

print("\n1. 生成圓餅圖...")
plot_pie_chart()

print("\n2. 生成堆疊面積圖（類似您提供的圖片）...")
plot_stacked_area()

print("\n3. 生成趨勢對比圖...")
plot_trend_comparison()

print("\n所有圖表生成完成！")

# 顯示數據基本統計信息
print("\n=== 數據基本統計 ===")
print(f"數據時間範圍: {df.index.min()} - {df.index.max()}")
print(f"職業類別數量: {len(df.columns)}")
print(f"年份數量: {len(df.index)}")

print("\n2022年各職業類別人數排名:")
data_2022_sorted = df.loc[2022].sort_values(ascending=False)
for i, (occupation, count) in enumerate(data_2022_sorted.head(10).items(), 1):
    print(f"{i:2d}. {occupation}: {count:,}人")

print(f"\n2022年總計: {df.loc[2022].sum():,}人")