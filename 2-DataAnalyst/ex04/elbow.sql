/*
* This query identifies users with fewer than 30 purchases from the customers table.
* 
* It returns:
*   - user_id: Unique identifier for each user
*   - purchases: Count of purchase events per user
*
* The results are:
*   - Filtered to include only purchase events
*   - Limited to users with fewer than 30 purchases 
*   - Ordered by purchase count in descending order (highest first)
*
* This query can be used for customer segmentation analysis or to identify
* users with moderate purchasing activity.
*/
SELECT user_id, COUNT(*) AS purchases
FROM customers
WHERE event_type = 'purchase'
GROUP BY user_id
HAVING COUNT(*) < 30
ORDER BY purchases DESC;