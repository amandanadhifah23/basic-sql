import streamlit as st
import pandas as pd
import sqlite3
from sqlalchemy import create_engine, text
import plotly.express as px

# Set the page configuration
st.set_page_config(page_title="Sales Trends Analysis", initial_sidebar_state="expanded")


# Database connection
db_path = "sales.db"  # Replace with your database path
conn_string = f"sqlite:///{db_path}"
engine = create_engine(conn_string)
conn = engine.connect()

def execute_query(query):
    result = conn.execute(text(query))
    columns = result.keys()
    return pd.DataFrame(result.fetchall(), columns=columns)

# Header dan Sub-Header untuk deskripsi analisis
st.title("Sales Trends Analysis")
st.write("""
**Analysis Goal:** Analyze sales trends to understand sales performance over time, 
identify peak sales periods, and gain insights for better decision-making.
""")

st.header("Datasets Customers")
customers = """
SELECT *
FROM customers
"""
customers_df = execute_query(customers)
st.write(customers_df)

st.header("Datasets Orders")
orders = """
SELECT *
FROM orders
"""
orders_df = execute_query(orders)
st.write(orders_df)

# Analysis 1: Top Customers
st.header("Identify top customers based on total sales and their contribution to overall revenue.")
st.write("**Analysis Goal:** Identify top customers based on total sales and their contribution to overall revenue.")
top_customers_query = """
SELECT c.Customer_ID, SUM(o.Sales) as Total_Sales,
(SUM(o.Sales) / (SELECT SUM(Sales) FROM orders)) * 100 as Contribution_Percentage
FROM orders o
JOIN customers c ON o.Customer_ID = c.Customer_ID
GROUP BY c.Customer_ID
ORDER BY Total_Sales DESC
LIMIT 10
"""
top_customers_df = execute_query(top_customers_query)
st.write(top_customers_df)
st.write("**Analysis Result:** The top ten customers collectively contribute significantly to the revenue, each contributing more than 11% individually, showcasing their importance in the overall sales strategy and revenue generation for the company. ")

# Analysis 2: Monthly Sales Trends
st.header("Analyze monthly sales trends and identify peak sales periods.")
st.write("**Analysis Goal:** Analyze monthly sales trends and identify peak sales periods.")
monthly_sales_query = """
SELECT STRFTIME('%Y-%m', 
    SUBSTR(Order_Date, 7, 4) || '-' || SUBSTR(Order_Date, 1, 2) || '-' || SUBSTR(Order_Date, 4, 2)) AS Month,
    SUM(Sales) AS Total_Sales
FROM orders
WHERE LENGTH(Order_Date) = 10
    AND SUBSTR(Order_Date, 7, 4) BETWEEN '1000' AND '9999'
    AND SUBSTR(Order_Date, 1, 2) BETWEEN '01' AND '12'
    AND SUBSTR(Order_Date, 4, 2) BETWEEN '01' AND '31'
GROUP BY Month
ORDER BY Month;
"""
monthly_sales_df = execute_query(monthly_sales_query)
st.write(monthly_sales_df)
st.write("**Analysis Result:** The total sales show a general increase each year during the October to December period, indicating a potential seasonality effect where sales peak towards the end of the year. Specifically, the highest sales recorded are in November 2020 with 79,834.192, showing a significant jump compared to previous years. December also consistently shows strong sales figures, peaking at 63,025.012 in 2019. However, there is a noticeable drop in December 2020 to 47,009.7178, which could indicate a specific event or market condition affecting sales. Overall, the data highlights a trend of increasing total sales year-over-year with notable peaks in November and December, suggesting these months are critical for maximizing revenue.")

# Analysis 3: Most Profitable Product Categories and Sub-Categories
st.header("Determine the most profitable product categories and sub-categories.")
st.write("**Analysis Goal:** Determine the most profitable product categories and sub-categories.")
profitable_categories_query = """
SELECT Category, Sub_Category, SUM(Profit) as Total_Profit
FROM orders
WHERE Category IS NOT NULL AND Category != '' 
    AND Sub_Category IS NOT NULL AND Sub_Category != ''
    AND Category != 'Category' AND Sub_Category != 'Sub_Category'
GROUP BY Category, Sub_Category
ORDER BY Total_Profit DESC
"""
profitable_categories_df = execute_query(profitable_categories_query)
st.write(profitable_categories_df)
st.write("**Analysis Result:** Technology items such as Copiers, Phones, and Accessories are the most profitable, with Copiers leading at 55,617.82. Office Supplies also show significant profit, especially in Paper and Binders. However, certain Furniture items, specifically Tables and Bookcases, are resulting in losses with -17,725.48 and -3,472.56 respectively. Other Office Supplies such as Supplies also show a minor loss of -1,189.10. This indicates that while technology and some office supplies are driving profits, certain furniture items are negatively impacting the overall profitability. The business may need to reassess their strategy regarding these loss-making items.")

# Analysis 4: Impact of Shipping Mode on Profitability
st.header("Assess the impact of shipping mode on order profitability.")
st.write("**Analysis Goal:** Assess the impact of shipping mode on order profitability.")
shipping_mode_profit_query = """
SELECT Ship_Mode, SUM(Sales) as Total_Sales, SUM(Profit) as Total_Profit
FROM orders
WHERE Ship_Mode != 'Ship_Mode'
GROUP BY Ship_Mode
ORDER BY Total_Profit DESC
"""
shipping_mode_profit_df = execute_query(shipping_mode_profit_query)
st.write(shipping_mode_profit_df)
st.write("**Analysis Result:** . Companies can optimize logistics and shipping strategies by leveraging the most profitable shipping modes while considering customer preferences and delivery time requirements. Evaluation of how different shipping modes affect sales and profitability, also helping optimize logistics and shipping.")

# Analysis 5: Regional Performance
st.header("Evaluate regional performance by comparing sales, profit, and order quantity across regions.")
st.write("**Analysis Goal:** Evaluate regional performance by comparing sales, profit, and order quantity across regions.")
regional_performance_query = """
SELECT Country, Region, SUM(Sales) as Total_Sales, SUM(Profit) as Total_Profit, COUNT(Order_ID) as Total_Orders
FROM orders
WHERE Country != 'Country'
GROUP BY Country, Region
ORDER BY Total_Sales DESC
"""
regional_performance_df = execute_query(regional_performance_query)
st.write(regional_performance_df)
st.write("**Analysis Result:** Regional performance comparison, providing insights into regional strengths and areas needing improvement.")

# Analysis 6: Customer Segmentation
st.header("Segment customers based on their purchasing behavior.")
st.write("**Analysis Goal:** Segment customers based on their purchasing behavior to tailor marketing strategies.")
customer_segmentation_query = """
SELECT c.Segment, SUM(o.Sales) as Total_Sales, AVG(o.Sales) as Average_Sales, SUM(o.Profit) as Total_Profit, COUNT(o.Order_ID) as Total_Orders
FROM orders o
JOIN customers c ON o.Customer_ID = c.Customer_ID
GROUP BY c.Segment
ORDER BY Total_Sales DESC
"""
customer_segmentation_df = execute_query(customer_segmentation_query)
st.write(customer_segmentation_df)
st.write("**Analysis Result:** Insights into customer segments and their purchasing behavior, aiding in targeted marketing.")

# Analysis 7: Discount Impact on Sales and Profit
st.header("Analyze the impact of discounts on sales and profit.")
st.write("**Analysis Goal:** Analyze the impact of discounts on sales and profit to determine optimal discounting strategies.")
discount_impact_query = """
SELECT Discount, SUM(Sales) as Total_Sales, SUM(Profit) as Total_Profit
FROM orders
WHERE Discount != 'Discount'
GROUP BY Discount
ORDER BY Discount
"""
discount_impact_df = execute_query(discount_impact_query)
st.write(discount_impact_df)
st.write("**Analysis Result:** The correlation analysis reveals that there is a weak negative correlation between discount and total sales, indicating that increasing discounts slightly decreases total sales. However, there is a strong negative correlation between discount and total profit, suggesting that higher discounts significantly reduce total profit. This indicates that while discounts may not drastically affect sales volume, they have a substantial negative impact on profitability.")

# Analysis 8: Product Sales Performance Over Time
st.header("Track sales performance of individual products over time.")
st.write("**Analysis Goal:** Track sales performance of individual products over time to identify trends and opportunities.")
product_sales_over_time_query = """
SELECT Product_ID, Product_Name, SUM(Sales) AS Total_Sales
FROM orders
GROUP BY Product_ID, Product_Name
ORDER BY Total_Sales DESC
LIMIT 10
"""
product_sales_over_time_df = execute_query(product_sales_over_time_query)
st.write(product_sales_over_time_df)
st.write("**Analysis Result:** Product sales trends over time, highlighting high-performing products.")

# Analysis 9: Correlation Between Order Quantity and Profit
st.header("Examine the correlation between order quantity and profit.")
st.write("**Analysis Goal:** Examine the correlation between order quantity and profit to identify optimal order sizes.")
quantity_profit_correlation_query = """
SELECT Quantity, AVG(Profit) as Avg_Profit
FROM orders
WHERE Quantity != 'Quantity'
GROUP BY Quantity
ORDER BY Quantity
"""
quantity_profit_correlation_df = execute_query(quantity_profit_correlation_query)
st.write(quantity_profit_correlation_df)
st.write("**Analysis Result:** Insights into how order quantities relate to profitability, aiding in inventory and sales strategy.")

# Analysis 10: Customer Lifetime Value (CLV)
st.header("Calculate the Customer Lifetime Value (CLV) for key customers.")
st.write("**Analysis Goal:** Calculate the Customer Lifetime Value (CLV) for key customers to prioritize long-term relationships.")
customer_lifetime_value_query = """
SELECT c.Customer_ID, SUM(o.Sales) as Total_Sales, SUM(o.Profit) as Total_Profit,
    (SUM(o.Sales) - SUM(o.Profit)) / COUNT(o.Order_ID) as Avg_Order_Value
FROM orders o
JOIN customers c ON o.Customer_ID = c.Customer_ID
GROUP BY c.Customer_ID
ORDER BY Avg_Order_Value DESC
LIMIT 10
"""
customer_lifetime_value_df = execute_query(customer_lifetime_value_query)
st.write(customer_lifetime_value_df)
st.write("**Analysis Result:** Calculation of CLV for top customers, helping prioritize efforts on high-value relationships.")

# Close the connection
conn.close()