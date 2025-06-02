import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties

# 設置中文字體
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # Mac使用
# plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # Windows使用
plt.rcParams['axes.unicode_minus'] = False

# 讀取數據並清洗
def load_and_clean_data(filepath):
    # 讀取原始文件，跳過前3行
    df = pd.read_csv(filepath, skiprows=3, encoding='utf-8')
    
    # 查看實際讀取的列名
    print("原始列名:", df.columns.tolist())
    
    # 根據實際列名重新命名
    # 原始結構: ['機關別', 'Unnamed: 1', '總計', 'Unnamed: 3', 'Unnamed: 4', ...]
    # 每種教育程度有3列: 男, 女, 總和
    new_columns = ['機關別']
    categories = ['總計', '不識字', '自修', '國小', '國中', '高中職', '大專', '研究所', '其他']
    
    for category in categories:
        new_columns.extend([f'{category}_男', f'{category}_女', f'{category}_總和'])
    
    # 確保列數匹配
    if len(df.columns) > len(new_columns):
        df = df.iloc[:, :len(new_columns)]
    df.columns = new_columns[:len(df.columns)]
    
    # 清理數據 - 去除空行
    df = df.dropna(subset=['機關別'])
    df = df[df['機關別'] != '民國112年']  # 移除總計行(可選)
    
    # 轉換數值列為數字類型
    numeric_cols = df.columns.drop('機關別')
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    return df

# 1. 堆疊條形圖 - 各地區教育程度分布
def plot_education_by_region(df):
    # 選擇要繪製的教育程度
    education_cols = ['國小_總和', '國中_總和', '高中職_總和', '大專_總和', '研究所_總和']
    
    # 確保這些列存在
    available_cols = [col for col in education_cols if col in df.columns]
    
    plt.figure(figsize=(14, 8))
    df.set_index('機關別')[available_cols].plot(kind='bar', stacked=True)
    
    plt.title('各地區刑事案件嫌疑犯教育程度分布(2023年)')
    plt.ylabel('人數')
    plt.xlabel('地區')
    plt.xticks(rotation=45)
    plt.legend(title='教育程度', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('education_by_region.png', dpi=300, bbox_inches='tight')
    plt.show()

# 2. 性別與教育程度分組條形圖
def plot_education_by_gender(df):
    # 準備數據 - 計算各教育程度的男女比例
    education_levels = ['國小', '國中', '高中職', '大專', '研究所']
    
    # 確保這些列存在
    male_cols = [f'{level}_男' for level in education_levels if f'{level}_男' in df.columns]
    female_cols = [f'{level}_女' for level in education_levels if f'{level}_女' in df.columns]
    
    male_data = df[male_cols].sum()
    female_data = df[female_cols].sum()
    
    x = range(len(male_cols))
    width = 0.35
    
    plt.figure(figsize=(12, 6))
    plt.bar(x, male_data, width, label='男性')
    plt.bar([i + width for i in x], female_data, width, label='女性')
    
    plt.title('刑事案件嫌疑犯教育程度與性別分布(2023年)')
    plt.ylabel('人數')
    plt.xlabel('教育程度')
    plt.xticks([i + width/2 for i in x], [col.replace('_男', '') for col in male_cols])
    plt.legend()
    plt.tight_layout()
    plt.savefig('education_by_gender.png', dpi=300)
    plt.show()

# 3. 教育程度比例餅圖
def plot_education_pie_chart(df):
    # 計算各教育程度總和
    education_levels = ['國小', '國中', '高中職', '大專', '研究所', '其他']
    sum_cols = [f'{level}_總和' for level in education_levels if f'{level}_總和' in df.columns]
    
    sizes = df[sum_cols].sum()
    labels = [col.replace('_總和', '') for col in sum_cols]
    
    plt.figure(figsize=(10, 10))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('刑事案件嫌疑犯教育程度比例分布(2023年)')
    plt.savefig('education_pie_chart.png', dpi=300)
    plt.show()

# 4. 熱力圖 - 地區與教育程度
def plot_education_heatmap(df):
    # 準備數據
    education_levels = ['國小', '國中', '高中職', '大專', '研究所']
    sum_cols = [f'{level}_總和' for level in education_levels if f'{level}_總和' in df.columns]
    
    if not sum_cols:
        print("沒有找到可用的教育程度數據列")
        return
    
    data = df.set_index('機關別')[sum_cols]
    data.columns = [col.replace('_總和', '') for col in sum_cols]
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(data, cmap='YlOrRd', annot=True, fmt='g', linewidths=.5)
    plt.title('各地區與教育程度熱力圖(人數)')
    plt.xlabel('教育程度')
    plt.ylabel('地區')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('education_heatmap.png', dpi=300)
    plt.show()

# 主程序
if __name__ == "__main__":
    # 載入數據
    filepath = '刑事案件嫌疑犯人數－按教育別2.csv'
    try:
        df = load_and_clean_data(filepath)
        print("數據加載成功，前5行數據:")
        print(df.head())
        
        # 生成所有圖表
        plot_education_by_region(df)
        plot_education_by_gender(df)
        plot_education_pie_chart(df)
        plot_education_heatmap(df)
        
        print("所有圖表已生成並保存為PNG文件")
    except Exception as e:
        print(f"發生錯誤: {e}")
        print("請檢查CSV文件結構是否與預期一致")