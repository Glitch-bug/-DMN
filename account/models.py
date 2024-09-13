import uuid
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission,)

from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, first_name, last_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        print("User creation commenced")
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True'
            )
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True'
            )
        
        return self.create_user(email, first_name, last_name, password, **other_fields)
    
    def create_user(self, email, first_name, last_name, password, **other_fields):
    # def create_user(self, email, first_name, last_name, password):
        if not email:
            raise ValueError(_('You must provide an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name = last_name, **other_fields)
        # user = self.model(email=email, first_name=first_name, last_name = last_name) 
        user.set_password(password)
        user.save()
        return user
    
    
# Create your models here.
class UserBase(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    #User Status 
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(
            subject, 
            message,
            'Kwabenayiadom271@gmail.com',
            [self.email],
            fail_silently=False
        )

    def to_dict(self):
        if len(self.address_set.filter(default=True)) > 0:
            default_address  = self.address_set.get(default=True)
            return {'email':self.email, 'first_name':self.first_name, 'last_name':self.last_name, 'phone_number':default_address.phone_number, 'country':default_address.country.name}
        else:
             return {'email':self.email, 'first_name':self.first_name, 'last_name':self.last_name}
    
    def list_addresses(self):
        return [address.to_dict() for address in list(self.address_set.all())]


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserBase, verbose_name=_("User"), on_delete=models.CASCADE)
    phone_number = models.CharField(_("Phone Number"), max_length=50)
    postcode = models.CharField(_("Postcode"), max_length=50)
    address_line = models.CharField(_("Address Line 1"), max_length=255)
    address_line2 = models.CharField(_("Address Line 2"), max_length=255)
    town_city = models.CharField(_("Town/City/State"), max_length=150)
    delivery_instructions = models.CharField(_("Delivery Instructions"), max_length=255)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    default = models.BooleanField(_("Default"), default=False)
    country = CountryField()


    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
    
    def to_dict(self):
        return {'id': self.pk, 'phone_number': self.phone_number, 'postcode': self.postcode, 'addresss_line': self.address_line, 'address_line2': self.address_line2, 'town_city': self.town_city, 'delivery_instructions':self.delivery_instructions, 'created_at': self.created_at, 'updated_at': self.updated_at, 'default': self.default, 'country': self.country.name}

    def __str__(self):
        return f"{self.town_city}"
