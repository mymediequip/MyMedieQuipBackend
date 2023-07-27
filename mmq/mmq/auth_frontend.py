from datetime import timedelta

from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from rest_framework import exceptions, status
from rest_framework.response import Response

from mmq_apps.front.users.models import UserType

from django.core.exceptions import ObjectDoesNotExist

# We are using this class for custom user login as login functionality
#EXPIRE_HOURS = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_HOURS', 720)

EXPIRE_HOURS = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_HOURS', 4320)


def authenticate_frontend(email=None, password=None,user_type=None):

    if '@' in email:
        kwargs = {'email': email,'user_type_id':user_type}
    else:
        kwargs = {'mobile':email,'user_type_id':user_type}

    # print(kwargs,"kwargs")
    # else:
    # kwargs = {'username__iexact': email}
    try:
        try:
            user = get_user_model().objects.get(
                **kwargs, user_type__in=list(UserType.objects.all().values_list('id', flat=True)))

            # print(user,'---------user auth')

            
        except get_user_model().DoesNotExist:
            if "@" in email and "." in email:
                return None
            else:
                return None
        # print(password,'------------auth password')
        if user.check_password(password):
            print('check_password')
            # Here we also check condition for user who didnt verify their
            # email
            
            return user
    except Exception as e:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>auth front error", e)
        return None
