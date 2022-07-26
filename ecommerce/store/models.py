from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Product(models.Model):
    name = models.CharField(null=False, blank=False, max_length=256)
    description = models.TextField(null=False, blank=False, max_length=1024)
    price = models.DecimalField(null=False, blank=False, max_digits=15, decimal_places=2)
    image = models.ImageField(null=True, blank=True, upload_to='images/', default='images/default_product.png')
    quantity = models.SmallIntegerField(null=False, blank=False, default=0)
    eta = models.DurationField(null=False, blank=False)
    available = models.BooleanField(null=False, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	def __str__(self):
		return self.name


class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)

	@property
	def shipping(self):
		shipping = False
		order_items = self.order_item_set.all()
		for i in order_items:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		order_items = self.order_item_set.all()
		total = sum([item.get_total for item in order_items])
		return total

	@property
	def get_cart_items(self):
		order_items = self.order_item_set.all()
		total = sum([item.quantity for item in order_items])
		return total


class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=512, null=False)
    landmark = models.CharField(max_length=256, null=True, blank=True)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    phone_number = PhoneNumberField(blank=False, null=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address