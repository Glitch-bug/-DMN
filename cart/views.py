from django.shortcuts import render
from .cart import Cart
# Create your views here.
def cart_summary(request):
    items = [item for item in cart]