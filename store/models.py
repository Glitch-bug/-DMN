from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name="product", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='products', null=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='last_edited_by', null=True)
    name = models.CharField(max_length=255)
    designer = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    rating = models.IntegerField(
         validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=12,decimal_places=2)
    in_stock = models.BooleanField(default=True)
    amount_in_stock = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name
    
    def cover(self):
        if self.images.all():
            return self.images.all()[0].pk

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=f'images/products/')
    
    
