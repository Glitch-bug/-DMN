from django.forms import ValidationError
from django.shortcuts import render

from core.core_exceptions import handle_exception

from .models import Address, UserBase
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from .token import account_activation_token
from django.contrib.sites.shortcuts import get_current_site 
from rest_framework import status
from django.contrib.auth import login, logout
import traceback

# Create your views here.
@api_view(['POST'])
def account_create(request):
    try:
        data = request.data
        print(data)
        user = UserBase.objects.create_user(email=data['email'], first_name=data['first_name'], password=data['password'], last_name=data['last_name'])
        
        user.save()

        #Send email
        current_site = get_current_site(request)
        subject = 'Activate your Account'
        
        message = render_to_string('accounts/account_activation_email.html', {
            'user':user,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user)
        })
        print('okay')
        user.email_user(subject=subject, message=message)
        return Response({"message" : "Account has been created successfully", "data": user.to_dict(),}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return handle_exception(e)
@api_view(['GET'])
def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return Response({"message":"Account has been activated successfully", "data":user.to_dict()})
        else:
            return Response({"message":"Error User object does not exist"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return handle_exception(e)

@api_view(['POST'])
def account_login(request):
    try:
        data = request.data
        print(data["email"])
        user = UserBase.objects.get(email=data["email"])

        print(user.is_active)
        if user.is_active:
            if user.check_password(data["password"]):
                return Response({"message":"Logged in successfully", "data":user.to_dict()})
            else:
                return Response({"message":"Incorrect email or password", "data":user.to_dict()}, status= status.HTTP_401_UNAUTHORIZED)
        else:

            return Response({"message":"This account has not been verified check your email for the verification link", "data":user.to_dict(),})
    except Exception as e:
        return handle_exception(e)

# @api_view(['GET']) 
# def account_logout(request):
#     try:
#         logout(request)
#         return Response({"message":"User successfully logged out"})
#     except Exception as e:
#         print(e)
#         traceback.print_exc()
#         return Response({"message":"Failed to log out"})
    
@api_view(['POST'])
def account_delete(request):
    try:
        data = request.data
        user = UserBase.objects.get(email=data["email"])
        if user.is_active:
            user.is_active = False
            user.save()
            return Response({"message":"User account has been deleted"})
        else:
            return Response({"message":"Error User object does not exist"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return handle_exception(e)
    
@api_view(['PUT', 'GET'])
def account_edit(request, user_id):
    try:
        data = request.data
        user = UserBase.objects.get(id=user_id)
        if request.method == 'PUT':
            user.email = data["email"]
            user.first_name = data["first_name"]
            user.last_name = data["last_name"]
            user.save()
            return Response({"message":"User details edited successfully", "data":user.to_dict()})
        else:
            return Response({"message":"User details retrieved", "data":user.to_dict()})
    except Exception as e:
        return handle_exception(e)
# Addresses
@api_view(['GET'])
def view_addresses(request, user_id):
    try:
        user = UserBase.objects.get(id=user_id)
        addresses = user.list_addresses()
        print(addresses)
        return Response({"addresses":addresses})
    except Exception as e:
        return handle_exception(e)

@api_view(['POST'])
def add_address(request, user_id):
    try:
        data = request.data
        user = UserBase.objects.get(id=user_id)
        print(data["phone_number"])
        address = Address(user=user, phone_number=data["phone_number"], address_line = data['address_line'] , address_line2 = data["address_line2"], town_city=data["city"], delivery_instructions=data["delivery_instructions"], default=False, country= data["country"])
        address.save()
        return Response({"message":"User address saved successfully", "data": address.to_dict()})
    except Exception as e:
        return handle_exception(e)

@api_view(['GET','POST'])
def edit_address(request, user_id, address_id):
    try:
        data = request.data 
        if request.method == "POST":
            user = UserBase.objects.get(id=user_id)
            address = Address.objects.get(id=address_id)
            return Response({"message": "says something"})
        else:
            address = Address.objects.get(id=address_id)
            return Response({"address": {"phone_number":address.phone_number,"post_code":address.postcode, "address_line": address.address_line}})
    except ValidationError as e:
        return handle_exception(Address.DoesNotExist())
    except Exception as e: 
        return handle_exception(e)

