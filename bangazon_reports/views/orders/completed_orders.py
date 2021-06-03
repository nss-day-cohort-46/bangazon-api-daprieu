from bangazonapi.models.order import Order
import sqlite3
from django.shortcuts import render
from bangazon_reports.views import Connection


def completedOrders_list(request):
    """Function to build an HTML report of games by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT
                    o.*,
                    u.first_name || " " || u.last_name customer,
                    SUM(p.price) total
                FROM bangazonapi_order o
                JOIN bangazonapi_customer c ON c.id = o.customer_id
                JOIN auth_user u ON u.id = c.user_id
                JOIN bangazonapi_orderproduct op ON op.order_id = o.id
                JOIN bangazonapi_product p ON p.id = op.product_id
                WHERE o.payment_type_id IS NOT NULL
                GROUP BY o.id
            """)
            dataset = db_cursor.fetchall()
            completed_orders_by_id = {}

            for row in dataset:
                # Crete a Order instance and set its properties
                completed_order = Order()
                completed_order.id = row["id"]
                completed_order.payment_type_id = row["payment_type_id"]

                # Store the order's id
                oid = row["id"]

                # If the user's id is already a key in the dictionary...
                if oid in completed_orders_by_id:

                    # Add the current order to the `orders` list for it
                    completed_orders_by_id[oid]['orders'].append(completed_order)

                else:
                    # Otherwise, create the key and dictionary value
                    completed_orders_by_id[oid] = {}
                    completed_orders_by_id[oid]["id"] = oid
                    completed_orders_by_id[oid]["customer"] = row["customer"]
                    completed_orders_by_id[oid]["total"] = row["total"]
                    completed_orders_by_id[oid]["orders"] = [completed_order]

        # Get only the values from the dictionary and create a list from them
        list_of_completed_orders_by_id = completed_orders_by_id.values()

        # Specify the Django template and provide data context
        template = 'orders/completed_orders_list.html'
        context = {
            'completedOrders_list': list_of_completed_orders_by_id
        }

        return render(request, template, context)