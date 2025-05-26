from django.shortcuts import render
from django.db.models import Sum, Count
from .models import Customers, Employees, Orders, Payments, Products

def dashboard(request):
    context = {
        # Revenue Data
        'revenue': {
            'total': Payments.objects.aggregate(total=Sum('amount'))['total'] or 0
        },

        # Company Metrics
        'company_metrics': {
            'total_customers': Customers.objects.count(),
            'total_orders': Orders.objects.count(),
            'total_employees': Employees.objects.count(),
            'total_products': Products.objects.count(),
        },

        # Top Customers by Total Payments
        'top_customers': Customers.objects.annotate(
            total_payments=Sum('payments__amount')
        ).order_by('-total_payments')[:10],

        # Top Products by Quantity Ordered
        'top_products': Products.objects.annotate(
            total_ordered=Sum('orderdetails__quantityOrdered')
        ).order_by('-total_ordered')[:10],

        # Recent Orders
        'recent_orders': Orders.objects.select_related(
            'customer'
        ).order_by('-orderDate')[:10],

        # Colors for UI (e.g. avatars)
        'colors': ['primary', 'success', 'warning', 'danger', 'info']
    }

    return render(request, 'dashboard/index.html', context)

def orders_list(request):
    orders = Orders.objects.select_related('customer').all()
    return render(request, 'dashboard/orders_list.html', {'orders': orders})