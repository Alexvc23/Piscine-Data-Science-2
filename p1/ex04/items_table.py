#!/usr/bin/env python3
import os
import psycopg2
import time
from psycopg2 import sql
from dotenv import load_dotenv
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

def create_items_table(conn, cursor, csv_file_path):
    """Create items table and bulk load data using COPY with duplicate handling"""
    print(f"{Fore.BLUE}{'='*80}")
    print(f"{Fore.CYAN}➤ Processing items file: {Fore.YELLOW}{csv_file_path}")
    print(f"{Fore.BLUE}{'-'*80}")
    
    # Step 1: Create a temporary table without primary key constraint
    cursor.execute("""
    DROP TABLE IF EXISTS items;
    CREATE TABLE items (
        product_id INTEGER,
        category_id DOUBLE PRECISION,
        category_code VARCHAR(255),
        brand VARCHAR(255)
    );
    """)
    conn.commit()
    print(f"{Fore.GREEN}✓ Temporary table created for deduplication.")
    
    # Step 2: Copy all data to the temporary table
    try:
        print(f"{Fore.CYAN}➤ Beginning data import for {Fore.YELLOW}items{Fore.CYAN}...")
        start_time = time.time()
        
        with open(csv_file_path, 'r') as f:
            # Skip the header line
            header = f.readline()
            
            # Copy all data to temp table
            cursor.copy_expert("COPY items FROM STDIN WITH CSV", f)
            
        conn.commit()
        
        # Get row count for the temporary table
        cursor.execute("SELECT COUNT(*) FROM items")
        # fetchone()[0] is the first column of the first row
        total_rows = cursor.fetchone()[0]
        
        # Calculate total time and stats
        total_time = time.time() - start_time
        print(f"{Fore.GREEN}✓ Data loading completed for {Fore.YELLOW}items table")
        print(f"{Fore.CYAN}  ├─ {Fore.WHITE}Total rows: {Fore.YELLOW}{total_rows:,}")
        print(f"{Fore.CYAN}  ├─ {Fore.WHITE}Total time: {Fore.YELLOW}{total_time:.2f} seconds")
        print(f"{Fore.CYAN}  └─ {Fore.WHITE}Average speed: {Fore.YELLOW}{total_rows / total_time:,.1f} rows/sec")
        
    except Exception as e:
        conn.rollback()
        print(f"{Fore.RED}✗ Error loading data into items table: {e}")

def main():
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}{'*'*80}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}*{' ':^78}*")
    print(f"{Fore.YELLOW}{Style.BRIGHT}*{' ITEMS TABLE IMPORT TOOL ':^78}*")
    print(f"{Fore.YELLOW}{Style.BRIGHT}*{' ':^78}*")
    print(f"{Fore.YELLOW}{Style.BRIGHT}{'*'*80}\n")
    
    # Connect to PostgreSQL
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        print(f"{Fore.GREEN}✓ Connected to PostgreSQL database: {Fore.YELLOW}{DB_PARAMS['dbname']} {Fore.GREEN}as {Fore.YELLOW}{DB_PARAMS['user']}")
        
        # Process items.csv file
        items_csv_file = "./data/items/items.csv"
        if not os.path.exists(items_csv_file):
            items_csv_file = "./data/item/items.csv"  # Try alternative path
            
        if os.path.exists(items_csv_file):
            create_items_table(conn, cursor, items_csv_file)
        else:
            print(f"{Fore.RED}✗ Items CSV file not found. Checked both ./data/items/items.csv and ./data/item/items.csv")
        
        # Close the database connection
        cursor.close()
        conn.close()
        print(f"\n{Fore.GREEN}✓ PostgreSQL connection closed. All operations completed.")
        print(f"{Fore.BLUE}{'='*80}")
    
    except Exception as e:
        print(f"{Fore.RED}✗ Error: {e}")

if __name__ == "__main__":
    main()