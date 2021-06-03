from bangazonapi.models.order import Order
from bangazonapi.models.customer import Customer
import sqlite3
from django.shortcuts import render
from bangazonapi.models import Favorite
from bangazon_reports.views import Connection


def incompleteOrders_list(request):
    """Function to build an HTML report of games by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT
                    o.id ,
                    o.payment_type_id,
                    u.first_name || ' ' || u.last_name customer,
                    SUM(p.price) total
                FROM
                    bangazonapi_order o
                JOIN
                    bangazonapi_customer cus ON cus.id = o.customer_id
                JOIN
                    auth_user u ON u.id = cus.user_id
                JOIN
                    bangazonapi_orderproduct op ON op.order_id = o.id
                JOIN
                    bangazonapi_product p ON p.id = op.Product_id
                WHERE o.payment_type_id is NULL
                GROUP BY o.id
            """)

            dataset = db_cursor.fetchall()

            incomplete_orders_by_id = {}

            for row in dataset:
                # Crete a Order instance and set its properties
                incomplete_order = Order()
                incomplete_order.id = row["id"]
                incomplete_order.payment_type_id = row["payment_type_id"]

                # Store the Orders id
                oid = row["id"]

                # If the orders id is already a key in the dictionary...
                if oid in incomplete_orders_by_id:

                    # Add the current order to the `orders` for it
                    incomplete_orders_by_id[oid]["orders"].append(incomplete_order)

                else:
                    # Otherwise, create the key and dictionary value
                    incomplete_orders_by_id[oid] = {}
                    incomplete_orders_by_id[oid]["id"] = oid
                    incomplete_orders_by_id[oid]["customer"] = row["customer"]
                    incomplete_orders_by_id[oid]["total"] = row["total"]
                    incomplete_orders_by_id[oid]["orders"] = [incomplete_order]

        # Get only the values from the dictionary and create a list from them
        list_of_incomplete_orders_by_id = incomplete_orders_by_id.values()

        # Specify the Django template and provide data context
        template = 'orders/list_of_incomplete_orders.html'
        context = {
            'incompleteOrders_list': list_of_incomplete_orders_by_id
        }

        return render(request, template, context)