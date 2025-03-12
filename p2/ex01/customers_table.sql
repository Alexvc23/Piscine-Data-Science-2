-- Transaction block with error handling
BEGIN;

-- Set client_min_messages to notice to see info messages
SET client_min_messages TO notice;

DO $$
BEGIN
    -- First, drop the customers table if it exists
    DROP TABLE IF EXISTS customers;
    
    -- Create the customers table with the same structure
    CREATE TABLE IF NOT EXISTS customers (
        event_time TIMESTAMP,
        event_type VARCHAR(255),
        product_id INTEGER,
        price NUMERIC(10, 2),
        user_id BIGINT,
        user_session VARCHAR(255),
        source_table VARCHAR(50)  -- Added to track which table the data came from
    );
    
    -- Check if all source tables exist before insertion
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'data_2022_oct') THEN
        RAISE EXCEPTION 'Source table data_2022_oct does not exist';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'data_2022_nov') THEN
        RAISE EXCEPTION 'Source table data_2022_nov does not exist';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'data_2022_dec') THEN
        RAISE EXCEPTION 'Source table data_2022_dec does not exist';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'data_2023_jan') THEN
        RAISE EXCEPTION 'Source table data_2023_jan does not exist';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'data_2023_feb') THEN
        RAISE EXCEPTION 'Source table data_2023_feb does not exist';
    END IF;
    
    -- Populate the customers table with data from all customer tables
    INSERT INTO customers (event_time, event_type, product_id, price, user_id, user_session, source_table)
    SELECT 
        event_time, 
        event_type, 
        product_id, 
        price, 
        user_id, 
        user_session,
        'data_2022_oct' AS source_table
    FROM data_2022_oct

    UNION ALL

    SELECT 
        event_time, 
        event_type, 
        product_id, 
        price, 
        user_id, 
        user_session,
        'data_2022_nov' AS source_table
    FROM data_2022_nov

    UNION ALL

    SELECT 
        event_time, 
        event_type, 
        product_id, 
        price, 
        user_id, 
        user_session,
        'data_2022_dec' AS source_table
    FROM data_2022_dec

    UNION ALL

    SELECT 
        event_time, 
        event_type, 
        product_id, 
        price, 
        user_id, 
        user_session,
        'data_2023_jan' AS source_table
    FROM data_2023_jan

    UNION ALL

    SELECT 
        event_time, 
        event_type, 
        product_id, 
        price, 
        user_id, 
        user_session,
        'data_2023_feb' AS source_table
    FROM data_2023_feb;

    -- Verify data was properly inserted
    PERFORM COUNT(*) FROM customers;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Failed to insert data into the customers table';
    END IF;
    
    RAISE NOTICE 'Successfully inserted data into the customers table';
    
    -- Create indexes for better performance
    CREATE INDEX idx_customers_event_time ON customers(event_time);
    CREATE INDEX idx_customers_product_id ON customers(product_id);
    CREATE INDEX idx_customers_user_id ON customers(user_id);
    
    RAISE NOTICE 'Successfully created indexes on the customers table';

EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'An error occurred: %', SQLERRM;
    RAISE EXCEPTION '%', SQLERRM;
END $$;

-- Commit the transaction if PL/pgSQL block succeeds
COMMIT;

-- Start a new transaction for the queries
BEGIN;

-- Display record count by source table using RAISE NOTICE
DO $$
DECLARE
    rec RECORD;
    total BIGINT;
BEGIN
    FOR rec IN 
        SELECT source_table, COUNT(*) AS record_count
        FROM customers
        GROUP BY source_table
        ORDER BY source_table
    LOOP
        RAISE NOTICE 'Source table: %, Record count: %', rec.source_table, rec.record_count;
    END LOOP;
    
    -- Display the total number of records in the customers table
    SELECT COUNT(*) INTO total FROM customers;
    RAISE NOTICE 'Total records in customers table: %', total;
END $$;

COMMIT;