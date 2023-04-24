from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .serializers import CategorySerializers, ProductSerializers, ImageSerializers

from .models import Category, Product, Image
# Create your views here.
def store_index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    images = Image.objects.all()
    serial_categories = CategorySerializers(categories, many=True)
    serial_products = ProductSerializers(products, many=True)
    serial_images = ImageSerializers(images, many=True)
    return JsonResponse({"categories":serial_categories.data, "products":serial_products.data, "image":serial_images.data}, safe=False)

def product_detail(request, slug, id):
    product = get_object_or_404(Product, slug=slug, id=id, in_stock=True)
    serializer = ProductSerializers(product)
    return JsonResponse(serializer.data)

def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    category = CategorySerializers(category)
    products = ProductSerializers(products, many=True)
    return JsonResponse({'category':category.data, 'products':products.data})