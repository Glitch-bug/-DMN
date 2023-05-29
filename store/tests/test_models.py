from django.test import TestCase 

from django.contrib.auth.models import User 

from store.models import Category, Product 

class TestCategoriesModel(TestCase):
    def setUp(self):
        self.data1 = Category.objects.create(name="django", slug="django")