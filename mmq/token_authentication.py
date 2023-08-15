from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
# from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import exceptions

# from rest_framework.authtoken.models import Token

from django.utils.translation import gettext_lazy as _

#
#EXPIRE_HOURS = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_HOURS', 720)
EXPIRE_HOURS = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_HOURS', 4320)


class ExpiringTokenAuthentication(TokenAuthentication):

    def authenticate_credentials(self, key):
        try:
            token = self.get_model().objects.get(key=key)
        except self.get_model().DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')
        # check user status if user status 0 that means user still did not
        # verified his account
        if token.user.status == 0:

            if token.user.created_date < timezone.now() - timedelta(hours=EXPIRE_HOURS):
                    raise exceptions.AuthenticationFailed('not verified user')
        return (token.user, token)

