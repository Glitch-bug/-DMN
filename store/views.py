from django.shortcuts import render
from django.http import JsonResponse
from .serializers import CategorySerializers, ProductSerializers

from .models import Category, Product
# Create your views here.
def store_index(request):
    category = Category.objects.all()
    product = Product.objects.all()
    categories = CategorySerializers(category, many=True)
    products = ProductSerializers(product, many=True)
    return JsonResponse({"categories":categories.data, "products":products.data}, safe=False)