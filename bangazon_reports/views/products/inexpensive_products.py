import sqlite3
from django.shortcuts import render
from bangazon_reports.views import Connection


def inexpensive_products_list(request):
    """Function to build an HTML report of games by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT
                    p.id,
                    p.name,
                    p.price
                FROM bangazonapi_product p
                WHERE p.price <= 999
            """)

            dataset = db_cursor.fetchall()

            inexpensive_products_list = []

            for row in dataset:
                # Crete a Product instance and set its properties
                inexpensive_products = {}
                inexpensive_products['id'] = row["id"]
                inexpensive_products['name'] = row["name"]
                inexpensive_products['price'] = row["price"]

                inexpensive_products_list.append(inexpensive_products)

        # Specify the Django template and provide data context
        template = 'products/list_of_inexpensive_products.html'
        context = {
            'inexpensive_products_list': inexpensive_products_list
        }

        return render(request, template, context)