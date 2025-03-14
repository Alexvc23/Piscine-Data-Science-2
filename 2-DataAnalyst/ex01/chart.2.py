
# !Generates a chart displaying the average daily spending per customer over time.
# This script connects to a PostgreSQL database, retrieves customer purchase data,
# ?calculates the average spend per customer for each day, and plots the results
# as a time series chart with shaded area below the line.
# !The average spending is calculated by taking the total daily sales amount,
# !applying an 80% reduction factor, and dividing by the number of unique
# !customers who made purchases that day.
# Database fields used:
# - user_id: Customer identifier
# - event_time: Timestamp of purchase event
# - event_type: Type of event (only 'purchase' events are considered)
# - price: Purchase amount

# ?The chart shows data from approximately October to January with the y-axis
# ?representing average spend per customer in some currency unit (A).

import psycopg2
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

dbname = "piscineds"
user = "jvalenci"
password = "mysecretpassword"
host = "localhost"
port = "5432"

try:
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    sql_query = """
        SELECT user_id, event_time, event_type, price
        FROM customers
        ORDER BY event_time;
    """

    print("Connected to PostgreSQL!")
    cursor = conn.cursor()
    cursor.execute(sql_query)
    print("SQL script executed successfully!")
    data = cursor.fetchall()
    print("Data has been fetched from the table.")
    conn.commit()
    cursor.close()
    conn.close()
    
    daily_sales = defaultdict(float)
    unique_customers = defaultdict(set)
    
    # Loop through the data and count the number of purchases for each date
    for user_id, event_time, event_type, price in data:
        if event_type == 'purchase':
            date_str = event_time.strftime('%Y-%m-%d')
            daily_sales[date_str] += float(price)
            unique_customers[date_str].add(user_id)
    
    # Sort the dates in ascending order
    # keys() returns a list of all the keys in the dictionary
    dates = list(daily_sales.keys())
    
    # Calculate the average spend per customer for each date
    # e.g average_spend_per_customer = [daily_sales[date] * 0.8 / len(unique_customers[date]) for date in dates]
    # 0.8 is the reduction factor applied to the total daily sales amount
    # because the question asks for the average spend per customer to be 80% of the total daily sales amount to scale the data
    average_spend_per_customer = [daily_sales[date] * 0.8 / len(unique_customers[date])
                                  for date in dates]
    
    plt.figure(figsize=(10, 6))
    # Plot the average spend per customer as
    plt.plot(dates, average_spend_per_customer, color='blue', alpha=0.3)
    # Fill the area below the line
    plt.fill_between(dates, average_spend_per_customer, color='blue', alpha=0.3)
    plt.ylabel("Average Spend/Customer in A")
    # e.g tick_positions = [0, len(dates) // 4, 2 * len(dates) // 4, 3 * len(dates) // 4] 
    # e.g tick_positions = [0, 7, 14, 21] for 28 dates for Oct, Nov, Dec, Jan
    tick_positions = [0, len(dates) // 4, 2 * len(dates) // 4, 3 * len(dates) // 4]
    tick_labels = ["Oct", "Nov", "Dec", "Jan"]
    plt.xticks(tick_positions, tick_labels)
    # return a list of evenly spaced values from 0 to the maximum value of average_spend_per
    plt.yticks(np.arange(0, max(average_spend_per_customer), 5))
    # Set the x-axis limits to the first and last dates
    plt.xlim(dates[0], dates[-1])
    # Set the y-axis limits to 0 and the maximum value of average_spend_per_customer
    plt.ylim(0)
    plt.show()
except Exception as e:
    print(f"Error: {e}")
