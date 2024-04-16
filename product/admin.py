from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path
from .forms import PriceAdjustmentForm
from .models import Category, PriceAdjustment, Vendor, Product, Weight

class ProductInline(admin.TabularInline):
    model = Product
    extra = 0  # Number of empty forms to display

class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'address')
    inlines = [ProductInline]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class WeightAdmin(admin.ModelAdmin):
    list_display = ('value', 'unit')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'weight', 'category', 'vendor', 'status', 'remark', 'view_count')
    list_filter = ('category', 'vendor', 'status')
    search_fields = ('name', 'vendor__name')
    readonly_fields = ('vendor_details',)  # Add vendor_details as a readonly field

    def vendor_details(self, obj):
        return f"{obj.vendor.name}\n{obj.vendor.phone_number}\n{obj.vendor.address}"  # Customize the vendor details display

    vendor_details.short_description = 'Vendor Details'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if obj:
            obj.view_count += 1
            obj.save()
        return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)

class PriceAdjustmentAdmin(admin.ModelAdmin):
    list_display = ('product', 'new_price', 'reason', 'user', 'created_at')
    list_filter = ('product', 'user', 'created_at')
    search_fields = ('product__name', 'user__username')

    def adjust_price_view(self, request):
        if request.method == 'POST':
            form = PriceAdjustmentForm(request.POST)
            if form.is_valid():
                price_adjustment = form.save(commit=False)
                price_adjustment.user = request.user
                price_adjustment.save()
                # Update product price
                price_adjustment.product.price = price_adjustment.new_price
                price_adjustment.product.save()
                return redirect('admin:index')  # Redirect to admin index page or adjust_price_success if defined
        else:
            form = PriceAdjustmentForm()
        return render(request, 'admin/adjust_price_form.html', {'form': form})

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('adjust-price/', self.admin_site.admin_view(self.adjust_price_view), name='adjust_price'),
        ]
        return custom_urls + urls


# Register models with the corresponding admin classes
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Product, ProductAdmin) 
admin.site.register(Weight, WeightAdmin) 
admin.site.register(PriceAdjustment, PriceAdjustmentAdmin)
