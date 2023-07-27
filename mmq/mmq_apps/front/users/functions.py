import logging
import datetime
import random
import string
import requests
import json
import re

from django.conf import settings
from django.utils.timezone import utc
from rest_framework.authtoken.models import Token
from .serializers import *
from .models import *


def getToken(user_id):       
    token = Token()
    token.user_id = user_id
    token.created = datetime.datetime.utcnow().replace(tzinfo=utc)

    token.save()
    try:
        return token.key
    except Exception as e:
        print(e,'-------except error')
        return None
        
def createToken(user_id):

    try:
        token = Token.objects.filter(user_id=user_id)
        if len(token)>0:
            return token[0]
        else:
            token = Token()
            token.user_id = user_id
            token.created = datetime.datetime.utcnow().replace(tzinfo=utc)

            token.save()
            return token
    except Exception as e:
        print(e,'-----token create error')

        

def deleteToken(user_id):
    if user_id:
        # first check previous token if exist then delete
        # we will look option update_or_create
        try:
            token = Token.objects.get(user_id=user_id)
            token.delete()
            return 1

            # token.delete() # currently we have disable delete token
        except Token.DoesNotExist:
            pass
            # No need to log exception here :

        # End
    else:
        return -1


def isValidMobileNumber(mobile):
     
    # 1) Begins with 0 or 91
    # 2) Then contains 6,7 or 8 or 9.
    # 3) Then contains 9 digits
    Pattern = re.compile("(0|91)?[6-9][0-9]{9}")
    return Pattern.match(mobile)



