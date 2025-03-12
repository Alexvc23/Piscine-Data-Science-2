-- Improved script for removing duplicates from customers table with better error checking

-- Wrap entire operation in a transaction for atomicity
BEGIN;

-- Step 0: Check if the customers table exists
-- making sure it rolls back the transaction if the table does not exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_tables WHERE tablename = 'customers') THEN
        RAISE EXCEPTION 'The customers table does not exist!';
    END IF;
END $$;

-- Step 1: Count the total records before deduplication
DO $$
DECLARE
    total_count INT;
BEGIN
    SELECT COUNT(*) INTO total_count FROM customers;
    RAISE NOTICE 'Total records before deduplication: %', total_count;
END $$;

-- Step 2: Drop temporary table if it exists from previous runs
DROP TABLE IF EXISTS customers_to_keep;
DROP TABLE IF EXISTS customers_deduplicated;

-- Step 3: Create a temporary table to identify records to keep
CREATE TEMPORARY TABLE customers_to_keep AS
WITH ranked_records AS (
    SELECT 
        event_time,
        event_type,
        product_id,
        price,
        user_id,
        user_session,
        source_table,
        -- Identify exact duplicates (all columns match)
        ROW_NUMBER() OVER (
            PARTITION BY event_time, event_type, product_id, price, user_id, user_session, source_table
            ORDER BY event_time
        ) AS exact_duplicate_rank,
        -- Identify near-time duplicates (same action, same product, within 1 second)
        ROW_NUMBER() OVER (
            PARTITION BY event_type, product_id, user_id
            ORDER BY event_time
        ) AS action_rank,
        LEAD(event_time) OVER (
            PARTITION BY event_type, product_id, user_id
            ORDER BY event_time
        ) - event_time AS time_diff_to_next
    FROM customers
)
SELECT 
    event_time,
    event_type,
    product_id,
    price,
    user_id,
    user_session,
    source_table
FROM ranked_records
WHERE 
    -- Keep only the first instance of exact duplicates
    exact_duplicate_rank = 1
    -- Remove records where the next identical action is within 1 second
    AND (time_diff_to_next IS NULL OR EXTRACT(EPOCH FROM time_diff_to_next) > 1);

-- Step 4: Check if deduplication process found any duplicates
DO $$
DECLARE
    original_count INT;
    new_count INT;
BEGIN
    SELECT COUNT(*) INTO original_count FROM customers;
    SELECT COUNT(*) INTO new_count FROM customers_to_keep;
    
    IF original_count = new_count THEN
        RAISE NOTICE 'No duplicates found. Table remains unchanged.';
    ELSIF new_count = 0 THEN
        RAISE EXCEPTION 'Deduplication would remove all records! Operation aborted.';
    ELSIF new_count < (original_count * 0.5) THEN
        RAISE WARNING 'Deduplication would remove more than 50%% of records. Please verify this is intended.';
    END IF;
END $$;

-- Step 5: Create a new table for the deduplicated data
CREATE TABLE customers_deduplicated AS 
SELECT * FROM customers_to_keep;

-- Step 6: Verification - check how many records we removed
SELECT 
    (SELECT COUNT(*) FROM customers) AS records_before,
    (SELECT COUNT(*) FROM customers_deduplicated) AS records_after,
    (SELECT COUNT(*) FROM customers) - (SELECT COUNT(*) FROM customers_deduplicated) AS records_removed,
    ROUND(((SELECT COUNT(*) FROM customers) - (SELECT COUNT(*) FROM customers_deduplicated))::NUMERIC / 
          (SELECT COUNT(*) FROM customers)::NUMERIC * 100, 2) AS percentage_removed;

-- Step 7: Create a backup of the original table (optional, uncomment if needed)
-- CREATE TABLE customers_backup_TIMESTAMP AS SELECT * FROM customers;

-- Step 8: Replace the original table with the deduplicated one
DROP TABLE customers;
ALTER TABLE customers_deduplicated RENAME TO customers;

-- Step 9: Recreate the indexes with validation
CREATE INDEX idx_customers_event_time ON customers(event_time);
CREATE INDEX idx_customers_product_id ON customers(product_id);
CREATE INDEX idx_customers_user_id ON customers(user_id);

-- Verify indexes were created
SELECT 
    indexname, 
    tablename 
FROM 
    pg_indexes 
WHERE 
    tablename = 'customers';

-- Step 10: Final record count
DO $$
DECLARE
    final_count INT;
BEGIN
    SELECT COUNT(*) INTO final_count FROM customers;
    RAISE NOTICE 'Final record count: %', final_count;
END $$;

-- Log deduplication completion
DO $$
BEGIN
    RAISE NOTICE 'Deduplication completed successfully at %', now();
END $$;

COMMIT;