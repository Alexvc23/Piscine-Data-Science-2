-- Exercise 03: Fusion - Combine the customers table with items table

-- Start transaction
BEGIN;

DO $$
DECLARE
    original_customer_count INTEGER;
    enhanced_customer_count INTEGER;
BEGIN
    -- Error handling for the entire process
    BEGIN
        -- Check if backup table already exists and drop it if needed
        DROP TABLE IF EXISTS customers_backup;

        -- Create a fresh backup of the customers table
        CREATE TABLE customers_backup AS SELECT * FROM customers;
        
        -- Store original count for validation later
        SELECT COUNT(*) INTO original_customer_count FROM customers;
        RAISE NOTICE 'Original customer count: %', original_customer_count;

        -- Check for duplicates in the items table
        RAISE NOTICE 'Checking for duplicate products in items table...';
        PERFORM 
            product_id, 
            COUNT(*) AS duplicate_count
        FROM items
        GROUP BY product_id
        HAVING COUNT(*) > 1
        ORDER BY COUNT(*) DESC
        LIMIT 10;

        -- Create a deduplicated items table to avoid multiplying customer records
        DROP TABLE IF EXISTS items_deduplicated;
        CREATE TABLE items_deduplicated AS
        SELECT DISTINCT ON (product_id) 
            product_id,
            category_id,
            category_code,
            brand
        FROM items
        ORDER BY product_id, category_id;

        -- Verify the deduplication worked
        RAISE NOTICE 'Deduplication summary: % original items, % deduplicated items, % duplicates removed',
            (SELECT COUNT(*) FROM items),
            (SELECT COUNT(*) FROM items_deduplicated),
            (SELECT COUNT(*) FROM items) - (SELECT COUNT(*) FROM items_deduplicated);

        -- Create the enhanced table using the deduplicated items
        DROP TABLE IF EXISTS customers_enhanced;
        CREATE TABLE customers_enhanced AS
        SELECT
            c.event_time,
            c.event_type,
            c.product_id,
            c.price,
            c.user_id,
            c.user_session,
            c.source_table,
            i.category_id,
            i.category_code,
            i.brand
        FROM
            customers c
        LEFT JOIN
            items_deduplicated i ON c.product_id = i.product_id;

        -- Verify counts match
        SELECT COUNT(*) INTO enhanced_customer_count FROM customers_enhanced;
        
        IF original_customer_count <> enhanced_customer_count THEN
            RAISE EXCEPTION 'Count mismatch: original=%, enhanced=%', 
                original_customer_count, enhanced_customer_count;
        ELSE
            RAISE NOTICE 'Count verification successful: % records', original_customer_count;
        END IF;

        -- Check how many customer records have product information
        RAISE NOTICE 'Checking product information coverage...';
        PERFORM
            COUNT(*) AS total_records,
            COUNT(category_id) AS records_with_category,
            COUNT(brand) AS records_with_brand,
            SUM(CASE WHEN category_id IS NULL AND brand IS NULL THEN 1 ELSE 0 END) AS records_missing_product_info,
            (COUNT(category_id) * 100.0 / COUNT(*))::numeric(5,2) AS percent_with_category_info
        FROM customers_enhanced;

        -- Replace the existing customers table with the enhanced version
        DROP TABLE customers;
        ALTER TABLE customers_enhanced RENAME TO customers;

        -- Clean up the temporary table
        DROP TABLE items_deduplicated;

        -- Create appropriate indexes for the enhanced table
        CREATE INDEX idx_customers_event_time ON customers(event_time);
        CREATE INDEX idx_customers_product_id ON customers(product_id);
        CREATE INDEX idx_customers_user_id ON customers(user_id);
        CREATE INDEX idx_customers_category_id ON customers(category_id);
        CREATE INDEX idx_customers_brand ON customers(brand);

        RAISE NOTICE 'Data fusion completed successfully';
        
    EXCEPTION WHEN OTHERS THEN
        -- Log the error and roll back
        RAISE NOTICE 'Error occurred during fusion process: %', SQLERRM;
        RAISE EXCEPTION '%', SQLERRM;
    END;
END $$;

-- If everything succeeded, commit the transaction
COMMIT;

-- Display sample data and stats (outside the transaction)
SELECT * FROM customers LIMIT 10;

-- Show stats about product data coverage
SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT product_id) AS unique_products,
    COUNT(DISTINCT category_code) AS unique_categories,
    COUNT(DISTINCT brand) AS unique_brands,
    SUM(CASE WHEN category_id IS NULL THEN 1 ELSE 0 END) AS products_missing_category,
    SUM(CASE WHEN brand IS NULL THEN 1 ELSE 0 END) AS products_missing_brand
FROM customers;