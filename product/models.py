from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import psycopg2 as Database


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Weight(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=10)  # You might want to create a separate model for weight units if needed

    def __str__(self):
        return f"{self.value} {self.unit}"

class Product(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.ForeignKey(Weight, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    view_count = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def increment_view_count(self):
        self.view_count += 1
        self.save()

class PriceAdjustment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Price Adjustment for {self.product} by {self.user}"

@receiver(post_save, sender=PriceAdjustment)
def update_product_price(sender, instance, **kwargs):
    """
    Signal handler to update the product price when a PriceAdjustment instance is saved.
    """
    if kwargs['created']:
        instance.product.price = instance.new_price
        instance.product.save()
