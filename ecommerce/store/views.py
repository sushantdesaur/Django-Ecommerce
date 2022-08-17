from multiprocessing import context
from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
import datetime

# import your utils here
from .utils import cart_data, guest_order

# import your models here
from .models import *

# import your forms here
from .forms import ShippingAddressForm, CustomerForm


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
    data = cart_data(request)
    
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']
      
    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items,
    }
    return render(request, template_name='store/cart.html', context=context)

def checkout (request):
    data = cart_data(request)

    cart_items = data['cart_items']
    order = data['order']
    items = data['items']
    
    context = {
        'order': order,
        'items': items,
        'cart_items': cart_items,
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


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guest_order(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            landmark=data['shipping']['landmark'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            country=data['shipping']['country'],
            phone_number=data['shipping']['phone_number'],
        )

    return JsonResponse('Payment submitted..', safe=False)


def orders(request):
    customer = request.user.customer
    orders = Order.objects.filter(customer=customer)
    
    context = {'orders': orders}
    
    return render(request, template_name='store/orders.html', context=context)
    