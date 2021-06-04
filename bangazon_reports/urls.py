from bangazon_reports.views.orders.incomplete_orders import incompleteOrders_list
from django.urls import path
from .views import customer_favorite_list, completed_orders_list, incomplete_orders_list

urlpatterns = [
    path('reports/favoritesellers', customer_favorite_list),
    path('reports/completedorders', completed_orders_list),
    path('reports/incompleteorders', incomplete_orders_list),
]