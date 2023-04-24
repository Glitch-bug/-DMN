from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .serializers import CategorySerializers, ProductSerializers, ImageSerializers

from .models import Category, Product, Image
# Create your views here.
def store_index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    images = Image.objects.all()
    print(images)
    serial_categories = CategorySerializers(categories, many=True)
    serial_products = ProductSerializers(products, many=True)
    serial_images = ImageSerializers(images, many=True)
    return JsonResponse({"categories":serial_categories.data, "products":serial_products.data, "images":serial_images.data}, safe=False)

def product_detail(request, slug, id):
    product = get_object_or_404(Product, slug=slug, id=id, in_stock=True)
    images = product.images.all()
    serial_product = ProductSerializers(product)
    serial_images = ImageSerializers(images, many=True)
    return JsonResponse({"product":serial_product.data, "images":serial_images.data})

def category_list(request, slug):
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