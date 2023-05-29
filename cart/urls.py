from django.urls import path
from . import views 
 

app_name = 'cart'

urlpartterns = [
    path('', views.basket_summary, name='cart_summary'),
]