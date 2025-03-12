# PostgreSQL and pgAdmin Docker Setup
This project provides a containerized setup for PostgreSQL database and pgAdmin administration tool using Docker Compose.

## Directory Structure

```
p1/
├── data/
│   ├── customer/
│   │   ├── data_2022_dec.csv
│   │   ├── data_2022_nov.csv
│   │   ├── data_2022_oct.csv
│   │   └── data_2023_jan.csv
│   └── items/
│       └── items.csv
├── env/
├── ex00/
│   └── docker-compose.yml
├── ex01/
├── ex02/
│   └── table.py
├── ex03/
│   └── automatic_table.py
├── ex04/
│   └── items_table.py
├── .env
├── copy.sh
├── en.subject.pdf
├── README.md
├── requirements.txt
└── setup.sh
```

## Components

### 1. PostgreSQL Database
- **Image**: postgres:14
- **Container Name**: piscineds_postgres
- **Port**: 5432 (accessible on host)
- **Data**: Stored in a persistent volume named `postgres_data`

### 2. pgAdmin Web Interface
- **Image**: dpage/pgadmin4
- **Container Name**: piscineds_pgadmin
- **Port**: 5050 (accessible on host at http://localhost:5050)
- **Dependencies**: Starts after the PostgreSQL service

## Environment Variables

Sensitive information is stored in the `.env` file:

- `POSTGRES_USER`: Database username
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_DB`: Database name
- `PGADMIN_DEFAULT_EMAIL`: pgAdmin login email
- `PGADMIN_DEFAULT_PASSWORD`: pgAdmin login password

This separation enhances security by keeping credentials out of the version control system.

## Usage

### Starting Services

#### Step 1: Start the Docker Containers
```bash
docker-compose up -d
```
This command starts both services in detached mode. I should see output indicating that the containers were created successfully.

#### Step 2: Verify the PostgreSQL Container is Running
Check that your containers are running:
```bash
docker ps
```
I should see both the PostgreSQL and pgAdmin containers in the list.

### Accessing pgAdmin
1. Open http://localhost:5050 in your browser
2. Log in using the credentials defined in the `.env` file

### Connecting to PostgreSQL via pgAdmin
1. In pgAdmin, add a new server
2. Use `postgres` as the hostname (the Docker service name)
3. Use the PostgreSQL credentials from the `.env` file

### Database Connection Verification

#### Step 1: Connect to PostgreSQL Using Docker
Since PostgreSQL is running in a Docker container, I can connect to it using:
```bash
docker exec -it piscineds_postgres psql -U your_login -d piscineds -h localhost -W
```

When prompted, enter the password: mysecretpassword

I should see something like: ```
psql (14.x)
Type "help" for help.

piscineds=#
```
This confirms that your PostgreSQL setup is working correctly.

### Stopping Services
```bash
docker-compose down
```

## Security Notes

- The `.env` file contains sensitive information and should never be committed to version control
- For production environments, use stronger passwords than the examples


# PostgreSQL Data Loading Project

## Overview

This project implements efficient data loading for an e-commerce database using PostgreSQL. It processes CSV files containing customer sales data and product information, creating appropriate database tables and populating them using high-performance techniques.

The project satisfies the requirements specified in the Piscine Data Science exercise:
- Create a PostgreSQL database with proper authentication
- Set up tables with appropriate data types for customer data and items
- Automate the loading of multiple CSV files


## Scripts

This project contains two main Python scripts for data loading:

### 1. `automatic_table.py`

Handles the automatic creation and loading of customer data tables from all CSV files in the 'customer' folder.

Key features:
- Creates tables named after each CSV file (without extension)
- Assigns appropriate PostgreSQL data types to columns
- Uses the high-performance COPY command for data loading
- Provides detailed performance metrics

### 2. `items_table.py`

Creates and populates the items table, 


## Installation & Setup

### Prerequisites

- PostgreSQL (either installed locally or running in Docker)
- Python 3.6+
- Required Python packages:
  - psycopg2-binary
  - pandas
  - python-dotenv

### Setup Steps

1. Clone the repository
2. Create a `.env` file with your PostgreSQL credentials:
   ```
   POSTGRES_DB=piscineds
   POSTGRES_USER=your_login
   POSTGRES_PASSWORD=mysecretpassword
   ```
3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Run the Customer Data Loading Script

```bash
python3 ex03/automatic_table.py
```

This will:
- Connect to your PostgreSQL database
- Create tables for each CSV file in the customer folder
- Load all data using the COPY command
- Display performance statistics

### 2. Run the Items Table Loading Script

```bash
python3 ex04/items_table.py
```

This will:
- Create table for items data
- Load all data into the table

## Technical Approach

### High-Performance Data Loading

Both scripts use PostgreSQL's COPY command through psycopg2's `copy_expert` method, which provides significant performance advantages over row-by-row INSERT statements:

- Up to 100x faster than individual INSERTs
- Reduced database round-trips
- Lower CPU usage
- Minimized transaction overhead


## Performance Considerations

- The COPY command is significantly faster than individual INSERTs or even batch INSERTs
- Loading time scales approximately linearly with data size
- Using a temporary table for deduplication is more efficient than filtering during insert
- The scripts include progress reporting and timing statistics

## Troubleshooting

If you encounter errors:

1. Check that your PostgreSQL connection details in `.env` are correct
2. Ensure PostgreSQL is running and accessible
3. Verify that the CSV files exist in the expected locations
4. Check that the CSV file format matches the expected structure
