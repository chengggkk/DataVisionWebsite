import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 2022年犯罪數據（從CSV提取）
crime_data = {
    '竊盜': {'少年': 1225, '青年': 1821, '成年': 28093},
    '贓物': {'少年': 3, '青年': 8, '成年': 69},
    '賭博': {'少年': 247, '青年': 736, '成年': 5870},
    '傷害': {'少年': 896, '青年': 1636, '成年': 14771},
    '詐欺背信': {'少年': 1670, '青年': 9846, '成年': 35174},
    '重利': {'少年': 10, '青年': 270, '成年': 959},
    '妨害自由': {'少年': 577, '青年': 1876, '成年': 13905},
    '殺人': {'少年': 13, '青年': 68, '成年': 343},
    '駕駛過失': {'少年': 318, '青年': 2615, '成年': 18581},
    '妨害婚姻及家庭': {'少年': 52, '青年': 81, '成年': 167},
    '妨害風化': {'少年': 13, '青年': 100, '成年': 842},
    '妨害性自主罪': {'少年': 875, '青年': 880, '成年': 2444},
    '恐嚇取財': {'少年': 29, '青年': 152, '成年': 575},
    '擄人勒贖': {'少年': 0, '青年': 1, '成年': 3},
    '侵占': {'少年': 143, '青年': 698, '成年': 7035},
    '偽造文書印文': {'少年': 64, '青年': 266, '成年': 2716},
    '違反毒品危害防制條例': {'少年': 456, '青年': 3088, '成年': 36420},
    '毀棄損壞': {'少年': 230, '青年': 685, '成年': 5260},
    '妨害公務': {'少年': 27, '青年': 122, '成年': 1114},
    '強盜搶奪': {'少年': 11, '青年': 53, '成年': 277},
    '竊佔': {'少年': 1, '青年': 12, '成年': 904},
    '偽造有價證券': {'少年': 1, '青年': 2, '成年': 64},
    '妨害秩序': {'少年': 997, '青年': 2248, '成年': 2942},
    '違反藥事法': {'少年': 10, '青年': 37, '成年': 277},
    '違反森林法': {'少年': 1, '青年': 10, '成年': 395},
    '違反著作權法': {'少年': 14, '青年': 114, '成年': 1935},
    '公共危險': {'少年': 349, '青年': 2618, '成年': 38318},
    '侵害墳墓屍體': {'少年': 0, '青年': 2, '成年': 14},
    '妨害名譽': {'少年': 239, '青年': 1166, '成年': 7858},
    '違反選罷法': {'少年': 20, '青年': 65, '成年': 3760},
    '妨害秘密': {'少年': 50, '青年': 166, '成年': 872},
    '遺棄': {'少年': 1, '青年': 8, '成年': 114},
    '懲治走私條例': {'少年': 0, '青年': 0, '成年': 2},
    '違反貪汙治罪條例': {'少年': 0, '青年': 1, '成年': 19},
    '瀆職': {'少年': 0, '青年': 0, '成年': 17},
    '妨害兵役': {'少年': 2, '青年': 7, '成年': 48},
    '偽證': {'少年': 0, '青年': 1, '成年': 35},
    '誣告': {'少年': 9, '青年': 38, '成年': 482},
    '湮滅證據': {'少年': 0, '青年': 2, '成年': 10},
    '藏匿頂替': {'少年': 3, '青年': 9, '成年': 51},
    '脫逃': {'少年': 0, '青年': 2, '成年': 10},
    '違反槍砲彈業刀械管制條例': {'少年': 37, '青年': 187, '成年': 915},
    '違反就業服務法': {'少年': 0, '青年': 0, '成年': 14},
    '妨害電腦使用': {'少年': 69, '青年': 138, '成年': 732},
    '其他': {'少年': 876, '青年': 1634, '成年': 12315}
}

def analyze_crime_data():
    """
    分析犯罪數據並輸出結果
    """
    print("=" * 80)
    print("                    2022年犯罪數據分析報告")
    print("=" * 80)
    
    # 1. 基本統計分析
    total_crimes = 0
    age_totals = {'少年': 0, '青年': 0, '成年': 0}
    crime_totals = {}
    
    for crime, ages in crime_data.items():
        crime_total = sum(ages.values())
        crime_totals[crime] = crime_total
        total_crimes += crime_total
        
        for age_group, count in ages.items():
            age_totals[age_group] += count
    
    print(f"\n【基本統計資料】")
    print(f"總犯罪人數: {total_crimes:,} 人")
    print(f"少年犯罪人數: {age_totals['少年']:,} 人 ({age_totals['少年']/total_crimes*100:.1f}%)")
    print(f"青年犯罪人數: {age_totals['青年']:,} 人 ({age_totals['青年']/total_crimes*100:.1f}%)")
    print(f"成年犯罪人數: {age_totals['成年']:,} 人 ({age_totals['成年']/total_crimes*100:.1f}%)")
    
    # 2. 最常見的犯罪類型
    print(f"\n【最常見的犯罪類型 Top 10】")
    sorted_crimes = sorted(crime_totals.items(), key=lambda x: x[1], reverse=True)
    for i, (crime, count) in enumerate(sorted_crimes[:10], 1):
        percentage = count / total_crimes * 100
        print(f"{i:2d}. {crime:<15} {count:>6,} 人 ({percentage:4.1f}%)")
    
    # 3. 年齡層犯罪特徵分析
    print(f"\n【年齡層犯罪特徵分析】")
    
    # 找出各年齡層最常犯的罪名
    age_crime_rates = {'少年': {}, '青年': {}, '成年': {}}
    
    for crime, ages in crime_data.items():
        for age_group, count in ages.items():
            if count > 0:
                age_crime_rates[age_group][crime] = count
    
    for age_group in ['少年', '青年', '成年']:
        print(f"\n{age_group}犯罪特徵:")
        sorted_age_crimes = sorted(age_crime_rates[age_group].items(), key=lambda x: x[1], reverse=True)
        print(f"  最常犯罪類型:")
        for i, (crime, count) in enumerate(sorted_age_crimes[:5], 1):
            percentage = count / age_totals[age_group] * 100
            print(f"    {i}. {crime:<15} {count:>5,} 人 ({percentage:4.1f}%)")
    
    # 4. 犯罪比例分析
    print(f"\n【犯罪比例分析】")
    print("各犯罪類型中年齡層分布:")
    
    # 找出特別值得注意的犯罪類型
    notable_crimes = []
    for crime, ages in crime_data.items():
        total = sum(ages.values())
        if total >= 1000:  # 只分析總數超過1000的犯罪
            juvenile_rate = ages['少年'] / total * 100
            young_rate = ages['青年'] / total * 100
            adult_rate = ages['成年'] / total * 100
            
            notable_crimes.append({
                'crime': crime,
                'total': total,
                'juvenile_rate': juvenile_rate,
                'young_rate': young_rate,
                'adult_rate': adult_rate
            })
    
    # 按少年犯罪比例排序
    notable_crimes.sort(key=lambda x: x['juvenile_rate'], reverse=True)
    
    print("\n少年犯罪比例較高的犯罪類型:")
    for crime_info in notable_crimes[:5]:
        print(f"  {crime_info['crime']:<15} - 少年: {crime_info['juvenile_rate']:4.1f}%, " +
              f"青年: {crime_info['young_rate']:4.1f}%, 成年: {crime_info['adult_rate']:4.1f}%")
    
    # 5. 重要發現與結論
    print(f"\n【重要發現與結論】")
    
    # 計算一些重要指標
    high_juvenile_crimes = [c for c in notable_crimes if c['juvenile_rate'] > 10]
    economic_crimes = ['竊盜', '詐欺背信', '侵占', '強盜搶奪']
    violent_crimes = ['殺人', '傷害', '妨害性自主罪', '強盜搶奪']
    
    print(f"1. 年齡分布特徵:")
    print(f"   - 成年人占總犯罪人數的 {age_totals['成年']/total_crimes*100:.1f}%，為主要犯罪群體")
    print(f"   - 青年犯罪占 {age_totals['青年']/total_crimes*100:.1f}%，需要特別關注")
    print(f"   - 少年犯罪占 {age_totals['少年']/total_crimes*100:.1f}%，雖比例較低但不容忽視")
    
    print(f"\n2. 主要犯罪類型:")
    top_3_crimes = sorted_crimes[:3]
    for i, (crime, count) in enumerate(top_3_crimes, 1):
        print(f"   - 第{i}名: {crime} ({count:,}人，占{count/total_crimes*100:.1f}%)")
    
    print(f"\n3. 值得關注的現象:")
    
    # 找出少年犯罪率特別高的類型
    high_juvenile_crime = max(notable_crimes, key=lambda x: x['juvenile_rate'])
    print(f"   - '{high_juvenile_crime['crime']}' 在少年中的比例達 {high_juvenile_crime['juvenile_rate']:.1f}%，需加強預防")
    
    # 毒品犯罪分析
    drug_crime = crime_data['違反毒品危害防制條例']
    drug_total = sum(drug_crime.values())
    print(f"   - 毒品犯罪總數 {drug_total:,} 人，其中青年占 {drug_crime['青年']/drug_total*100:.1f}%，成年占 {drug_crime['成年']/drug_total*100:.1f}%")
    
    # 詐欺犯罪分析
    fraud_crime = crime_data['詐欺背信']
    fraud_total = sum(fraud_crime.values())
    print(f"   - 詐欺背信犯罪激增，總數達 {fraud_total:,} 人，青年參與率 {fraud_crime['青年']/fraud_total*100:.1f}%")
    
    print(f"\n4. 政策建議:")
    print(f"   - 加強青少年法治教育，特別針對網路詐欺和毒品防制")
    print(f"   - 建立更完善的犯罪預防機制，降低初犯率")
    print(f"   - 重點關注經濟犯罪和毒品犯罪的預防工作")
    print(f"   - 針對不同年齡層設計差異化的犯罪預防策略")
    
    print("\n" + "=" * 80)
    
    return crime_totals

# 執行分析
crime_totals = analyze_crime_data()

# 選擇主要犯罪類型（案件數較多的前10種）
major_crimes = {}
for crime, ages in crime_data.items():
    total = sum(ages.values())
    if total > 2000:  # 只顯示總數超過2000的犯罪類型
        major_crimes[crime] = ages

# 準備數據
crimes = list(major_crimes.keys())
juvenile_data = [major_crimes[crime]['少年'] for crime in crimes]
young_adult_data = [major_crimes[crime]['青年'] for crime in crimes]
adult_data = [major_crimes[crime]['成年'] for crime in crimes]

# 創建圖表
fig, ax = plt.subplots(figsize=(15, 8))

# 設定寬度
width = 0.8
x = np.arange(len(crimes))

# 創建堆疊柱狀圖
p1 = ax.bar(x, juvenile_data, width, label='少年', color='#4472C4')
p2 = ax.bar(x, young_adult_data, width, bottom=juvenile_data, label='青年', color='#E67E22')
p3 = ax.bar(x, adult_data, width, bottom=np.array(juvenile_data) + np.array(young_adult_data), 
           label='成年', color='#27AE60')

# 設定標籤和標題
ax.set_xlabel('犯罪類型', fontsize=12)
ax.set_ylabel('人數', fontsize=12)
ax.set_title('2022年各犯罪類型年齡層分布圖', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(crimes, rotation=45, ha='right')

# 添加圖例
ax.legend(loc='upper right')

# 設定格線
ax.grid(True, alpha=0.3, axis='y')

# 調整佈局
plt.tight_layout()

# 顯示圖表
plt.show()

# 如果需要保存圖片
# plt.savefig('2022年犯罪統計圖.png', dpi=300, bbox_inches='tight')

print("\n圖表已生成完成！")
print(f"共顯示 {len(crimes)} 種主要犯罪類型")