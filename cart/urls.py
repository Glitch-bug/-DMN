from django.urls import path
from . import views 
 

app_name = 'cart'

urlpatterns = [
    path('', views.cart_summary, name='cart_summary'),
    path('update', views.update_cart, name="add_to_cart"),
    path('delete', views.delete_product, name="delete_product")
]