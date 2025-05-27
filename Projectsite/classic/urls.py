from django.urls import path
from . import views
from classic.views import OrderListView

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('order/', OrderListView, name='order_list'),
]