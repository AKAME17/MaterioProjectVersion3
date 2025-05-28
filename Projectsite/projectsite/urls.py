from django.urls import path
from classic import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
]