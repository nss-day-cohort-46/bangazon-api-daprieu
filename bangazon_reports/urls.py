from django.urls import path
from .views import customerFavorite_list

urlpatterns = [
    path('reports/favoritesellers', customerFavorite_list),
]