import psycopg2
import matplotlib.pyplot as plt

dbname = "piscineds"
user = "jvalenci"
password = "mysecretpassword"
host = "localhost"
port = "5432"

# SQL query defined directly in the file
sql_script = """
SELECT event_type, COUNT(*) as event_count
FROM customers
GROUP BY event_type
ORDER BY event_count DESC;
"""

try:
    print("SQL query is defined in the script.")
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    print("Connected to postgres!")
    # Create a cursor object using the cursor() method
    cursor = conn.cursor()
    # Execute the SQL script
    cursor.execute(sql_script)
    print("SQL script executed successfully!")
    # Fetch all of the rows from the query
    data = cursor.fetchall()
    print("Data has been fetched from the table.")
    # save the changes
    conn.commit()
    cursor.close()
    conn.close()

    # Using lighter tones for the same color scheme
    event_colors = {'view': 'lightblue', 'purchase': 'lightcoral', 'remove_from_cart': 'lightgreen', 'cart': 'moccasin'}

    # !Unzipping the data to get the event types and counts
    # ? e.g data = [('view', 100), ('purchase', 50), ('remove_from_cart', 30), ('cart', 20)]
    # ? *data to asterisk unpacks the data into two lists
    # ? e.g *data = ['view', 'purchase', 'remove_from_cart', 'cart'], [100, 50, 30, 20]
    # ? zip(*data) zips the two lists back together
    # ? event_types = ('view', 'purchase', 'remove_from_cart', 'cart'), counts = (100, 50, 30, 20)
    # ? zip returns an iterator of tuples, which can be unpacked into two lists
    event_types, counts = zip(*data)

    # ? plot the pie chart with the event types and counts
    # ? y = counts, labels = event_types
    plt.pie(counts, labels=[f"{event_type}" for event_type in event_types],

    # ?autopct='%1.1f%%' displays the percentage of each slice in this case with one decimal place
    # ?startangle=0 starts the first slice at 0 degrees
    # ?colors= assigns the color of each slice
            autopct='%1.1f%%', startangle=0, colors=[event_colors.get(event, 'lightgray') for event in event_types])
    
    # ? axis('equal') ensures that the pie is drawn as a circle
    plt.axis('equal')
    plt.show()
except Exception as e:
    print(f"Error: {str(e)}")