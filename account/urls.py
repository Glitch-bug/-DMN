from django.urls import path 
from . import views 

app_name="account"

urlpatterns = [
    path('create', views.account_create, name="create"),
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name="activate"),
    path('delete_account', views.account_delete, name="delete"),
    path('login_account', views.account_login, name="login"),
    path('edit/<slug:user_id>', views.account_edit, name="edit"),

    #Addresses
    path("addresses/<slug:user_id>", views.view_addresses, name="addresses"),
    path("add_address/<slug:user_id>", views.add_address, name="add_address"),
    path("edit_address/<slug:user_id>/<slug:address_id>", views.edit_address, name="edit_addres")

]