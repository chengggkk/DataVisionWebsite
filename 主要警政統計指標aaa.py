import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import rcParams
import warnings
warnings.filterwarnings('ignore')

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def load_and_clean_data(filename):
    """讀取並清理警政統計資料"""
    # 讀取CSV檔案，跳過前兩行標題
    df = pd.read_csv(filename, encoding='utf-8', skiprows=2)
    
    # 移除空行和無效資料
    df = df.dropna(subset=[df.columns[0]])
    df = df[df.iloc[:, 0].str.contains('民國', na=False)]
    
    # 重新命名欄位
    columns = [
        '年別', '西元年', '全般刑案_發生數', '全般刑案_破獲數', '全般刑案_破獲率', 
        '全般刑案_嫌疑犯', '全般刑案_犯罪率', '全般刑案_犯罪人口率',
        '暴力犯罪_發生數', '暴力犯罪_破獲數', '暴力犯罪_破獲率', 
        '暴力犯罪_嫌疑犯', '暴力犯罪_犯罪率',
        '竊盜_發生數', '竊盜_破獲數', '竊盜_破獲率', '竊盜_嫌疑犯', '竊盜_犯罪率'
    ]
    
    df.columns = columns
    
    # 資料型別轉換
    numeric_columns = [col for col in columns if col not in ['年別']]
    for col in numeric_columns:
        if col in df.columns:
            # 移除千分位逗號並轉換為數值
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')
    
    return df

def create_crime_trend_analysis(df):
    """製作犯罪趨勢分析圖表"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('台灣警政統計趨勢分析 (2003-2023)', fontsize=16, fontweight='bold')
    
    # 1. 全般刑案發生數趨勢
    axes[0, 0].plot(df['西元年'], df['全般刑案_發生數'], marker='o', linewidth=2, color='#e74c3c')
    axes[0, 0].set_title('全般刑案發生數趨勢', fontweight='bold')
    axes[0, 0].set_xlabel('年份')
    axes[0, 0].set_ylabel('發生數 (件)')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # 2. 破獲率趨勢比較
    axes[0, 1].plot(df['西元年'], df['全般刑案_破獲率'], marker='o', label='全般刑案', linewidth=2)
    axes[0, 1].plot(df['西元年'], df['暴力犯罪_破獲率'], marker='s', label='暴力犯罪', linewidth=2)
    axes[0, 1].plot(df['西元年'], df['竊盜_破獲率'], marker='^', label='竊盜', linewidth=2)
    axes[0, 1].set_title('各類犯罪破獲率趨勢', fontweight='bold')
    axes[0, 1].set_xlabel('年份')
    axes[0, 1].set_ylabel('破獲率 (%)')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # 3. 犯罪率趨勢
    axes[1, 0].plot(df['西元年'], df['全般刑案_犯罪率'], marker='o', label='全般刑案', linewidth=2)
    axes[1, 0].plot(df['西元年'], df['暴力犯罪_犯罪率'], marker='s', label='暴力犯罪', linewidth=2)
    axes[1, 0].plot(df['西元年'], df['竊盜_犯罪率'], marker='^', label='竊盜', linewidth=2)
    axes[1, 0].set_title('各類犯罪率趨勢 (件/十萬人口)', fontweight='bold')
    axes[1, 0].set_xlabel('年份')
    axes[1, 0].set_ylabel('犯罪率')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # 4. 近年犯罪結構比例 (2023年)
    latest_year_data = df[df['西元年'] == 2023]
    if not latest_year_data.empty:
        crime_types = ['暴力犯罪', '竊盜', '其他']
        violence_crime = latest_year_data['暴力犯罪_發生數'].iloc[0]
        theft_crime = latest_year_data['竊盜_發生數'].iloc[0]
        total_crime = latest_year_data['全般刑案_發生數'].iloc[0]
        other_crime = total_crime - violence_crime - theft_crime
        
        crime_counts = [violence_crime, theft_crime, other_crime]
        colors = ['#e74c3c', '#3498db', '#95a5a6']
        
        wedges, texts, autotexts = axes[1, 1].pie(crime_counts, labels=crime_types, autopct='%1.1f%%', 
                                                  colors=colors, startangle=90)
        axes[1, 1].set_title('2023年犯罪類型結構', fontweight='bold')
    
    plt.tight_layout()
    return fig

def create_performance_analysis(df):
    """製作警政績效分析圖表"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('台灣警政績效分析', fontsize=16, fontweight='bold')
    
    # 1. 破獲數 vs 發生數散佈圖
    axes[0, 0].scatter(df['全般刑案_發生數'], df['全般刑案_破獲數'], 
                      c=df['西元年'], cmap='viridis', s=60, alpha=0.7)
    # 添加對角線 (理想破獲率100%)
    max_val = max(df['全般刑案_發生數'].max(), df['全般刑案_破獲數'].max())
    axes[0, 0].plot([0, max_val], [0, max_val], 'r--', alpha=0.5, label='100%破獲率')
    axes[0, 0].set_title('破獲數 vs 發生數關係', fontweight='bold')
    axes[0, 0].set_xlabel('發生數 (件)')
    axes[0, 0].set_ylabel('破獲數 (件)')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. 年度績效熱力圖
    performance_data = df[['西元年', '全般刑案_破獲率', '暴力犯罪_破獲率', '竊盜_破獲率']].set_index('西元年').T
    im = axes[0, 1].imshow(performance_data.values, cmap='RdYlGn', aspect='auto')
    axes[0, 1].set_xticks(range(len(performance_data.columns)))
    axes[0, 1].set_xticklabels(performance_data.columns, rotation=45)
    axes[0, 1].set_yticks(range(len(performance_data.index)))
    axes[0, 1].set_yticklabels(['全般刑案', '暴力犯罪', '竊盜'])
    axes[0, 1].set_title('各類犯罪破獲率熱力圖', fontweight='bold')
    plt.colorbar(im, ax=axes[0, 1], label='破獲率 (%)')
    
    # 3. 犯罪減少幅度分析
    df['全般刑案_減少率'] = df['全般刑案_發生數'].pct_change() * -100  # 負值變正值表示減少
    df['暴力犯罪_減少率'] = df['暴力犯罪_發生數'].pct_change() * -100
    df['竊盜_減少率'] = df['竊盜_發生數'].pct_change() * -100
    
    x = range(1, len(df))  # 從第二年開始
    width = 0.25
    
    axes[1, 0].bar([i - width for i in x], df['全般刑案_減少率'].iloc[1:], 
                   width, label='全般刑案', alpha=0.8)
    axes[1, 0].bar(x, df['暴力犯罪_減少率'].iloc[1:], 
                   width, label='暴力犯罪', alpha=0.8)
    axes[1, 0].bar([i + width for i in x], df['竊盜_減少率'].iloc[1:], 
                   width, label='竊盜', alpha=0.8)
    
    axes[1, 0].set_title('年度犯罪減少率', fontweight='bold')
    axes[1, 0].set_xlabel('年份')
    axes[1, 0].set_ylabel('減少率 (%)')
    axes[1, 0].set_xticks(x)
    axes[1, 0].set_xticklabels(df['西元年'].iloc[1:], rotation=45)
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    # 4. 嫌疑犯數量趨勢
    axes[1, 1].stackplot(df['西元年'], 
                        df['暴力犯罪_嫌疑犯'], 
                        df['竊盜_嫌疑犯'], 
                        df['全般刑案_嫌疑犯'] - df['暴力犯罪_嫌疑犯'] - df['竊盜_嫌疑犯'],
                        labels=['暴力犯罪', '竊盜', '其他'], 
                        alpha=0.8)
    axes[1, 1].set_title('各類犯罪嫌疑犯數量趨勢', fontweight='bold')
    axes[1, 1].set_xlabel('年份')
    axes[1, 1].set_ylabel('嫌疑犯數 (人)')
    axes[1, 1].legend(loc='upper right')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    return fig

def generate_summary_report(df):
    """生成統計摘要報告"""
    print("=== 台灣警政統計分析報告 ===\n")
    
    # 基本統計
    print("1. 資料期間：{} - {}".format(int(df['西元年'].min()), int(df['西元年'].max())))
    print("2. 資料筆數：{} 年\n".format(len(df)))
    
    # 趨勢分析
    first_year = df.iloc[0]
    last_year = df.iloc[-1]
    
    print("=== 整體趨勢分析 ===")
    crime_change = ((last_year['全般刑案_發生數'] - first_year['全般刑案_發生數']) / first_year['全般刑案_發生數']) * 100
    solve_rate_change = last_year['全般刑案_破獲率'] - first_year['全般刑案_破獲率']
    
    print(f"• 全般刑案發生數變化：{crime_change:.1f}%")
    print(f"• 全般刑案破獲率變化：+{solve_rate_change:.1f}個百分點")
    print(f"• 2023年整體破獲率：{last_year['全般刑案_破獲率']:.1f}%")
    
    # 各類犯罪分析
    print(f"\n=== 2023年犯罪結構 ===")
    print(f"• 全般刑案發生數：{last_year['全般刑案_發生數']:,.0f} 件")
    print(f"• 暴力犯罪發生數：{last_year['暴力犯罪_發生數']:,.0f} 件 ({(last_year['暴力犯罪_發生數']/last_year['全般刑案_發生數']*100):.1f}%)")
    print(f"• 竊盜發生數：{last_year['竊盜_發生數']:,.0f} 件 ({(last_year['竊盜_發生數']/last_year['全般刑案_發生數']*100):.1f}%)")
    
    # 績效分析
    print(f"\n=== 破獲率表現 ===")
    print(f"• 全般刑案破獲率：{last_year['全般刑案_破獲率']:.1f}%")
    print(f"• 暴力犯罪破獲率：{last_year['暴力犯罪_破獲率']:.1f}%")
    print(f"• 竊盜破獲率：{last_year['竊盜_破獲率']:.1f}%")
    
    # 犯罪率分析
    print(f"\n=== 犯罪率分析 (件/十萬人口) ===")
    print(f"• 全般刑案犯罪率：{last_year['全般刑案_犯罪率']:.1f}")
    print(f"• 暴力犯罪犯罪率：{last_year['暴力犯罪_犯罪率']:.1f}")
    print(f"• 竊盜犯罪率：{last_year['竊盜_犯罪率']:.1f}")

def main():
    """主程式"""
    filename = "主要警政統計指標1V.csv"
    
    try:
        # 載入資料
        print("正在載入資料...")
        df = load_and_clean_data(filename)
        
        # 生成統計報告
        generate_summary_report(df)
        
        # 建立視覺化圖表
        print("\n正在生成視覺化圖表...")
        
        # 犯罪趨勢分析圖
        fig1 = create_crime_trend_analysis(df)
        plt.show()
        
        # 警政績效分析圖
        fig2 = create_performance_analysis(df)
        plt.show()
        
        print("\n分析完成！")
        
        # 可選：儲存圖表
        save_plots = input("\n是否要儲存圖表？(y/n): ").lower().strip()
        if save_plots == 'y':
            fig1.savefig('台灣警政統計趨勢分析.png', dpi=300, bbox_inches='tight')
            fig2.savefig('台灣警政績效分析.png', dpi=300, bbox_inches='tight')
            print("圖表已儲存！")
            
    except FileNotFoundError:
        print(f"錯誤：找不到檔案 '{filename}'")
        print("請確認檔案存在於當前目錄中")
    except Exception as e:
        print(f"發生錯誤：{str(e)}")

if __name__ == "__main__":
    main()