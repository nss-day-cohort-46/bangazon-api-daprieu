SELECT
                    c.id,
                    u.first_name || ' ' || u.last_name AS customer_name,
                    f.seller_id AS Favortie_seller,
                    fs.first_name || ' ' || fs.last_name AS fav_seller_name
                FROM
                    bangazonapi_customer c
                JOIN
                    bangazonapi_favorite f ON f.customer_id = c.id
                JOIN
                    auth_user u ON c.id = u.id
                Join 
                    auth_user fs ON f.seller_id = fs.id