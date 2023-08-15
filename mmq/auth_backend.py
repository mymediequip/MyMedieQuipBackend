from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model



class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password.

    """
    def authenticate(self, request,username=None,password=None, **kwargs):
        print("\n in backend authentication")
        try:
            return get_user_model().objects.get(username=username)
        except:
            return None

    def get_user(self, user_id):
        print("in get user function ", user_id)
        try:
            return get_user_model().objects.get(pk=user_id)
        except User.DoesNotExist:
            return None