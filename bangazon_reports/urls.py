from bangazon_reports.views.products.expensive_products import expensiveProducts_list
from bangazon_reports.views.products.inexpensive_products import inexpensiveProducts_list
from django.urls import path
from .views import customerFavorite_list

urlpatterns = [
    path('reports/favoritesellers', customerFavorite_list),
    path('reports/inexpensiveproducts', inexpensiveProducts_list),
    path('reports/expensiveproducts', expensiveProducts_list),
]