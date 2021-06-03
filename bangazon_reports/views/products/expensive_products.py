import sqlite3
from django.shortcuts import render
from bangazon_reports.views import Connection


def expensiveProducts_list(request):
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
                WHERE p.price >= 1000
            """)

            dataset = db_cursor.fetchall()

            expensive_products_list = []

            for row in dataset:
                # Crete a Product instance and set its properties
                expensive_products = {}
                expensive_products['id'] = row["id"]
                expensive_products['name'] = row["name"]
                expensive_products['price'] = row["price"]

                expensive_products_list.append(expensive_products)

        # Specify the Django template and provide data context
        template = 'products/list_of_expensive_products.html'
        context = {
            'expensiveProducts_list': expensive_products_list
        }

        return render(request, template, context)