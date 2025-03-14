import psycopg2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


dbname = "piscineds"
user = "jvalenci"
password = "mysecretpassword"
host = "localhost"
port = "5432"

try:
    with open("ex04/elbow.sql", "r") as sql_file:
        sql_script = sql_file.read()
    print("SQL code has been imported!")
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    print("Connected to PostgreSQL!")
    cursor = conn.cursor()
    cursor.execute(sql_script)
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
