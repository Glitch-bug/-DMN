from django.shortcuts import render
from .models import CustomAccountManager, UserBase
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from .token import account_activation_token
from django.contrib.sites.shortcuts import get_current_site 

# Create your views here.
@api_view(['POST'])
def account_register(request):
    try:
        data = request.data
        user = UserBase.objects.create_user(email=data['email'], user_name=data['user_name'], password=data['password'])
        user.save()

        #Send email
        current_site = get_current_site(request)
        subject = 'Activate you Account'
        message = render_to_string('account/registration/account_activation_email.html', {
            'user':user,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user)
        })
        user.email_user(subject=subject, message=message)
        return Response({"message" : "User has been created successfully"})
    except:
        pass

