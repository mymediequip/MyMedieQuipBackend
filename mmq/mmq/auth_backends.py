from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from mmq.users.models import UserType

# We are using this class for API authentication + django ADMIN ACCESS



class UsersModelBackend(ModelBackend):

    def authenticate(self, request, email=None, password=None):
        if '@' in email:
            kwargs = {'email': email}
            print(email, password,'--------?????????')
        
        try:
            user = self.user_class.objects.get(
                **kwargs, user_type__in=list(UserType.objects.all().values_list('id', flat=True)))
            print(user,'------useeeerrrrrrrrrrrr')
            
            if user.check_password(password):
                print(user,'-----------() check_password')

                return user
        except self.user_class.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return self.user_class.objects.get(pk=user_id)
        except self.user_class.DoesNotExist:
            return None

    @property
    def user_class(self):
        print('test111111111111')
        if not hasattr(self, '_user_class'):
            self._user_class = get_user_model()
            if not self._user_class:
                raise ImproperlyConfigured('Could not get custom user model')
        return self._user_class
