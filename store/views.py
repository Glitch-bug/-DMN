from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .serializers import CategorySerializers, ProductSerializers, ImageSerializers
from rest_framework.decorators import api_view
from .models import Category, Product, Image
from rest_framework.response import Response
from rest_framework import status
import traceback

from core.core_exceptions import handle_exception
# Create your views here.
@api_view(['GET'])
def store_index(request):
    try:
        categories = Category.objects.all()
        products = Product.objects.all()
        images = Image.objects.all()
        serial_categories = CategorySerializers(categories, many=True)
        serial_products = ProductSerializers(products, many=True)
        serial_images = ImageSerializers(images, many=True)
        return JsonResponse({"categories":serial_categories.data, "products":serial_products.data, "images":serial_images.data}, safe=False)
   
    except Exception as e:
        handle_exception(e)

@api_view(['GET'])
def product_detail(request, slug, id):
    try:
        product = get_object_or_404(Product, slug=slug, id=id, in_stock=True)
        images = product.images.all()
        serial_product = ProductSerializers(product)
        serial_images = ImageSerializers(images, many=True)
        return JsonResponse({"product":serial_product.data, "images":serial_images.data})
    except Exception as e:
        handle_exception(e)

@api_view(['GET'])
def category_list(request, slug):
    try:
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=category)
        image_sets = [product.images.all() for product in products]
        images = []
        for set in image_sets:
            for item in set:
                images.append(item)
        print(images)
        serial_category = CategorySerializers(category)
        serial_products = ProductSerializers(products, many=True)
        serial_images = ImageSerializers(images, many=True)
        return JsonResponse({'category':serial_category.data, 'products':serial_products.data, 'images':serial_images.data})
    except Exception as e:
        handle_exception(e)
