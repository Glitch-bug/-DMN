from django.shortcuts import render
from django.http import JsonResponse
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
    cart = Cart(request)
    print(type(cart.cart))
    qty = cart.__len__()
    total = cart.get_abstotal_price()
    return Response({"cart":cart.cart, "total_qty":qty, "total_price":total})
# spic = {"PK2":"NOT"}

# for key in spic:
#     print(spic[key])

@api_view(['POST'])
def update_cart(request):
    cart = Cart(request)
    try:
        data = request.data
        if Product.objects.get(id=data['product']['id'], in_stock= True):
            cart.add(data['product'], data['qty'])
            return Response(status=status.HTTP_200_OK)
        else:
            raise EmptyResultSet
    except Product.DoesNotExist:
        return Response({'message': "This product is not in stock"}, status=status.HTTP_404_NOT_FOUND)
    except  Exception as e:
        print(e)
        print(request.method)
        if (request.method != 'POST'):
            return Response({'message': "Only post methods are accepted"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return Response({'message': "Failed to add"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def delete_product(request):
    cart = Cart(request)
    try:
        data = request.data  
        delete = cart.delete(data['id'])
        return Response(status=status.HTTP_200_OK)
    except EmptyResultSet:
        return Response({'message': "This product is not in the cart"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        print(request.method)
        if (request.method != 'POST'):
            return Response({'message': "Only post methods are accepted"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return Response({'message': "Failed to delete product"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)