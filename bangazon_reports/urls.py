from bangazon_reports.views.orders.incomplete_orders import incompleteOrders_list
from django.urls import path
from .views import customerFavorite_list, incompleteOrders_list

urlpatterns = [
    path('reports/favoritesellers', customerFavorite_list),
    path('reports/incompleteorders', incompleteOrders_list),
]