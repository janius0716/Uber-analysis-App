import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('processed_uber_fares.csv')

# Set page title
st.title('Uber Fare Dataset Analysis App')
st.header('Basic Data Information')

# Question 1: What is the relationship between the number of passengers and fare amount?
st.header('Question 1: What is the relationship between the number of passengers and fare amount?')

# Filter component - select passenger count range
passenger_count_min = int(df['passenger_count'].min())
passenger_count_max = int(df['passenger_count'].max())
selected_passenger_count = st.slider('Select passenger count range', 
                                     passenger_count_min, passenger_count_max,
                                     (passenger_count_min, passenger_count_max))

# Filter data
filtered_df = df[(df['passenger_count'] >= selected_passenger_count[0]) &
                 (df['passenger_count'] <= selected_passenger_count[1])]

# Analyze relationship between passenger count and fare amount
grouped_data = filtered_df.groupby('passenger_count')['fare_amount'].mean().reset_index()

# Plot bar chart
plt.figure(figsize=(10, 6))
sns.barplot(x='passenger_count', y='fare_amount', data=grouped_data)
plt.title('Relationship between Number of Passengers and Average Fare Amount')
plt.xlabel('Number of Passengers')
plt.ylabel('Average Fare Amount')
st.pyplot(plt)

# Display analysis results
st.write(grouped_data)

# Question 2: How do different times of day affect fare amounts?
st.header('Question 2: How do different times of day affect fare amounts?')

# Convert pickup_datetime to datetime type
df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])

# Extract hour information
df['hour'] = df['pickup_datetime'].dt.hour

# Filter component - select time of day category
st.sidebar.header('Time of Day Category')
time_categories = {
    'Early Morning': range(0, 6),
    'Morning': range(6, 11),
    'Noon': range(11, 15),
    'Afternoon': range(15, 19),
    'Evening': range(19, 24)
}
selected_category = st.sidebar.radio('Select Time Category', list(time_categories.keys()))

# Get selected hours
selected_hours = time_categories[selected_category]

# Filter component - input hour range
hour_min = int(df['hour'].min())
hour_max = int(df['hour'].max())
selected_hour = st.slider('Select hour range', hour_min, hour_max, (hour_min, hour_max))

# Filter data
filtered_df_hour = df[
    df['hour'].isin(selected_hours) &
    (df['hour'] >= selected_hour[0]) & 
    (df['hour'] <= selected_hour[1])
    ]

# Analyze average fare amount at different times
hourly_avg_fare = filtered_df_hour.groupby('hour')['fare_amount'].mean().reset_index()

# Plot line chart
plt.figure(figsize=(10, 6))
sns.lineplot(x='hour', y='fare_amount', data=hourly_avg_fare, marker='o')
plt.title('Average Fare Amount at Different Times of Day')
plt.xlabel('Hour')
plt.ylabel('Average Fare Amount')
st.pyplot(plt)

# Display analysis results
st.write(hourly_avg_fare)

# Exploratory Data Analysis (EDA) - Fare amount distribution (histogram)
st.header('Exploratory Data Analysis (EDA) - Fare Amount Distribution (Histogram)')

# Filter component - select fare amount category
st.sidebar.header('Fare Amount Category')
fare_categories = {
    'Cheap': lambda x: x < 15,
    'Medium': lambda x: (x >= 15) & (x <= 50),
    'Expensive': lambda x: x > 50
    }
selected_category = st.sidebar.radio(
    'Select Fare Category', 
    list(fare_categories.keys())
    )

# Filter data
filter_func = fare_categories[selected_category]
filtered_fares = df[df['fare_amount'].apply(filter_func)]

# Plot histogram
plt.figure(figsize=(10, 6))
sns.histplot(filtered_fares['fare_amount'], bins=30, kde=True)
plt.title('Fare Amount Distribution')
plt.xlabel('Fare Amount')
plt.xticks(rotation=45)
plt.ylabel('Frequency')
st.pyplot(plt)

# Exploratory Data Analysis (EDA) - Passenger count distribution (bar chart)
st.header('Exploratory Data Analysis (EDA) - Passenger Count Distribution (Bar Chart)')
plt.figure(figsize=(10, 6))
sns.countplot(x='passenger_count', data=df)
plt.title('Passenger Count Distribution')
plt.xlabel('Number of Passengers')
plt.ylabel('Frequency')
st.pyplot(plt)