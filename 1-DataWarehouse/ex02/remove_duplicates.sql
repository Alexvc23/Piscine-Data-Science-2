/* 
 * Script: remove_duplicates.sql
 * Purpose: Removes duplicate entries from the customers table
 *
 * This script identifies and eliminates duplicate rows from the customers table
 * where duplicates are defined as entries with identical:
 * - event_type
 * - product_id
 * - price
 * - user_id
 * - user_session
 * AND occurring within 1 second of each other.
 *
 * The process:
 * 1. Creates a temporary table using window functions to identify duplicates
 * 2. Uses lag() function to compare each row with previous rows in same partition
 * 3. Keeps only unique rows or those separated by more than 1 second
 * 4. Replaces the original customers table with the de-duplicated version
 *
 * The transaction ensures atomicity - either all operations complete successfully
 * or none take effect.
 */
BEGIN TRANSACTION;

DO $$
DECLARE
    initial_count INT;
    final_count INT;
    removed_count INT;
BEGIN
    -- Get initial count
    SELECT COUNT(*) INTO initial_count FROM customers;
    RAISE NOTICE 'Initial number of records: %', initial_count;
    
    CREATE TABLE tmp AS 
    WITH remove_duplicates AS (
        SELECT *,
            LAG(event_time) OVER (
                PARTITION BY event_type, product_id, price, user_id, user_session 
                ORDER BY event_time
            ) AS prevtime,
            LAG(product_id) OVER (
                PARTITION BY event_type, product_id, price, user_id, user_session 
                ORDER BY event_time
            ) AS prevproduct,
            LAG(event_type) OVER (
                PARTITION BY event_type, product_id, price, user_id, user_session 
                ORDER BY event_time
            ) AS prevevent_type,
            LAG(user_id) OVER (
                PARTITION BY event_type, product_id, price, user_id, user_session 
                ORDER BY event_time
            ) AS prevuser_id,
            LAG(user_session) OVER (
                PARTITION BY event_type, product_id, price, user_id, user_session 
                ORDER BY event_time
            ) AS prevuser_session,
            LAG(price) OVER (
                PARTITION BY event_type, product_id, price, user_id, user_session 
                ORDER BY event_time
            ) AS prevprice
        FROM customers
    )
    SELECT 
        event_time, 
        event_type, 
        product_id, 
        price, 
        user_id, 
        user_session
    FROM remove_duplicates
    WHERE user_id != user_id 
       OR user_session != user_session 
       OR price != price 
       OR prevevent_type != event_type 
       OR prevproduct != product_id 
       OR event_time - prevtime > INTERVAL '1 second' 
       OR prevtime IS NULL;

    -- Get final count
    SELECT COUNT(*) INTO final_count FROM tmp;
    removed_count := initial_count - final_count;
    
    RAISE NOTICE 'Final number of records: %', final_count;
    RAISE NOTICE 'Number of duplicates removed: %', removed_count;
    RAISE NOTICE 'Percentage of duplicates: %.2f%%', (removed_count * 100.0 / initial_count);

    DROP TABLE customers;
    ALTER TABLE tmp RENAME TO customers;
END;
$$;