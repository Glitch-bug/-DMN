from django.urls import path
from . import views

urlpatterns = [
    path('store/', views.store_index, name = "store"),
    path('<slug:slug>/<int:id>', views.product_detail, name = "product_detail"),
    path('store/<slug:slug>', views.category_list, name = "category_list"),
]
