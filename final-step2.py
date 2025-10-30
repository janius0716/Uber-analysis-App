import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# 设置中文字体显示
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
sns.set(font_scale=1.2)
sns.set_style("whitegrid")

# 缓存数据加载函数（使用streamlit缓存优化性能）
@st.cache_data
def load_and_process_data(file_path='D:/MISY225/app/uber.csv', sample_size=5000):
    """加载并处理Uber车费数据集"""
    # 1. 加载数据
    df = pd.read_csv(file_path)
    
    # 2. 数据基本信息展示
    st.subheader("1. 数据集基本信息")
    st.write(f"原始数据集形状: {df.shape[0]}行, {df.shape[1]}列")
    st.write(f"采样后数据集形状: {sample_size}行, {df.shape[1]}列")
    
    # 3. 数据采样（确保不超过原始数据量）
    sample_size = min(sample_size, df.shape[0])
    df_sampled = df.sample(sample_size, random_state=42)  # 固定随机种子确保可复现
    
    # 4. 数据清洗
    st.subheader("2. 数据清洗")
    
    # 4.1 缺失值处理
    missing_values = df_sampled.isnull().sum()
    st.write("缺失值统计:")
    st.dataframe(missing_values[missing_values > 0].to_frame(name="缺失值数量"))
    
    # 移除包含缺失值的行（对于这个数据集更合理）
    df_cleaned = df_sampled.dropna()
    st.write(f"清洗后数据量: {df_cleaned.shape[0]}行")
    
    # 4.2 数据类型转换
    # 将日期列转换为datetime类型
    df_cleaned['pickup_datetime'] = pd.to_datetime(df_cleaned['pickup_datetime'])
    
    # 4.3 异常值处理（基于业务逻辑）
    # 移除 fare_amount 为负数或0的记录
    df_cleaned = df_cleaned[df_cleaned['fare_amount'] > 0]
    # 移除乘客数量为0的记录
    df_cleaned = df_cleaned[df_cleaned['passenger_count'] > 0]
    # 移除经纬度异常值（基于纽约大致经纬度范围）
    df_cleaned = df_cleaned[
        (df_cleaned['pickup_latitude'].between(40.4, 41.0)) &
        (df_cleaned['pickup_longitude'].between(-74.3, -73.7)) &
        (df_cleaned['dropoff_latitude'].between(40.4, 41.0)) &
        (df_cleaned['dropoff_longitude'].between(-74.3, -73.7))
    ]
    
    st.write(f"异常值处理后数据量: {df_cleaned.shape[0]}行")
    
    return df_cleaned

# 数据探索函数（必须放在 load_and_process_data() 之后、main() 之前）
def explore_data(df):
    """详细探索数据集特征"""
    st.subheader("3. 数据集详细描述")
    
    # 3.1 数据概览
    st.write("数据前5行:")
    st.dataframe(df.head())
    
    # 3.2 数值特征统计描述
    st.write("数值特征统计描述:")
    st.dataframe(df.describe())
    
    # 3.3 特征相关性分析
    st.write("3.3 特征相关性分析")
    numeric_df = df.select_dtypes(include=[np.number])
    corr = numeric_df.corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('特征相关性热力图')
    st.pyplot(plt)
    plt.close()
    
    # 3.4 关键特征分布分析
    st.subheader("4. 关键特征分布")
    
    # 4.1 车费金额分布
    plt.figure(figsize=(10, 6))
    sns.histplot(df['fare_amount'], kde=True, bins=30)
    plt.title('车费金额分布')
    plt.xlabel('车费金额($)')
    st.pyplot(plt)
    plt.close()
    
    # 4.2 乘客数量分布
    plt.figure(figsize=(10, 6))
    sns.countplot(x='passenger_count', data=df)
    plt.title('乘客数量分布')
    plt.xlabel('乘客数量')
    st.pyplot(plt)
    plt.close()
    
    # 4.3 时间特征分析
    df['hour'] = df['pickup_datetime'].dt.hour
    df['day_of_week'] = df['pickup_datetime'].dt.dayofweek  # 0=周一, 6=周日
    
    plt.figure(figsize=(12, 5))
    sns.boxplot(x='hour', y='fare_amount', data=df)
    plt.title('不同时段的车费分布')
    plt.xlabel('小时')
    plt.ylabel('车费金额($)')
    st.pyplot(plt)
    plt.close()
    
    # 4.4 地理分布简单展示（已解决列名问题）
    st.write("4.4 上下车地点经纬度分布")
    sample_data = df[['pickup_latitude', 'pickup_longitude']].sample(1000)
    sample_data = sample_data.rename(columns={
        'pickup_latitude': 'latitude',
        'pickup_longitude': 'longitude'
    })
    st.map(sample_data)
# 商业价值分析
def business_value_analysis(df):
    """分析数据集的商业价值"""
    st.subheader("5. 商业价值分析")
    
    # 5.1 高峰时段分析
    hourly_avg_fare = df.groupby('hour')['fare_amount'].mean().reset_index()
    peak_hour = hourly_avg_fare.loc[hourly_avg_fare['fare_amount'].idxmax()]
    
    st.write(f"• 车费最高的时段: {int(peak_hour['hour'])}点，平均车费: ${peak_hour['fare_amount']:.2f}")
    
    # 5.2 乘客数量与车费关系
    passenger_fare = df.groupby('passenger_count')['fare_amount'].mean().reset_index()
    st.write("• 不同乘客数量的平均车费:")
    st.dataframe(passenger_fare.rename(columns={
        'passenger_count': '乘客数量', 
        'fare_amount': '平均车费($)'
    }).round(2))
    
    # 5.3 潜在商业应用
    st.write("""
    • 商业应用1: 动态定价策略 - 基于高峰时段调整价格，最大化收益  
    • 商业应用2: 车辆调度优化 - 根据上下车热点区域合理分配车辆  
    • 商业应用3: 市场细分 - 针对不同乘客数量的群体设计差异化服务  
    • 商业应用4: 路线规划优化 - 分析高频路线，优化司机导航
    """)

# 主函数
def main():
    st.title("Uber车费数据集分析与处理")
    
    # 加载并处理数据
    df = load_and_process_data()
    
    # 数据探索
    explore_data(df)
    
    # 商业价值分析
    business_value_analysis(df)
    
    # 提供清洗后的数据集下载
    st.subheader("6. 数据下载")
    csv = df.to_csv(index=False)
    st.download_button(
        label="下载处理后的CSV文件",
        data=csv,
        file_name="processed_uber_fares.csv",
        mime="text/csv",
    )

if __name__ == "__main__":
    main()