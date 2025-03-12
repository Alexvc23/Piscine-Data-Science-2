#!/usr/bin/env python3
import os
import psycopg2
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import seaborn as sns

# Load environment variables from .env file
load_dotenv()

# Database connection parameters from environment variables
DB_PARAMS = {
    'dbname': os.getenv('POSTGRES_DB', 'ecommerce_dw'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'password'),
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', '5432')
}

def connect_to_database():
    """Establish connection to the PostgreSQL database"""
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        print("Successfully connected to the data warehouse")
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def get_purchase_data(conn):
    """Query the database to get purchase data for statistical analysis"""
    query = """
    SELECT 
        user_id,
        price,
        product_id,
        user_session
    FROM 
        customers
    WHERE 
        event_type = 'purchase'
        AND event_time BETWEEN '2022-10-01' AND '2023-02-28 23:59:59'
    """
    
    try:
        # Use server-side cursor for efficient memory usage with large datasets
        cursor = conn.cursor(name='fetch_purchases_stats')
        cursor.execute(query)
        
        # Fetch data in chunks and build DataFrame
        chunk_size = 100000
        chunks = []
        
        while True:
            records = cursor.fetchmany(chunk_size)
            if not records:
                break
            chunk_df = pd.DataFrame(records, columns=['user_id', 'price', 'product_id', 'user_session'])
            chunks.append(chunk_df)
        
        cursor.close()
        
        if not chunks:
            print("No purchase data found for the specified period")
            return None
        
        # Combine all chunks
        df = pd.concat(chunks, ignore_index=True)
        # Convert decimal.Decimal to float to avoid type errors in calculations
        df['price'] = df['price'].astype(float)
        print(f"Retrieved {len(df)} purchase records for statistical analysis")
        return df
    
    except Exception as e:
        print(f"Error executing query: {e}")
        return None

def calculate_statistics(df):
    """Calculate statistical measures for purchase prices"""
    # Calculate basic statistics manually to avoid pandas version issues
    count = len(df)
    mean = df['price'].mean()
    std = df['price'].std()
    min_val = df['price'].min()
    
    # Calculate quartiles
    q1 = np.percentile(df['price'], 25)
    median = np.percentile(df['price'], 50)
    q3 = np.percentile(df['price'], 75)
    max_val = df['price'].max()
    
    # Create a dictionary with all statistics
    stats_dict = {
        'count': count,
        'mean': mean,
        'std': std,
        'min': min_val,
        'q1': q1,
        'median': median,
        'q3': q3,
        'max': max_val
    }
    
    # Print statistics in formatted table
    print("\nStatistical Analysis of Purchase Prices (Altairian Dollars):")
    print("=" * 50)
    print(f"count      : {count:,.0f}")
    print(f"mean       : {mean:.6f}")
    print(f"std        : {std:.6f}")
    print(f"min        : {min_val:.6f}")
    print(f"25%        : {q1:.6f}")
    print(f"50% (median): {median:.6f}")
    print(f"75%        : {q3:.6f}")
    print(f"max        : {max_val:.6f}")
    
def create_price_boxplot(df, stats=None, output_file="price_boxplot.png"):
    """Create box plot of purchase prices"""
    # Reset to default matplotlib style
    plt.style.use('default')
    # Reset to default matplotlib style
    plt.style.use('default')
    
    # Create figure - make two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10), gridspec_kw={'height_ratios': [1, 1]})
    
    # First subplot - Full range
    sns.boxplot(x=df['price'], ax=ax1, color='none', fliersize=2)
    ax1.set_xlim(-50, 300)
    ax1.set_xlabel('price')
    ax1.grid(True, axis='x')
    
    # Second subplot - Zoomed in with green box
    sns.boxplot(x=df['price'], ax=ax2, color='#8fbc8f', fliersize=0)
    ax2.set_xlim(0, 12)
    ax2.set_xlabel('price')
    ax2.grid(True, axis='x')
    
    # Add grid lines to both plots
    ax1.xaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax2.xaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    
    # Save figure
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"Price distribution boxplot saved as '{output_file}'")
    
    return fig

def calculate_avg_basket_per_user(df):
    """Calculate average basket price per user"""
    # Group by user_id and user_session to identify unique baskets
    basket_df = df.groupby(['user_id', 'user_session'])['price'].sum().reset_index()
    basket_df.columns = ['user_id', 'user_session', 'basket_total']
    
    # Calculate average basket per user
    avg_basket_df = basket_df.groupby('user_id')['basket_total'].mean().reset_index()
    avg_basket_df.columns = ['user_id', 'avg_basket_price']
    
    print(f"Calculated average basket price for {len(avg_basket_df)} users")
    return avg_basket_df

def create_avg_basket_boxplot(avg_basket_df, output_file="avg_basket_boxplot.png"):
    """Create box plot of average basket price per user"""
    # Reset to default matplotlib style
    plt.style.use('default')
    
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Create title text as a separate figure element (not on the plot itself)
    fig.text(0.5, 0.95, "Then a box plot with the average basket price per user", 
             ha='center', fontsize=12)
    
    # Create box plot - horizontal with light blue color
    sns.boxplot(x=avg_basket_df['avg_basket_price'], ax=ax, color='#87CEEB', fliersize=2)
    
    # Set x-axis range to match example
    ax.set_xlim(28, 42)
    
    # Add x-axis label
    ax.set_xlabel('price')
    
    # Add grid
    ax.grid(True, axis='x')
    ax.xaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    
    # Save and show plot
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"Average basket boxplot saved as '{output_file}'")
    
    return fig

def main():
    """Main function to perform statistical analysis and create box plots"""
    print("Exercise 02: My beautiful mustache - Statistical analysis of purchase prices")
    
    # Connect to the database
    conn = connect_to_database()
    if not conn:
        return
    
    try:
        # Get purchase data
        purchase_data = get_purchase_data(conn)
        if purchase_data is not None and not purchase_data.empty:
            # Calculate and display statistics
            stats = calculate_statistics(purchase_data)
            
            # Create box plot of purchase prices
            create_price_boxplot(purchase_data, stats)
            
            # Calculate average basket price per user
            avg_basket_df = calculate_avg_basket_per_user(purchase_data)
            
            # Create box plot of average basket price per user
            create_avg_basket_boxplot(avg_basket_df)
            
            print("All analyses and visualizations for Exercise 02 completed successfully")
        else:
            print("No data available for analysis")
    finally:
        # Close the database connection
        conn.close()
        print("Database connection closed")

if __name__ == "__main__":
    main()