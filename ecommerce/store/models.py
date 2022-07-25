from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(null=False, blank=False, max_length=256)
    description = models.TextField(null=False, blank=False, max_length=1024)
    price = models.DecimalField(null=False, blank= False, max_digits=15, decimal_places=2)
    image = models.ImageField(null=True, blank=True, upload_to='images/', default='images/default_product.png')
    quantity = models.SmallIntegerField(null=False, blank=False, default=0)
    eta = models.DurationField(null=False, blank=False)
    available = models.BooleanField(null=False, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

