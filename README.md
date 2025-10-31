# Uber-analysis-App
## 1. Team members
- Zhijia Zhou
- Shuyu Zhang

## 2. Reasons for choosing the data set
- (1) Nearly all of us have experience using ride-hailing or food delivery platforms,allowing us to intuitively understand the process of "user placing an order → driver accepting the order → trip completion" without spending extra time learning the business logic of an unfamiliar industry.
- (2) Clear research questions: The problems of Uber’s business, such as poor data quality, inefficient dispatching, and privacy breach risks are real-world issues which are worth focusing and analyzing. This prevents vague, empty conclusions and aligns with the core academic requirements.

## 3. Questions
- Question1：What is the relationship between the number of passengers and fare amount?

  We created a chart presenting the relationship between Uber's fare amounts and passenger counts. 

  For 1 passenger, the fare is 11.1061. With 2 passengers, it rises to 11.5367, then drops slightly to 11.3936 for 3 passengers. A notable increase occurs when there are 4 passengers, with the fare jumping to 13.3985. For 5 passengers, it decreases to 12.6485, and for 6 passengers, it is 11.7999. 

  In terms of commercial value, this data helps Uber optimize pricing strategies. It can adjust fares based on passenger count to balance supply and demand, maximizing revenue—for example, setting higher fares for 4 passengers to reflect increased resource usage. For drivers, it provides insights into potential earnings across different passenger loads, aiding in trip acceptance decisions. For riders, it offers transparency, allowing them to anticipate costs based on group size, which can inform travel planning and budgeting. Additionally, this data supports market analysis, helping Uber identify trends in passenger group sizes and tailor services, such as promoting rides for specific group sizes with targeted offers, to enhance user experience and business profitability.

- Question2: How do different times of day affect fare amounts?

  We developed a chart illustrating the variation of Uber fare amounts across different hours of a day. As shown in the chart, the Uber fares exhibit significant fluctuations throughout the day, with the peak at 5 AM and the lowest point at 6 PM.

  Starting from midnight (hour 0), the fare stands at 10.9292. It rises slightly to 11.46 at 1 AM, then decreases to 11.2975 at 2 AM. A steady increase follows, with the fare reaching 12.0973 at 3 AM and 12.9416 at 4 AM. There is a notable surge at 5 AM, where the fare jumps to 15.9602, the highest point in the observed period.
  Subsequently, the fare drops significantly to 9.9742 at 6 PM (hour 19), then climbs back to 12.0668 at 7 PM (hour 20). At 8 PM (hour 21), it decreases to 10.9415, similar to the midnight fare. It increases again to 12.0948 at 9 PM (hour 22) and finally settles at 11.9 (partially visible) at 10 PM (hour 23).

## 4. Interactive Plots Explanation
- chart1：Relationship between Number of Passengers and Average Fare Amount
- chart2：Average Fare Amount at Different Times of Day
- chart3：Exploratory Data Analysis (EDA) - Fare Amount Distribution (Histogram)
- chart4: Exploratory Data Analysis (EDA) - Passenger Count Distribution (Bar Chart)

## 5. Variables Explanation
- number of passengers
- hour
- fare amount
- average fare amount
- frequency: order quantity corresponding to different price ranges and passenger count ranges

## 6. Interactive Widgets Description
- widget1：Time Range Slider: Filter Data for a Specific Time Period
  
  description: The slider is in the range of 24 hours. When the slider moves from 0 to 23, the line chart shows different average fare amount.

- widget2: Passengers Count Range Slider
  
  description: The slider is in range of one to six because the capacity of the Uber car is 6 people. When the slider moves from 1 to 6, the histogram demonstrates different average fare amount.

- widget3：Multi Select: Time of Day Category
  
  description: we categorized the whole day into four parts --- early morning(0 am to 5 am), morning(6 am to 11 am), noon(12 pm to 2 pm), afternoon(3 pm to 6 pm), and evening(7 pm to 24 am) respectively. The line chart presents different average fare amount.

- widget4: Multi Select: Fare Amount Category
  
  description: we categorized the fare amount into three parts --- cheap(lower than 15), medium(between 15 to 50), and expensive(more than 50) respectively. The chart reveals different frequencies.

## 7. Links
- Streamlit app：https://uber-analysis-app-k6fkkpkwh4z45ygwuuokfq.streamlit.app/
- GitHub repo：https://github.com/janius0716/Uber-analysis-App#

