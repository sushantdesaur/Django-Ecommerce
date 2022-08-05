from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.template import RequestContext


# import your models here
from .models import *

from .forms import ShippingAddressForm

# Create your views here.

def store (request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, template_name='store/store.html', context=context)


class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()

        context = {
            'products': products,
        }
        return render(request, 'store/products.html', context)

class ProductDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        product = Product.objects.get(pk=pk)

        context = {
            'product': product,
        }
        return render(request, 'store/product.html', context)


def cart (request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0,  'shipping': False}
    context = {
        'items': items,
        'order': order,
    }
    return render(request, template_name='store/cart.html', context=context)

def checkout (request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0,  'shipping': False}
    
    form = ShippingAddressForm()
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST or None)
        if form.is_valid():
            form.save(commit=True)
            return redirect("home")
        else:
            form = ShippingAddressForm()
    context = {
        'order': order,
        'items': items,
        'form': form,
    }
    return render(request, template_name='store/checkout.html', context=context)


def update_item(request):
    data = json.loads(request.body)
    
    product_id = data['productId']
    action = data['action']
    print('Product Id:', product_id)
    print('Action:', action)
    
    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)
        
    order_item.save()
    
    if order_item.quantity <= 0:
        order_item.delete()
        
    return JsonResponse('Item was added', safe=False)