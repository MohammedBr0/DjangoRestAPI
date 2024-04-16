from datetime import datetime, timedelta
from django.shortcuts import render
from product.models import Product, Category, Vendor, PriceAdjustment
from django.db.models import Avg

def home(request):
    # Total Number of Categories
    total_categories = Category.objects.count()

    # Total Number of Vendors
    total_vendors = Vendor.objects.count()

    # Average Product Price
    average_price = Product.objects.aggregate(avg_price=Avg('price'))['avg_price']

    # Recent Price Adjustments
    recent_price_adjustments = PriceAdjustment.objects.order_by('-created_at')[:5]

    # Product Status Summary
    product_status_summary = {
        'active': Product.objects.filter(status='Active').count(),
        'inactive': Product.objects.filter(status='Inactive').count()
    }
   
    def has_daily_adjustment(product):
        # Calculate the datetime threshold for the last 24 hours
        last_24_hours = datetime.now() - timedelta(hours=24)

        # Check if any price adjustment exists for the product within the last 24 hours
        return PriceAdjustment.objects.filter(product=product, created_at__gte=last_24_hours).exists()

    products_without_price_adjustments = Product.objects.all()
    for product in products_without_price_adjustments:
        product.has_daily_adjustment = has_daily_adjustment(product)

    # Define context data to pass to the template
    context = {
        'total_categories': total_categories,
        'total_vendors': total_vendors,
        'average_price': average_price,
        'recent_price_adjustments': recent_price_adjustments,
        'product_status_summary': product_status_summary,
        'products_without_price_adjustments': products_without_price_adjustments
    }

    # Render the template with the provided context data
    return render(request, 'home.html', context)
