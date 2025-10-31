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

# 主函数
def main():
    st.title("Uber车费数据处理")
    
    # 加载并处理数据
    df = load_and_process_data()
    
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