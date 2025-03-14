"""
PostgreSQL Data Visualization Script
This script connects to a PostgreSQL database, retrieves average cart prices for
users whose average price falls between $26 and $43, and visualizes the data
as a horizontal boxplot.
The script:
1. Establishes a connection to the PostgreSQL database using SQLAlchemy
2. Executes a SQL query to retrieve filtered cart price data
3. Creates a customized horizontal boxplot with the following features:
    - Notched boxplot for confidence interval visualization
    - Light blue colored boxes with black edges
    - Diamond-shaped markers for outliers
    - Customized whiskers (0.2 * IQR) (whiskers is the line that extends from the box to the highest and lowest value)
    - X-axis ticks at 2-unit intervals spanning the data range
Dependencies:
     - sqlalchemy: For database connectivity
     - pandas: For data manipulation and SQL query execution
     - matplotlib: For data visualization
     - numpy: For numerical operations and array manipulation
Database Schema:
     The query assumes a 'customers' table with columns:
     - user_id: Unique identifier for users
     - price: Numeric value representing cart prices
     - event_type: String categorizing the event (filtering for 'cart' events)
"""

import sqlalchemy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

try:
    # Create connection using SQLAlchemy
    connection = sqlalchemy.create_engine("postgresql://jvalenci:mysecretpassword@localhost:5432/piscineds")
    
    # Execute query directly using pandas

    data = pd.read_sql_query("""
        SELECT user_id, AVG(price) AS avg_cart_price
        FROM customers
        WHERE event_type = 'cart'
        GROUP BY user_id
        HAVING AVG(price) BETWEEN 26 AND 43;
    """, con=connection)

    print("Data has been fetched from the table.")
    
    # Extract avg_cart_price colum  values for plotting
    avg_cart_prices = data['avg_cart_price'].values.tolist()
    
    # Plotting the boxplot
    # (10, 6) is the size of the figure
    plt.figure(figsize=(10, 6))
    # boxplot() method creates the boxplot
    # vert=False makes the boxplot horizontal
    # widths=0.5 sets the width of the boxes
    plt.boxplot(avg_cart_prices, vert=False, widths=0.5,
                #boxprops is used to customize the appearance of the boxes 
                boxprops=dict(facecolor='lightblue', edgecolor='black'),
                # flierprops is used to customize the appearance of the outliers
                flierprops=dict(marker='D', markersize=8, markerfacecolor='lightgray', markeredgecolor='none'),
                patch_artist=True, whis=0.2)
    #np.arange is used to set the x-axis ticks at 2-unit intervals
    plt.xticks(np.arange(int(min(avg_cart_prices)), int(max(avg_cart_prices)) + 1, step=2))
    plt.tight_layout()
    # xlim() is used to set the x-axis limits
    # min(avg_cart_prices) - 1 and max(avg_cart_prices) + 1 are the lower and upper limits
    plt.xlim(min(avg_cart_prices) - 1, max(avg_cart_prices) + 1)
    plt.yticks([])
    plt.show()
except Exception as e:
    print(f"Error: {e}")
