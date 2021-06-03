from bangazonapi.models.customer import Customer
import sqlite3
from django.shortcuts import render
from bangazonapi.models import Favorite
from bangazon_reports.views import Connection


def customerFavorite_list(request):
    """Function to build an HTML report of games by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
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
            """)

            dataset = db_cursor.fetchall()

            favorite_seller_by_customer = {}

            for row in dataset:
                # Crete a  Customer instance and set its properties
                favorite = Customer()
                favorite.seller = row["fav_seller_name"]

                # Store the user's id
                uid = row["id"]

                # If the user's id is already a key in the dictionary...
                if uid in favorite_seller_by_customer:

                    # Add the current seller to the `sellers` list for it
                    favorite_seller_by_customer[uid]['seller'].append(favorite)

                else:
                    # Otherwise, create the key and dictionary value
                    favorite_seller_by_customer[uid] = {}
                    favorite_seller_by_customer[uid]["id"] = uid
                    favorite_seller_by_customer[uid]["customer_name"] = row["customer_name"]
                    favorite_seller_by_customer[uid]["seller"] = [favorite]

        # Get only the values from the dictionary and create a list from them
        list_of_customers_with_favorite_sellers = favorite_seller_by_customer.values()

        # Specify the Django template and provide data context
        template = 'users/list_with_favorite_sellers.html'
        context = {
            'customerFavorite_list': list_of_customers_with_favorite_sellers
        }

        return render(request, template, context)