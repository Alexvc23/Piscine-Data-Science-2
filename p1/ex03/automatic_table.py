#!/usr/bin/env python3
import os
import psycopg2
import time
import glob
from psycopg2 import sql
from dotenv import load_dotenv
import pandas as pd
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored terminal text
init(autoreset=True)

# Load environment variables from .env file
load_dotenv()

# Database connection parameters from environment variables
DB_PARAMS = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': 'localhost',
    'port': '5432'
}

def create_customer_tables(conn, cursor, csv_file_path):
    """Create a customer table and bulk load data using COPY"""
    # Extract the table name from file path (without extension)
    table_name = os.path.splitext(os.path.basename(csv_file_path))[0]
    print(f"{Fore.BLUE}{'='*80}")
    print(f"{Fore.CYAN}➤ Processing: {Fore.YELLOW}{csv_file_path} {Fore.GREEN}→ {Fore.MAGENTA}{table_name}")
    print(f"{Fore.BLUE}{'-'*80}")
    
    # Sample the CSV to determine data types
    df_sample = pd.read_csv(csv_file_path, nrows=5)
    print(f"{Fore.CYAN}➤ Sample columns: {Fore.WHITE}{', '.join(df_sample.columns.tolist())}")
    
    # Drop table if it exists
    drop_table_query = sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(table_name))
    cursor.execute(drop_table_query)
    
    # Create table with appropriate data types
    create_table_query = sql.SQL("""
    CREATE TABLE {} (
        event_time TIMESTAMP,
        event_type VARCHAR(255),
        product_id INTEGER,
        price NUMERIC(10, 2),
        user_id BIGINT,
        user_session VARCHAR(255)
    )
    """).format(sql.Identifier(table_name))
    
    cursor.execute(create_table_query)
    conn.commit()
    print(f"{Fore.GREEN}✓ Table {Fore.YELLOW}{table_name}{Fore.GREEN} created successfully")
    
    # Load data using COPY
    try:
        print(f"{Fore.CYAN}➤ Beginning data import for {Fore.YELLOW}{table_name}{Fore.CYAN}...")
        start_time = time.time()
        
        # Use copy_expert for maximum performance
        with open(csv_file_path, 'r') as f:
            # Skip the header line
            header = f.readline()
            
            # Create a COPY command
            copy_sql = sql.SQL("""
            COPY {} FROM STDIN WITH CSV
            """).format(sql.Identifier(table_name))
            
            # Execute the COPY command
            cursor.copy_expert(copy_sql, f)
            
        conn.commit()
        
        # Get row count
        cursor.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(table_name)))
        row_count = cursor.fetchone()[0]
        
        # Final stats
        total_time = time.time() - start_time
        print(f"{Fore.GREEN}✓ Data loading completed for {Fore.YELLOW}{table_name}")
        print(f"{Fore.CYAN}  ├─ {Fore.WHITE}Total rows: {Fore.YELLOW}{row_count:,}")
        print(f"{Fore.CYAN}  ├─ {Fore.WHITE}Total time: {Fore.YELLOW}{total_time:.2f} seconds")
        print(f"{Fore.CYAN}  └─ {Fore.WHITE}Average speed: {Fore.YELLOW}{row_count / total_time:,.1f} rows/sec")
              
    except Exception as e:
        conn.rollback()
        print(f"{Fore.RED}✗ Error loading data into {table_name}: {e}")

def main():
    """Main function to process all customer data"""
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}{'*'*80}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}*{' ':^78}*")
    print(f"{Fore.YELLOW}{Style.BRIGHT}*{' POSTGRESQL DATA IMPORT TOOL ':^78}*")
    print(f"{Fore.YELLOW}{Style.BRIGHT}*{' ':^78}*")
    print(f"{Fore.YELLOW}{Style.BRIGHT}{'*'*80}\n")
    
    # Connect to PostgreSQL
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        print(f"{Fore.GREEN}✓ Connected to PostgreSQL database: {Fore.YELLOW}{DB_PARAMS['dbname']} {Fore.GREEN}as {Fore.YELLOW}{DB_PARAMS['user']}")
        
        # Process all CSV files in the customer folder
        customer_csv_files = glob.glob("./data/customer/*.csv")
        if not customer_csv_files:
            print(f"{Fore.RED}✗ No CSV files found in the customer folder.")
        else:
            print(f"{Fore.CYAN}➤ Found {Fore.YELLOW}{len(customer_csv_files)}{Fore.CYAN} CSV files to process")
            for csv_file in customer_csv_files:
                create_customer_tables(conn, cursor, csv_file)
        
        # Close the database connection
        cursor.close()
        conn.close()
        print(f"\n{Fore.GREEN}✓ PostgreSQL connection closed. All operations completed.")
        print(f"{Fore.BLUE}{'='*80}")
    
    except Exception as e:
        print(f"{Fore.RED}✗ Error: {e}")

if __name__ == "__main__":
    main()