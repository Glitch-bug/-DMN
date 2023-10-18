from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission)
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, first_name, last_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

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

    # Delivery details 
    phone_number = models.CharField(max_length=150, blank=True)
    address_line_1 = models.CharField(max_length=150, blank=True)
    address_line_2 = models.CharField(max_length=150, blank=True)
    country = CountryField()

    #User Status 
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(
            subject, 
            message,
            'DMN@DMN.com',
            [self.email],
            fail_silently=False
        )


