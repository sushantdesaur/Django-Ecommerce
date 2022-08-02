from django.contrib import admin

# import models here
from .models import Product, Order, OrderItem, Customer, ShippingAddress


# Register your models here.
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
