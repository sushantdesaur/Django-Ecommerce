from django.views import View
from django.shortcuts import render, redirect

# import your models here
from .models import *

from .forms import ShippingAddressForm

# Create your views here.


def store (request):
    products = Product.objects.all()
    context = {
        'products': products
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
        order = {'get_cart_total': 0, 'get_cart_items': 0}   
    context = {
        'items': items,
        'order': order,
    }
    return render(request, template_name='store/cart.html', context=context)

def checkout (request):
    form = ShippingAddressForm()
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST or None)
        if form.is_valid():
            form.save(commit=True)
            return redirect("home")
        else:
            form = ShippingAddressForm()
    context = {
        'form': form
    }
    return render(request, template_name='store/checkout.html', context=context)