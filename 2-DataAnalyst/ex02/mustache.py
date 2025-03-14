import psycopg2
import numpy as np
import matplotlib.pyplot as plt

dbname = "piscineds"
user = "jvalenci"
password = "mysecretpassword"
host = "localhost"
port = "5432"

try:
    with open("ex02/mustache.sql", "r") as sql_file:
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

    prices = [float(price) for event_type, price in data if event_type == 'purchase']

    count = len(prices)
    mean_price = np.mean(prices)
    std_price = np.std(prices)
    min_price = np.min(prices)
    quartiles = np.percentile(prices, [25, 50, 75])
    max_price = np.max(prices)

    print(f"count {count:.6f}")
    print(f"mean {mean_price:.6f}")
    print(f"std {std_price:.6f}")
    print(f"min {min_price:.6f}")
    print(f"25% {quartiles[0]:.6f}")
    print(f"50% {quartiles[1]:.6f}")
    print(f"75% {quartiles[2]:.6f}")
    print(f"max {max_price:.6f}")

    # (ax1, ax2) are the two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    # notch=True makes the boxplot notched (notch is the indentation at the median)
    boxes = ax1.boxplot(prices, vert=False, widths=0.5, notch=True,
                        # boxprops appereance of the boxes
                        boxprops=dict(facecolor='lightgray', edgecolor='none'),
                        # flierprops appearance of the outliers
                            # marker is the shape of the outlier "D" is a diamond
                            # patch_artist=True fills the outliers
                        flierprops=dict(marker='D', markersize=8, markerfacecolor='lightgray', markeredgecolor='none'),
                        patch_artist=True)
    ax1.set_yticks([])
    ax1.set_xlabel("Price")
    ax1.set_title("Full Box Plot")

    # ──────────────────────────────────────────────────────────────────────
    # boxprops is used to customize the appearance of the boxes
    boxprops = dict(facecolor='green', edgecolor='black')
    # medianprops is used to customize the appearance
    # of the median line
    medianprops = dict(linestyle='-', linewidth=2, color='black')
    # boxplot() method creates the boxplot
    # vert=False makes the boxplot horizontal
    # widths=0.5 sets the width of the boxes
    # notch=True makes the boxplot notched
    # showfliers=False hides the outliers
    ax2.boxplot(prices, vert=False, widths=0.5, notch=True,
                boxprops=boxprops, medianprops=medianprops, showfliers=False,
                patch_artist=True)
    ax2.set_yticks([])
    ax2.set_xlabel("Price")
    ax2.set_title("Interquartile range (IQR)")

    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Error: {e}")
