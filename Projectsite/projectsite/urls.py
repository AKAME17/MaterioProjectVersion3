from django.contrib import admin
from django.urls import path, include

from classic.views import OrderListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('classic.urls')),


    #order_list
    path('order/', OrderListView, name='order_list'),
    
]