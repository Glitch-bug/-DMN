from rest_framework import serializers

from .models import Category, Product, Image

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'description', 'cover', 'rating', 'price', 'in_stock', 'images']

class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'product', 'image']
