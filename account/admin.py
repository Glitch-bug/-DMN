from django.contrib import admin

from .models import UserBase, Address 


@admin.register(UserBase)
class UserBaseAdmin(admin.ModelAdmin):
    pass
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass