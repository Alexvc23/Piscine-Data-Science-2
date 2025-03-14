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
    
    monthly_sales = defaultdict(float)
    
    for event_time, event_type, price in data:
        if event_type == 'purchase':
            year, month, day = event_time.year, event_time.month, event_time.day
            month_str = datetime(year, month, 1).strftime('%b')
            monthly_sales[month_str] += float(price)
    
    months = ['Oct', 'Nov', 'Dec', 'Jan']
    sales = [monthly_sales[month] * 0.8 for month in months]
    
    plt.figure(figsize=(10, 6))
    plt.bar(months, sales)
    plt.ylabel("Total Sales (in Altairian Dollars)")
    plt.show()
except Exception as e:
    print(f"Error: {e}")
