from django.shortcuts import render
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from .models import Customers, Employees, Orders, Payments, Products
from django.views.generic import ListView
import json

class OrderListView(ListView):
    model = Orders
    template_name = 'dashboard/order_list.html'
    context_object_name = 'orders'

def dashboard(request):
    # Pie Chart: Order Status Distribution
    order_status_data = Orders.objects.values('status').annotate(count=Count('orderNumber'))
    order_status_labels = [item['status'] for item in order_status_data]
    order_status_counts = [item['count'] for item in order_status_data]

    # Line Chart: Monthly Orders
    monthly_orders = (
        Orders.objects
        .annotate(month=TruncMonth('orderDate'))
        .values('month')
        .annotate(count=Count('orderNumber'))
        .order_by('month')
    )
    monthly_order_labels = [item['month'].strftime('%B %Y') for item in monthly_orders]
    monthly_order_data = [item['count'] for item in monthly_orders]

    # Bar Chart: Sales by Product Line
    product_sales = (
        Products.objects
        .values('productLine')
        .annotate(total_sales=Sum('orderdetails__priceEach'))
        .order_by('-total_sales')
    )
    product_line_labels = [item['productLine'] for item in product_sales]
    product_line_sales = [float(item['total_sales']) if item['total_sales'] else 0 for item in product_sales]

    # Company Metrics
    company_metrics = {
        'total_customers': Customers.objects.count(),
        'total_orders': Orders.objects.count(),
        'total_employees': Employees.objects.count(),
        'total_products': Products.objects.count(),
    }

    # Top Products Table
    top_products = Products.objects.order_by('-quantityInStock')[:10]

    context = {
        'order_status_labels': json.dumps(order_status_labels),
        'order_status_counts': json.dumps(order_status_counts),
        'monthly_order_labels': json.dumps(monthly_order_labels),
        'monthly_order_data': json.dumps(monthly_order_data),
        'product_line_labels': json.dumps(product_line_labels),
        'product_line_sales': json.dumps(product_line_sales),
        'company_metrics': company_metrics,
        'top_products': top_products,
    }

    return render(request, 'dashboard/index.html', context)
