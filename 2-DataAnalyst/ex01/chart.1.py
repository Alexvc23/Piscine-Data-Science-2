# A script to connect to a PostgreSQL database, retrieve customer purchase data, and create 
    # a monthly sales bar chart.
# !3. Processes the data to calculate total monthly sales
# ?4. Creates a bar chart showing sales trends over a 4-month period (Oct-Jan)
# ?5. Displays the sales in Altairian Dollars (with an apparent 20% reduction applied)

import psycopg2
from datetime import datetime
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
    print("Connected to PostgreSQL!")
    cursor = conn.cursor()

    # Direct SQL query instead of importing from file
    sql_query = """
    SELECT event_time, event_type, price
    FROM customers;
    """

    cursor.execute(sql_query)
    print("SQL script executed successfully!")
    data = cursor.fetchall()
    print("Data has been fetched from the table.")
    conn.commit()
    cursor.close()
    conn.close()
    
    # Initialize a dictionary to store total monthly sales
    # e.g. {'Oct': 1000.0, 'Nov': 2000.0, 'Dec': 1500.0, 'Jan': 3000.0}
    monthly_sales = defaultdict(float)
    
    # Calculate total monthly sales
    for event_time, event_type, price in data:
        # Check if the event type is a purchase
        if event_type == 'purchase':
            # Extract the year, month, and day from the event time
            year, month, day = event_time.year, event_time.month, event_time.day
            # Format the month as a 3-letter string
            month_str = datetime(year, month, 1).strftime('%b')
            # Add the price to the total sales for the month
            monthly_sales[month_str] += float(price)
    
    months = ['Oct', 'Nov', 'Dec', 'Jan']
    # Apply an 80% reduction to the monthly sales
    # in order to display the sales in Altairian Dollars
    # e.g [800.0, 1600.0, 1200.0, 2400.0]
    sales = [monthly_sales[month] * 0.8 for month in months]
    
    plt.figure(figsize=(10, 6))
    plt.bar(months, sales)
    plt.ylabel("Total Sales (in Altairian Dollars)")
    plt.show()
except Exception as e:
    print(f"Error: {e}")
