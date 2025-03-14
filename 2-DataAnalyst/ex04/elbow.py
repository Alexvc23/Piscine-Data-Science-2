
# Elbow Method for K-Means Clustering

# This script connects to a PostgreSQL database, extracts purchase data, and applies
# the Elbow method to determine the optimal number of clusters for K-means clustering.

# The script:
# 1. Connects to a PostgreSQL database using provided credentials
# 2. Executes a SQL query to get user purchase counts (limited to <30 purchases)
# 3. Applies K-means clustering with varying numbers of clusters (1-9)
# 4. Calculates Within-Cluster Sum of Squares (WSS) for each cluster configuration
# 5. Plots the WSS values against number of clusters to identify the "elbow point"
#     which suggests the optimal number of clusters

# Database Requirements:
# - PostgreSQL database named "piscineds"
# - Table "customers" with columns:
#   - user_id
#   - event_type (containing 'purchase' events)

# Dependencies:
# - psycopg2
# - matplotlib
# - sklearn.cluster (KMeans)

import psycopg2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


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
        SELECT user_id, COUNT(*) AS purchases
        FROM customers
        WHERE event_type = 'purchase'
        GROUP BY user_id
        HAVING COUNT(*) < 30
        ORDER BY purchases DESC;
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

    # Initialize an empty list to store Within-Cluster Sum of Squares (WSS) values
    # squared (wss) is a common abbreviation for Within-Cluster Sum of Squares
    wss = []
    # Loop through different numbers of clusters from 1 to 9
    # 10 beacasue the range function is exclusive of the last number
    for k in range(1, 10):
        # Create and fit KMeans model with k clusters
        # random_state=0 ensures reproducibility
        # n_init=10 means algorithm runs 10 times with different initializations
        # n_clusters=k means the number of clusters is k
        # ramdom_state=0 means the random number generator is initialized with 0
        kmeans = KMeans(n_clusters=k, random_state=0, n_init=10).fit(data)
        # Calculate and store the inertia (sum of squared distances to nearest centroid)

        # inertia_ is a property of the KMeans model that returns 
        # the sum of squared distances of samples to their closest cluster center
        wss.append(kmeans.inertia_)

    # x-axis: number of clusters
    # y-axis
    plt.plot(range(1, 10), wss)
    plt.xlabel("Number of clusters")
    plt.title("The Elbow Method")
    plt.show()
except Exception as e:
    print(f"Error: {e}")