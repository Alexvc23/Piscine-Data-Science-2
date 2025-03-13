# pyscopg2 is a PostgreSQL database adapter for the Python programming language.
import psycopg2

dbname = "piscineds"
user = "jvalenci"
password = "mysecretpassword"
host = "localhost"
port = "5432"

try:
    with open("ex03/fusion.sql", "r") as sql_file:
        sql_script = sql_file.read()
    print("SQL code has been imported!")
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    print("Connected to postgres!")
    cursor = conn.cursor()
    cursor.execute(sql_script)
    print("SQL script executed successfully!")
    conn.commit()
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error: {str(e)}")