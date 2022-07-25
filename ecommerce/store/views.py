from multiprocessing import context
from django.shortcuts import render

# Create your views here.
# def index(request):
#     return render(request, template_name='index.html')


def store (request):
    context = {}
    return render(request, template_name='store/store.html', context=context)

def cart (request):
    context = {}
    return render(request, template_name='store/cart.html', context=context)

def checkout (request):
    context = {}
    return render(request, template_name='store/checkout.html', context=context)