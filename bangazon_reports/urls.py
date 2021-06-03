from django.urls import path
from .views import customerFavorite_list, completedOrders_list

urlpatterns = [
    path('reports/favoritesellers', customerFavorite_list),
    path('reports/completedorders', completedOrders_list),
]