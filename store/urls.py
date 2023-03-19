from django.urls import path
from . import views

urlpatterns = [
    path('store/', views.store_index, name="store")
]
