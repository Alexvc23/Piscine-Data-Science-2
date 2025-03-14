import psycopg2
import matplotlib.pyplot as plt

dbname = "piscineds"
user = "jvalenci"
password = "mysecretpassword"
host = "localhost"
port = "5432"

try:
    with open("ex03/Building.sql", "r") as sql_file:
        sql_script1 = sql_file.read()
    with open("ex03/Building.1.sql", "r") as sql_file:
        sql_script2 = sql_file.read()
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
    cursor.execute(sql_script1)
    print("SQL script 1 executed successfully!")
    # SELECT user_id, COUNT(*)
    # FROM customers
    # WHERE event_type = 'purchase'
    # GROUP BY user_id

    # Number of purchases per customer 
    data_frequency = cursor.fetchall()
    cursor.execute(sql_script2)
    
    # SELECT user_id, SUM(price)
    # FROM customers
    # WHERE event_type = 'purchase'
    # GROUP BY user_id
    # HAVING SUM(price) < 225;

    print("SQL script 2 executed successfully!")
    # Total purchase amount per customer lower than 225
    data_monetary = cursor.fetchall()
    print("Data has been fetched from the table.")
    conn.commit()
    cursor.close()
    conn.close()

    print(data_frequency[:5])  # Print first 5 rows
    print(data_monetary[:5])   # Print first 5 rows
    # data_frequency: [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]
    # data_monetary: [(1, 50), (2, 50), (3, 50), (4, 50), (5, 50)]
    # Extract the frequency and monetary values from the data
    # Filter out the customers with a frequency higher than 40
    frequency = [row[1] for row in data_frequency if row[1] <= 40]
    # Filter out the customers with a monetary value higher than 225
    monetary = [row[1] for row in data_monetary]

    # fig is the figure object, and axs is an array of axes objects
    # (1,2) means that we want to create a 1(row)x2(cols) grid of plots
    # figsize=(15, 6) means that the figure will be 15 units wide and 6 units tall
    fig, axs = plt.subplots(1, 2, figsize=(15, 6))

    # zorder is the order of the grid lines -1 means that the grid lines will be behind the bars
    axs[0].grid(True, zorder=-1)
    # .hist() creates a histogram
    # bins=5 means that we want to create 5 bins(5 bars)
    # edgecolor='k' means that the edges of the bars will be black
    axs[0].hist(frequency, bins=5, edgecolor='k')
    # Set the labels and title for the first plot
    axs[0].set_ylabel('customers')
    # xlabel is the label for the x-axis 
    axs[0].set_xlabel('frequency')
    # set_xticks() sets the ticks on the x-axis
    axs[0].set_xticks(range(0, 39, 10))
    # set_yticks() sets the ticks on the y-axis
    axs[0].set_ylim(0, 60000)
    axs[0].set_title('Frequency distribution of the number of orders per customer')

    axs[1].grid(True, zorder=-1)
    axs[1].hist(monetary, bins=5, edgecolor='k')
    axs[1].set_ylabel('Count of customers')
    axs[1].set_xlabel('Monetary value in Altairian Dollars (A$)')
    axs[1].set_title('Frequency distribution of the purchase prices per customer')

    for ax in axs:
        ax.yaxis.grid(True, linestyle='-', alpha=0.7)
        ax.set_axisbelow(True)

    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Error: {e}")