from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('rentals/', views.rental_list, name='rental_list'), 
]