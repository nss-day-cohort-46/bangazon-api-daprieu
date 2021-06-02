
SELECT
    c.*,
    cus.first_name || ' ' || cus.last_name AS customer,
    r.product_id,
    r.recommender_id,
    rs.first_name || ' ' || rs.last_name AS recommender
FROM
    bangazonapi_customer c
JOIN 
    bangazonapi_recommendation r ON r.customer_id = c.id
JOIN 
    auth_user rs ON rs.id = r.customer_id
JOIN 
    auth_user cus ON cus.id = c.user_id