-- Check if duplicates for product_id 5809103 have been removed
SELECT event_time, event_type, product_id 
FROM customers 
WHERE event_time::timestamp::date = '2022-10-01' 
    AND event_time::time >= '00:00:30'::time
    AND event_time::time < '00:00:31'::time
    AND product_id = 5809103
    AND event_type = 'remove_from_cart'
ORDER BY event_time;


-- Check if duplicates for product_id 5779403 have been removed
SELECT event_time, event_type, product_id 
FROM customers 
WHERE event_time BETWEEN '2022-10-01 00:00:32' AND '2022-10-01 00:00:33'
    AND product_id = 5779403
    AND event_type = 'remove_from_cart'
ORDER BY event_time;

-- Check if non-duplicates still exist
SELECT event_time, event_type, product_id 
FROM customers 
WHERE event_time::timestamp::date = '2022-10-01' 
    AND event_time::time = '00:04:15'::time
    AND product_id IN (5692893, 5802443)
    AND event_type = 'remove_from_cart'
ORDER BY event_time;

-- Check total count of records
SELECT COUNT(*) FROM customers;