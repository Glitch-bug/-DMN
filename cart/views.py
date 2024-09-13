import traceback
from django.shortcuts import render
from django.http import JsonResponse

from core.core_exceptions import handle_exception
from .cart import Cart
from store.models import Product
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.exceptions import EmptyResultSet

# Create your views here.
#TODO: Work here. Add: total price (for loop through dict)
@api_view(['GET'])
def cart_summary(request):
    try:
        cart = Cart(request)
        print(type(cart.cart))
        qty = cart.__len__()
        total = cart.get_abstotal_price()
        return Response({"cart":cart.cart, "total_qty":qty, "total_price":total})
    except Exception as e:
        return handle_exception(e)
# spic = {"PK2":"NOT"}

# for key in spic:
#     print(spic[key])

@api_view(['POST'])
def update_cart(request):
    cart = Cart(request)
    print(request)
    try:
        data = request.data
        if Product.objects.get(id=data['product']['id'], in_stock= True):
            cart.add(data['product'], data['qty'])
            print(cart.cart)
            return Response({'message': "Cart updated successfully"},status=status.HTTP_200_OK,)
        else:
            raise EmptyResultSet
    except Exception as e:
        return handle_exception(e)
 
@api_view(['POST'])
def delete_product(request):
    cart = Cart(request)
    try:
        data = request.data  
        cart.delete(data['id'])
        return Response({'message': "Product deleted successfully"},status=status.HTTP_200_OK)
    except EmptyResultSet:
        return Response({'message': "This product is not in the cart"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return handle_exception(e)