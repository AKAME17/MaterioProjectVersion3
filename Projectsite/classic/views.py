from django.shortcuts import render
from django.db import models  # Add this import
from .models import Film, Actor, Customer, Rental, Payment, Store, Inventory, Staff
from django.db.models import Sum, Count

from django.shortcuts import render
from django.db import models
from .models import Film, Actor, Customer, Rental, Payment, Store, Inventory, Staff
from django.db.models import Sum, Count

def dashboard(request):
    context = {
        # Revenue Data
        'revenue': {
            'total': Payment.objects.aggregate(total=Sum('amount'))['total'] or 0
        },
        
        # Store Metrics
        'store_metrics': {
            'total_stores': Store.objects.count(),
            'active_customers': Customer.objects.filter(active=True).count(),
            'available_films': Film.objects.filter(rental_duration__gt=0).count()
        },
        
        # Top Films (ordered by rental count)
        'top_films': Film.objects.annotate(
            rental_count=Count('inventory__rental')
        ).order_by('-rental_count')[:10],
        
        # Staff Performance
        'staff_performance': Staff.objects.annotate(
            rental_count=Count('rental'),
            payment_total=Sum('rental__payment__amount')
        ).order_by('-payment_total')[:5],
        
        # Latest Rentals
        'latest_rentals': Rental.objects.select_related(
            'inventory__film', 'customer', 'staff'
        ).order_by('-rental_date')[:10],
        
        # Colors for staff avatars
        'colors': ['primary', 'success', 'warning', 'danger', 'info']
    }
    
    return render(request, 'dashboard/index.html', context)

def rental_list(request):
    rentals = Rental.objects.all()  # Or whatever query you need
    return render(request, 'sakila/rental_list.html', {'rentals': rentals})