from bangazon_reports.views.products.inexpensive_products import inexpensiveProducts_list
from django.urls import path
from .views import customerFavorite_list

urlpatterns = [
    path('reports/favoritesellers', customerFavorite_list),
    path('reports/inexpensiveproducts', inexpensiveProducts_list),
]