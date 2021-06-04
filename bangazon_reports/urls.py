from django.urls import path
from .views import customer_favorite_list, completed_orders_list, incomplete_orders_list, inexpensive_products_list, expensive_products_list

urlpatterns = [
    
    path('reports/expensiveproducts', expensive_products_list),
    path('reports/favoritesellers', customer_favorite_list),
    path('reports/completedorders', completed_orders_list),
    path('reports/incompleteorders', incomplete_orders_list),
    path('reports/incompleteorders', inexpensive_products_list),
]