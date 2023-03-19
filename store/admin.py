from django.contrib import admin

from .models import Category, Product, Image
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass