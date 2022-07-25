from django import views
from django.urls import path
from . import views
urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('products/', views.ProductListView.as_view(), name="products"),
    path('products/<int:pk>', views.ProductDetailView.as_view(), name='product'),
]
