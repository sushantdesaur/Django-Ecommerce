from unicodedata import name
from django import views
from django.urls import path
from . import views


urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('products/', views.ProductListView.as_view(), name="products"),
    path('products/<int:pk>', views.ProductDetailView.as_view(), name='product'),
    
    path('update_item/', views.update_item, name='update_item'),
    
    path('process_order/', views.process_order, name="process_order"),
    
    path('orders/', views.orders, name="orders"),
]
