from django.views import View
from django.shortcuts import render

# import your models here
from .models import Product

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
    context = {}
    return render(request, template_name='store/cart.html', context=context)

def checkout (request):
    context = {}
    return render(request, template_name='store/checkout.html', context=context)