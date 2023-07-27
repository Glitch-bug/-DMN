from django.test import TestCase 

from django.contrib.auth.models import User 

from store.models import Category, Product, Image

class TestCategoriesModel(TestCase):
    def setUp(self):
        self.data1 = Category.objects.create(name="django", slug="django")

    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))

    def test_category_model(self):
        data = self.data1
        self.assertEqual(str(data), 'django')

    

class TestProductsModels(TestCase):
    def setUp(self):
        Category.objects.create(name="django", slug="django")
        User.objects.create(username="admin")
        self.data1 = Product.objects.create(category_id=1, name="django beginners", created_by_id=1,
                                            slug="django-beginners", price=34.56, amount_in_stock = 5, rating=4)

                                        
                                
                            
    def test_products_model_entry(self):
        """
        Test product model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data,Product))
        self.assertEqual(str(data), 'django beginners')


class TestImageModel(TestCase):
    def setUp(self):
        Category.objects.create(name="django", slug="django")
        User.objects.create(username="admin")
        Product.objects.create(category_id=1, name="django beginners", created_by_id=1,
                                            slug="django-beginners", price=34.56, amount_in_stock = 5, rating = 4)
        self.data = Image.objects.create(product_id=1, image="necklace")
    
    def test_products_model_entry(self):
        """
        Test product model data insertion/types/field attributes
        """
        data = self.data
        self.assertTrue(isinstance(data, Image))