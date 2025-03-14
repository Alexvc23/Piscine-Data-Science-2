import psycopg2
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


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

    # Direct SQL query instead of importing from file
    sql_query = """
        SELECT event_time, event_type
        FROM customers;
    """

    print("Connected to postgres!")
    cursor = conn.cursor()
    cursor.execute(sql_query)
    print("SQL script executed successfully!")
    data = cursor.fetchall()
    print("Data has been fetched from the table.")
    conn.commit()
    cursor.close()
    conn.close()

    # e.g purchase_counts = {'2022-11-15': 6855, '2023-01-08': 7601, '2023-01-07': 7561, '2023-01-22': 9081}
    purchase_counts = {}
    
    # Loop through the data and count the number of purchases for each date
    for event_time, event_type in data:
        if event_type == 'purchase':
            # Extract the year, month, and day from the event_time
            year, month, day = event_time.year, event_time.month, event_time.day
            date = datetime(year, month, day)
            # Format the date as a string
            date_str = date.strftime('%Y-%m-%d')
            # !Check if the month is between October and January
            if month >= 10 or month <= 1:
                # If the date is not in the dictionary, add it with a count of 0
                if date_str not in purchase_counts:
                    # e.g purchase_counts = {'2022-11-15': 0, '2023-01-08': 0, '2023-01-07': 0, '2023-01-22': 0}
                    purchase_counts[date_str] = 0
                # Increment the count for the date
                # because the date is in the dictionary
                # e.g purchase_counts = {'2022-11-15': 1, '2023-01-08': 1, '2023-01-07': 1, '2023-01-22': 1}
                purchase_counts[date_str] += 1

    # Sort the dates in ascending order
    sorted_counts = sorted(purchase_counts.items())
    # Unzip the sorted dates and counts
    # e.g dates = ['2022-11-15', '2023-01-07', '2023-01-08', '2023-01-22'], counts = [1, 1, 1, 1]
    dates, counts = zip(*sorted_counts)
    
    plt.figure(figsize=(12, 8))
    plt.grid(True, color='white', linestyle='--', linewidth=0.8, alpha=0.7)
    # Set the background color of the plot to lightgray
    plt.gca().set_facecolor('#e6e6e6')
    plt.plot(dates, counts, linestyle='-')
    plt.ylabel("Number of customers")
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{int(x / 10)}'))
    tick_positions = [0, len(dates) // 4, 2 * len(dates) // 4, 3 * len(dates) // 4]
    tick_labels = ["Oct", "Nov", "Dec", "Jan"]
    plt.xticks(tick_positions, tick_labels)
    plt.xlim(dates[0], dates[-1])
    plt.show()
except Exception as e:
    print(f"Error: {e}")