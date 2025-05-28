from django.urls import path
from classic import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('employees/', views.EmployeeListView.as_view(), name='employee_list'),
]